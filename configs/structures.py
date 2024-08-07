from pydantic import BaseModel
from typing import List


class SentenceEvaluation(BaseModel):
    sentence_number: int
    original_sentence: str
    translated_sentence: str
    additional_comments: str
    accuracy: str
    meaning_intact: str
    well_phrased: str
    errors: str


class TranslationEvaluation(BaseModel):
    evaluations: List[SentenceEvaluation]
    explanation: str
    overall_translation_quality: int
