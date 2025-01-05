from typing import List, Optional
from datetime import datetime
from text_processing.cleaning_rules import TextCleaningRule, TimestampRule, AudioPlaceholderRule, WhitespaceRule
from domain.models import ProcessedText


class TextCleaner:
    def __init__(self, rules: Optional[List[TextCleaningRule]] = None):
        self._rules = rules or [
            TimestampRule(),
            AudioPlaceholderRule(),
            WhitespaceRule()
        ]

    def clean(self, text: str) -> ProcessedText:
        original_length = len(text)
        processed = text

        for rule in self._rules:
            processed = rule.apply(processed)

        return ProcessedText(
            content=processed,
            processed_at=datetime.now(),
            original_length=original_length,
            processed_length=len(processed)
        )
