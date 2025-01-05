from typing import List
from config.env import NLPConfig


class NLPBasedExtractor:
    def __init__(self, nlp_model, config: NLPConfig):
        self._nlp = nlp_model
        self._config = config
        self._nlp.max_length = config.max_length

    def extract_sentences(self, text: str) -> List[str]:
        doc = self._nlp(text)
        return [
            sent.text.strip()
            for sent in doc.sents
            if self._is_valid_sentence(sent)
        ]

    def _is_valid_sentence(self, sent) -> bool:
        text = sent.text.strip()
        return bool(text and len(text.split()) > 1)
