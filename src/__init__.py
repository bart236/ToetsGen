"""
ToetsGen - Een toetsgenerator voor het maken van alternatieve vragen.
"""

from .models import (
    Question,
    QuestionBank,
    GeneratedQuestion,
    DifficultyLevel,
    QuestionType,
    LearningObjective,
    Answer
)
from .generator import QuestionGenerator
from .llm_client import LLMClient
from .config import settings
from .utils import (
    load_questions_from_json,
    save_questions_to_json,
    load_question_bank,
    save_question_bank,
    save_generated_questions,
    create_example_question_bank
)

__version__ = "0.1.0"

__all__ = [
    # Models
    "Question",
    "QuestionBank",
    "GeneratedQuestion",
    "DifficultyLevel",
    "QuestionType",
    "LearningObjective",
    "Answer",
    # Generator
    "QuestionGenerator",
    "LLMClient",
    # Config
    "settings",
    # Utils
    "load_questions_from_json",
    "save_questions_to_json",
    "load_question_bank",
    "save_question_bank",
    "save_generated_questions",
    "create_example_question_bank",
]
