"""
Utility functies voor het laden en opslaan van vragen.
"""
import json
from pathlib import Path
from typing import List
from .models import Question, QuestionBank, GeneratedQuestion


def load_questions_from_json(file_path: str | Path) -> List[Question]:
    """
    Laad vragen uit een JSON bestand.

    Args:
        file_path: Pad naar het JSON bestand

    Returns:
        Lijst met Question objecten
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Bestand niet gevonden: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = []
    if isinstance(data, list):
        # Direct een lijst van vragen
        for q_data in data:
            questions.append(Question(**q_data))
    elif isinstance(data, dict):
        # Mogelijk een QuestionBank
        if "questions" in data:
            for q_data in data["questions"]:
                questions.append(Question(**q_data))
        else:
            # Enkele vraag
            questions.append(Question(**data))

    return questions


def save_questions_to_json(
    questions: List[Question],
    file_path: str | Path,
    pretty: bool = True
) -> None:
    """
    Sla vragen op naar een JSON bestand.

    Args:
        questions: Lijst met Question objecten
        file_path: Pad waar het bestand moet worden opgeslagen
        pretty: Of de JSON geformatteerd moet worden
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Converteer naar dictionaries
    questions_data = [q.model_dump() for q in questions]

    with open(file_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(questions_data, f, indent=2, ensure_ascii=False)
        else:
            json.dump(questions_data, f, ensure_ascii=False)


def load_question_bank(file_path: str | Path) -> QuestionBank:
    """
    Laad een vragenbank uit een JSON bestand.

    Args:
        file_path: Pad naar het JSON bestand

    Returns:
        QuestionBank object
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Bestand niet gevonden: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return QuestionBank(**data)


def save_question_bank(
    question_bank: QuestionBank,
    file_path: str | Path,
    pretty: bool = True
) -> None:
    """
    Sla een vragenbank op naar een JSON bestand.

    Args:
        question_bank: QuestionBank object
        file_path: Pad waar het bestand moet worden opgeslagen
        pretty: Of de JSON geformatteerd moet worden
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(
                question_bank.model_dump(),
                f,
                indent=2,
                ensure_ascii=False
            )
        else:
            json.dump(
                question_bank.model_dump(),
                f,
                ensure_ascii=False
            )


def save_generated_questions(
    generated_questions: List[GeneratedQuestion],
    file_path: str | Path,
    pretty: bool = True
) -> None:
    """
    Sla gegenereerde vragen op naar een JSON bestand.

    Args:
        generated_questions: Lijst met GeneratedQuestion objecten
        file_path: Pad waar het bestand moet worden opgeslagen
        pretty: Of de JSON geformatteerd moet worden
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Converteer naar dictionaries
    data = [gq.model_dump() for gq in generated_questions]

    with open(file_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            json.dump(data, f, ensure_ascii=False)


def create_example_question_bank() -> QuestionBank:
    """
    Maak een voorbeeld vragenbank voor demonstratie.

    Returns:
        QuestionBank met voorbeeldvragen
    """
    from .models import (
        Question,
        QuestionType,
        DifficultyLevel,
        LearningObjective,
        Answer
    )

    questions = [
        Question(
            id="q001",
            question_text="Wat is de hoofdstad van Nederland?",
            question_type=QuestionType.MEERKEUZE,
            difficulty=DifficultyLevel.MAKKELIJK,
            learning_objectives=[
                LearningObjective(
                    id="geo-nl-1",
                    description="Kan de hoofdstad van Nederland noemen",
                    category="geografie"
                )
            ],
            answers=[
                Answer(text="Rotterdam", is_correct=False),
                Answer(text="Amsterdam", is_correct=True),
                Answer(text="Den Haag", is_correct=False),
                Answer(text="Utrecht", is_correct=False)
            ],
            explanation="Amsterdam is de hoofdstad van Nederland volgens de grondwet.",
            tags=["geografie", "nederland", "basis"]
        ),
        Question(
            id="q002",
            question_text="Los op: 2x + 5 = 13. Wat is x?",
            question_type=QuestionType.OPEN,
            difficulty=DifficultyLevel.GEMIDDELD,
            learning_objectives=[
                LearningObjective(
                    id="wiskunde-algebra-1",
                    description="Kan lineaire vergelijkingen met één onbekende oplossen",
                    category="algebra"
                )
            ],
            correct_answer="4",
            explanation="2x = 13 - 5 = 8, dus x = 8 / 2 = 4",
            hints=[
                "Trek eerst 5 af van beide kanten",
                "Deel dan beide kanten door 2"
            ],
            tags=["wiskunde", "algebra", "vergelijkingen"]
        ),
        Question(
            id="q003",
            question_text="Fotosynthese vindt plaats in de chloroplasten van plantencellen.",
            question_type=QuestionType.WAAR_ONWAAR,
            difficulty=DifficultyLevel.MAKKELIJK,
            learning_objectives=[
                LearningObjective(
                    id="biologie-planten-1",
                    description="Begrijpt waar fotosynthese plaatsvindt",
                    category="biologie"
                )
            ],
            answers=[
                Answer(text="Waar", is_correct=True),
                Answer(text="Onwaar", is_correct=False)
            ],
            explanation="Fotosynthese vindt inderdaad plaats in chloroplasten, de groene structuren in plantencellen.",
            tags=["biologie", "planten", "fotosynthese"]
        )
    ]

    return QuestionBank(
        name="Voorbeeld Vragenbank",
        description="Een verzameling voorbeeldvragen voor verschillende vakken",
        questions=questions
    )
