"""
Tests voor utility functies.
"""
import pytest
import json
from pathlib import Path
from src.utils import (
    load_questions_from_json,
    save_questions_to_json,
    load_question_bank,
    save_question_bank,
    create_example_question_bank
)
from src.models import (
    Question,
    QuestionBank,
    QuestionType,
    DifficultyLevel,
    LearningObjective
)


def test_create_example_question_bank():
    """Test het aanmaken van een voorbeeld vragenbank."""
    bank = create_example_question_bank()

    assert bank.name == "Voorbeeld Vragenbank"
    assert len(bank.questions) > 0
    assert all(isinstance(q, Question) for q in bank.questions)


def test_save_and_load_questions(tmp_path):
    """Test het opslaan en laden van vragen."""
    # Maak test vragen
    questions = [
        Question(
            id="q001",
            question_text="Test vraag 1",
            question_type=QuestionType.OPEN,
            difficulty=DifficultyLevel.MAKKELIJK,
            learning_objectives=[
                LearningObjective(id="lo-1", description="Test", category="test")
            ],
            correct_answer="antwoord"
        ),
        Question(
            id="q002",
            question_text="Test vraag 2",
            question_type=QuestionType.MEERKEUZE,
            difficulty=DifficultyLevel.GEMIDDELD,
            learning_objectives=[
                LearningObjective(id="lo-2", description="Test 2", category="test")
            ],
            answers=[]
        )
    ]

    # Sla op
    file_path = tmp_path / "test_questions.json"
    save_questions_to_json(questions, file_path)

    # Controleer dat bestand bestaat
    assert file_path.exists()

    # Laad terug
    loaded_questions = load_questions_from_json(file_path)

    # Vergelijk
    assert len(loaded_questions) == len(questions)
    assert loaded_questions[0].id == questions[0].id
    assert loaded_questions[1].id == questions[1].id


def test_save_and_load_question_bank(tmp_path):
    """Test het opslaan en laden van een vragenbank."""
    # Maak test bank
    bank = QuestionBank(
        name="Test Bank",
        description="Test beschrijving",
        questions=[
            Question(
                id="q001",
                question_text="Test",
                question_type=QuestionType.OPEN,
                difficulty=DifficultyLevel.GEMIDDELD,
                learning_objectives=[
                    LearningObjective(id="lo-1", description="Test", category="test")
                ],
                correct_answer="test"
            )
        ]
    )

    # Sla op
    file_path = tmp_path / "test_bank.json"
    save_question_bank(bank, file_path)

    # Laad terug
    loaded_bank = load_question_bank(file_path)

    # Vergelijk
    assert loaded_bank.name == bank.name
    assert loaded_bank.description == bank.description
    assert len(loaded_bank.questions) == len(bank.questions)
    assert loaded_bank.questions[0].id == bank.questions[0].id


def test_load_questions_from_list(tmp_path):
    """Test laden van vragen uit een lijst JSON."""
    # Maak een JSON bestand met een lijst van vragen
    questions_data = [
        {
            "id": "q001",
            "question_text": "Test 1",
            "question_type": "open",
            "difficulty": "makkelijk",
            "learning_objectives": [
                {"id": "lo-1", "description": "Test", "category": "test"}
            ],
            "correct_answer": "test"
        }
    ]

    file_path = tmp_path / "questions_list.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(questions_data, f)

    # Laad
    questions = load_questions_from_json(file_path)

    assert len(questions) == 1
    assert questions[0].id == "q001"


def test_load_questions_from_bank_format(tmp_path):
    """Test laden van vragen uit vragenbank formaat."""
    # Maak een JSON bestand met vragenbank structuur
    bank_data = {
        "name": "Test",
        "questions": [
            {
                "id": "q001",
                "question_text": "Test 1",
                "question_type": "open",
                "difficulty": "makkelijk",
                "learning_objectives": [
                    {"id": "lo-1", "description": "Test", "category": "test"}
                ],
                "correct_answer": "test"
            }
        ]
    }

    file_path = tmp_path / "bank_format.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(bank_data, f)

    # Laad
    questions = load_questions_from_json(file_path)

    assert len(questions) == 1
    assert questions[0].id == "q001"


def test_load_nonexistent_file():
    """Test laden van niet-bestaand bestand."""
    with pytest.raises(FileNotFoundError):
        load_questions_from_json("nonexistent.json")


def test_save_creates_directory(tmp_path):
    """Test dat opslaan automatisch directories aanmaakt."""
    file_path = tmp_path / "subdir" / "nested" / "questions.json"

    questions = [
        Question(
            id="q001",
            question_text="Test",
            question_type=QuestionType.OPEN,
            difficulty=DifficultyLevel.MAKKELIJK,
            learning_objectives=[
                LearningObjective(id="lo-1", description="Test", category="test")
            ],
            correct_answer="test"
        )
    ]

    save_questions_to_json(questions, file_path)

    assert file_path.exists()
    assert file_path.parent.exists()
