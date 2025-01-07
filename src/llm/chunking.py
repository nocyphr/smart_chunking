from llama_index.llms.litellm import LiteLLM
from llama_index.core.agent import ReActAgent
from llama_index.core.memory.chat_memory_buffer import ChatMemoryBuffer
from re import search
import logging
from typing import List, Optional, Tuple
from config.env import LLMConfig
from llm.rate_limiter import RateLimiter, count_tokens
from domain.models import Chunk
from llama_index.core.tools import FunctionTool


class TextChunker:
    def __init__(self, config: LLMConfig, rate_limiter: RateLimiter):
        self._llm = LiteLLM(model=config.model, api_key=config.api_key)
        self._rate_limiter = rate_limiter
        self._use_agent = config.use_agent

        if self._use_agent:
            memory = ChatMemoryBuffer.from_defaults(chat_history=[], llm=self._llm)

            def return_response(response: str) -> str:
                """Use this tool to return your final APPEND or CUT decision for the text chunk."""
                return response

            return_response_tool = FunctionTool.from_defaults(
                fn=return_response,
                name="return_response"
            )
            self._agent = ReActAgent(
                tools=[return_response_tool],
                llm=self._llm,
                memory=None,
                max_iterations=9,
                verbose=False
            )

    async def categorize_relevance(
        self,
        data: dict,
        prompt_template: str,
        progress: Optional[Tuple[int, int]] = None
    ) -> Optional[str]:
        prompt = prompt_template.format(**data)
        tokens = count_tokens(prompt)

        try:
            await self._rate_limiter.acquire(tokens, progress)
            logging.info(f"Making API call (prompt tokens: {tokens})")
            if self._use_agent:
                response = self._agent.chat(prompt)
                response_text = response.response
            else:
                response = self._llm.complete(prompt)
                response_text = response.text
            return self._validate_response(response_text, tokens)
        except Exception as e:
            logging.error(f"API call failed: {str(e)}")
            raise

    def _validate_response(self, response_text: str, tokens: int) -> Optional[str]:
        match = search(r'(APPEND|CUT)', response_text)
        if not match:
            logging.warning("Invalid response format")
            return None

        status = match.group(1)
        logging.info(f"Got valid response: {status} (prompt tokens: {tokens})")
        return status

    async def chunk_text(self, sentences: List[str], prompt_template: str) -> List[Chunk]:
        chunks = []
        current_chunk = []
        current_indices = []

        for i, sentence in enumerate(sentences, 1):

            if not current_chunk:
                current_chunk = [sentence]
                current_indices = [i-1]
                continue

            data = {'sentence': sentence, 'chunk': ' '.join(current_chunk)}
            status = await self.categorize_relevance(data, prompt_template, (i, len(sentences)))

            if not status:
                continue

            if status == 'APPEND':
                current_chunk.append(sentence)
                current_indices.append(i-1)
            else:
                chunks.append(Chunk(
                    content=' '.join(current_chunk),
                    sequence_number=len(chunks),
                    source_sentence_ids=current_indices
                ))
                current_chunk = [sentence]
                current_indices = [i-1]

        if current_chunk:
            chunks.append(Chunk(
                content=' '.join(current_chunk),
                sequence_number=len(chunks),
                source_sentence_ids=current_indices
            ))

        return chunks
