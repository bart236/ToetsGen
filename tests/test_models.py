"""
Tests voor de data modellen.
"""
import pytest
from src.models import (
    Question,
    QuestionBank,
    DifficultyLevel,
    QuestionType,
    LearningObjective,
    Answer
)


def test_learning_objective_creation():
    """Test het aanmaken van een leerdoel."""
    lo = LearningObjective(
        id="test-1",
        description="Test leerdoel",
        category="test"
    )
    assert lo.id == "test-1"
    assert lo.description == "Test leerdoel"
    assert lo.category == "test"


def test_answer_creation():
    """Test het aanmaken van een antwoord."""
    answer = Answer(
        text="Test antwoord",
        is_correct=True,
        explanation="Dit is het juiste antwoord"
    )
    assert answer.text == "Test antwoord"
    assert answer.is_correct is True
    assert answer.explanation == "Dit is het juiste antwoord"


def test_multiple_choice_question():
    """Test het aanmaken van een meerkeuzevraag."""
    question = Question(
        id="q001",
        question_text="Test vraag?",
        question_type=QuestionType.MEERKEUZE,
        difficulty=DifficultyLevel.GEMIDDELD,
        learning_objectives=[
            LearningObjective(
                id="lo-1",
                description="Test leerdoel",
                category="test"
            )
        ],
        answers=[
            Answer(text="Optie 1", is_correct=False),
            Answer(text="Optie 2", is_correct=True),
            Answer(text="Optie 3", is_correct=False),
        ],
        explanation="Optie 2 is correct"
    )

    assert question.id == "q001"
    assert question.question_type == QuestionType.MEERKEUZE
    assert question.difficulty == DifficultyLevel.GEMIDDELD
    assert len(question.answers) == 3
    assert question.answers[1].is_correct is True


def test_open_question():
    """Test het aanmaken van een open vraag."""
    question = Question(
        id="q002",
        question_text="Wat is 2+2?",
        question_type=QuestionType.OPEN,
        difficulty=DifficultyLevel.MAKKELIJK,
        learning_objectives=[
            LearningObjective(
                id="lo-1",
                description="Kan optellen",
                category="wiskunde"
            )
        ],
        correct_answer="4",
        explanation="2+2=4"
    )

    assert question.id == "q002"
    assert question.question_type == QuestionType.OPEN
    assert question.correct_answer == "4"
    assert question.answers is None


def test_question_bank():
    """Test het aanmaken en gebruiken van een vragenbank."""
    bank = QuestionBank(
        name="Test Bank",
        description="Een test vragenbank",
        questions=[]
    )

    # Voeg vraag toe
    question = Question(
        id="q001",
        question_text="Test?",
        question_type=QuestionType.OPEN,
        difficulty=DifficultyLevel.MAKKELIJK,
        learning_objectives=[
            LearningObjective(id="lo-1", description="Test", category="test")
        ],
        correct_answer="test"
    )

    bank.add_question(question)
    assert len(bank.questions) == 1

    # Haal vraag op via ID
    found = bank.get_question_by_id("q001")
    assert found is not None
    assert found.id == "q001"

    # Haal vragen op via moeilijkheidsgraad
    easy_questions = bank.get_questions_by_difficulty(DifficultyLevel.MAKKELIJK)
    assert len(easy_questions) == 1
    assert easy_questions[0].difficulty == DifficultyLevel.MAKKELIJK


def test_difficulty_levels():
    """Test alle moeilijkheidsgraden."""
    levels = [
        DifficultyLevel.ZEER_MAKKELIJK,
        DifficultyLevel.MAKKELIJK,
        DifficultyLevel.GEMIDDELD,
        DifficultyLevel.MOEILIJK,
        DifficultyLevel.ZEER_MOEILIJK
    ]

    for level in levels:
        question = Question(
            id=f"q-{level.value}",
            question_text="Test",
            question_type=QuestionType.OPEN,
            difficulty=level,
            learning_objectives=[
                LearningObjective(id="lo-1", description="Test", category="test")
            ],
            correct_answer="test"
        )
        assert question.difficulty == level


def test_question_types():
    """Test alle vraagtypen."""
    types = [
        QuestionType.MEERKEUZE,
        QuestionType.OPEN,
        QuestionType.WAAR_ONWAAR,
        QuestionType.INVUL
    ]

    for qtype in types:
        question = Question(
            id=f"q-{qtype.value}",
            question_text="Test",
            question_type=qtype,
            difficulty=DifficultyLevel.GEMIDDELD,
            learning_objectives=[
                LearningObjective(id="lo-1", description="Test", category="test")
            ],
            correct_answer="test"
        )
        assert question.question_type == qtype
