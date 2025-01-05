from re import sub
from abc import ABC, abstractmethod


class TextCleaningRule(ABC):
    @abstractmethod
    def apply(self, text: str) -> str:
        pass


class TimestampRule(TextCleaningRule):
    def apply(self, text: str) -> str:
        return sub(r'\d{2}:\d{2}:\d{2}.\d{3}\s+', '', text).strip()


class AudioPlaceholderRule(TextCleaningRule):
    def apply(self, text: str) -> str:
        return sub(r'\[.*?\]', '', text).strip()


class WhitespaceRule(TextCleaningRule):
    def apply(self, text: str) -> str:
        return sub(r'\s+', ' ', text).strip()
