from pathlib import Path
import asyncio
import spacy
import logging
from config.env import get_config, AppConfig
from text_processing.cleaner import TextCleaner
from text_processing.extractor import NLPBasedExtractor
from llm.chunking import TextChunker
from llm.rate_limiter import RateLimiter, RateLimitConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class TranscriptProcessor:
    def __init__(self, config: AppConfig):
        self._config = config
        self._setup_components()

    def _setup_components(self):
        self._nlp = spacy.load(self._config.nlp.model)
        self._cleaner = TextCleaner()
        self._extractor = NLPBasedExtractor(
            nlp_model=self._nlp,
            config=self._config.nlp
        )

        rate_limiter = RateLimiter(
            config=RateLimitConfig(
                token_limit=self._config.llm.token_limit,
                request_limit=self._config.llm.request_limit,
                time_window=self._config.llm.time_window
            )
        )

        self._chunker = TextChunker(
            config=self._config.llm,
            rate_limiter=rate_limiter
        )

    def _read_file(self, filepath: str) -> str:
        return Path(filepath).read_text(encoding='utf-8')

    def _save_file(self, filepath: str, content: list[str]):
        output_path = Path(filepath)
        output_path.parent.mkdir(exist_ok=True)
        output_path.write_text(
            '\n'.join(content),
            encoding='utf-8'
        )

    async def process_transcript(self):
        logging.info("Starting transcript processing...")

        raw_text = self._read_file(self._config.files.input_path)
        cleaned = self._cleaner.clean(raw_text)
        logging.info(f"Cleaned text: {cleaned.processed_length} chars")

        sentences = self._extractor.extract_sentences(cleaned.content)
        logging.info(f"Extracted {len(sentences)} sentences")

        prompt_template = self._read_file(
            self._config.files.prompt_template_path)
        chunks = await self._chunker.chunk_text(sentences, prompt_template)
        logging.info(f"Created {len(chunks)} chunks")

        chunk_texts = [chunk.content for chunk in chunks]
        self._save_file(self._config.files.output_path, chunk_texts)
        logging.info(f"Results saved to {self._config.files.output_path}")

        return chunks


async def main():
    config = get_config()
    processor = TranscriptProcessor(config)
    chunks = await processor.process_transcript()
    print(f'Total chunks extracted: {len(chunks)}')

if __name__ == '__main__':
    asyncio.run(main())
