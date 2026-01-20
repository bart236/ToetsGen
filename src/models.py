"""
Data modellen voor toetsvragen en leerdoelen.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from enum import Enum


class DifficultyLevel(str, Enum):
    """Moeilijkheidsgraad van een vraag."""
    ZEER_MAKKELIJK = "zeer_makkelijk"
    MAKKELIJK = "makkelijk"
    GEMIDDELD = "gemiddeld"
    MOEILIJK = "moeilijk"
    ZEER_MOEILIJK = "zeer_moeilijk"


class QuestionType(str, Enum):
    """Type vraag."""
    MEERKEUZE = "meerkeuze"
    OPEN = "open"
    WAAR_ONWAAR = "waar_onwaar"
    INVUL = "invul"


class LearningObjective(BaseModel):
    """Leerdoel van een vraag."""
    id: str = Field(..., description="Unieke identifier voor het leerdoel")
    description: str = Field(..., description="Beschrijving van het leerdoel")
    category: Optional[str] = Field(None, description="Categorie van het leerdoel")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "wiskunde-algebra-1",
                "description": "Kan kwadratische vergelijkingen oplossen",
                "category": "algebra"
            }
        }


class Answer(BaseModel):
    """Een antwoordoptie voor meerkeuzevragen."""
    text: str = Field(..., description="Tekst van het antwoord")
    is_correct: bool = Field(..., description="Of dit het correcte antwoord is")
    explanation: Optional[str] = Field(None, description="Uitleg waarom dit antwoord (on)juist is")


class Question(BaseModel):
    """Een toetsvraag met alle metadata."""
    id: str = Field(..., description="Unieke identifier voor de vraag")
    question_text: str = Field(..., description="De vraag zelf")
    question_type: QuestionType = Field(..., description="Type vraag")
    difficulty: DifficultyLevel = Field(..., description="Moeilijkheidsgraad")
    learning_objectives: List[LearningObjective] = Field(
        ...,
        description="Leerdoelen die deze vraag test"
    )
    answers: Optional[List[Answer]] = Field(
        None,
        description="Antwoordopties (voor meerkeuzevragen)"
    )
    correct_answer: Optional[str] = Field(
        None,
        description="Correct antwoord (voor open vragen)"
    )
    hints: Optional[List[str]] = Field(
        default=None,
        description="Hints om de vraag op te lossen"
    )
    explanation: Optional[str] = Field(
        None,
        description="Uitleg van het correcte antwoord"
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="Extra tags voor categorisatie"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "q001",
                "question_text": "Wat is de wortel van 16?",
                "question_type": "meerkeuze",
                "difficulty": "makkelijk",
                "learning_objectives": [
                    {
                        "id": "wiskunde-wortels-1",
                        "description": "Kan vierkantswortels berekenen",
                        "category": "wiskunde"
                    }
                ],
                "answers": [
                    {"text": "2", "is_correct": False},
                    {"text": "4", "is_correct": True},
                    {"text": "8", "is_correct": False},
                    {"text": "16", "is_correct": False}
                ],
                "explanation": "De vierkantswortel van 16 is 4, omdat 4 × 4 = 16"
            }
        }


class GeneratedQuestion(BaseModel):
    """Een gegenereerde alternatieve vraag."""
    original_question_id: str = Field(..., description="ID van de originele vraag")
    generated_question: Question = Field(..., description="De gegenereerde vraag")
    similarity_score: Optional[float] = Field(
        None,
        description="Score voor gelijkenis met origineel (0-1)",
        ge=0.0,
        le=1.0
    )
    generation_metadata: Optional[dict] = Field(
        default=None,
        description="Metadata over de generatie"
    )


class QuestionBank(BaseModel):
    """Een verzameling vragen."""
    name: str = Field(..., description="Naam van de vragenbank")
    description: Optional[str] = Field(None, description="Beschrijving van de vragenbank")
    questions: List[Question] = Field(default_factory=list, description="Lijst met vragen")

    def add_question(self, question: Question) -> None:
        """Voeg een vraag toe aan de bank."""
        self.questions.append(question)

    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Haal een vraag op via ID."""
        for question in self.questions:
            if question.id == question_id:
                return question
        return None

    def get_questions_by_difficulty(self, difficulty: DifficultyLevel) -> List[Question]:
        """Haal alle vragen op met een specifieke moeilijkheidsgraad."""
        return [q for q in self.questions if q.difficulty == difficulty]
