from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass(frozen=True)
class ProcessedText:
    content: str
    processed_at: datetime
    original_length: int
    processed_length: int


@dataclass(frozen=True)
class Chunk:
    content: str
    sequence_number: int
    source_sentence_ids: List[int]
