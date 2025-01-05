from dataclasses import dataclass
from functools import lru_cache
import os
from typing import Optional
from dotenv import load_dotenv


@dataclass(frozen=True)
class LLMConfig:
    model: str
    api_key: str
    request_limit: int
    token_limit: int
    time_window: float


@dataclass(frozen=True)
class NLPConfig:
    model: str
    max_length: int


@dataclass(frozen=True)
class FileConfig:
    input_path: str
    output_path: str
    prompt_template_path: str


@dataclass(frozen=True)
class AppConfig:
    llm: LLMConfig
    nlp: NLPConfig
    files: FileConfig


class EnvironmentConfigLoader:
    def __init__(self, env_file: Optional[str] = None):
        load_dotenv(env_file)

    def _get_env_or_raise(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Missing required environment variable: {key}")
        return value

    def _get_env_int(self, key: str) -> int:
        return int(self._get_env_or_raise(key))

    def _get_env_float(self, key: str) -> float:
        return float(self._get_env_or_raise(key))

    def load_llm_config(self) -> LLMConfig:
        return LLMConfig(
            model=self._get_env_or_raise('LLM_MODEL'),
            api_key=self._get_env_or_raise('LLM_API_KEY'),
            request_limit=self._get_env_int('LLM_REQUEST_LIMIT'),
            token_limit=self._get_env_int('LLM_TOKEN_LIMIT'),
            time_window=self._get_env_float('LLM_TIME_WINDOW')
        )

    def load_nlp_config(self) -> NLPConfig:
        return NLPConfig(
            model=self._get_env_or_raise('NLP_MODEL'),
            max_length=self._get_env_int('NLP_MAX_LENGTH')
        )

    def load_file_config(self) -> FileConfig:
        return FileConfig(
            input_path=self._get_env_or_raise('INPUT_TRANSCRIPT_PATH'),
            output_path=self._get_env_or_raise('OUTPUT_CHUNKS_PATH'),
            prompt_template_path=self._get_env_or_raise('PROMPT_TEMPLATE_PATH')
        )

    def load_config(self) -> AppConfig:
        return AppConfig(
            llm=self.load_llm_config(),
            nlp=self.load_nlp_config(),
            files=self.load_file_config()
        )


@lru_cache()
def get_config(env_file: Optional[str] = None) -> AppConfig:
    loader = EnvironmentConfigLoader(env_file)
    return loader.load_config()
