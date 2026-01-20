"""
Toetsvragen generator voor het maken van alternatieve vragen.
"""
import json
from typing import List, Optional
from .models import (
    Question,
    GeneratedQuestion,
    DifficultyLevel,
    QuestionType,
    LearningObjective,
    Answer
)
from .llm_client import LLMClient


class QuestionGenerator:
    """Generator voor alternatieve toetsvragen."""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialiseer de generator.

        Args:
            llm_client: Optionele LLM client. Maakt een nieuwe aan als None.
        """
        self.llm_client = llm_client or LLMClient()

    def generate_alternative(
        self,
        original_question: Question,
        num_alternatives: int = 1,
        preserve_difficulty: bool = True
    ) -> List[GeneratedQuestion]:
        """
        Genereer alternatieve versies van een vraag.

        Args:
            original_question: De originele vraag
            num_alternatives: Aantal alternatieven om te genereren
            preserve_difficulty: Of de moeilijkheidsgraad behouden moet blijven

        Returns:
            Lijst met gegenereerde alternatieve vragen
        """
        system_prompt = self._create_system_prompt()
        user_prompt = self._create_generation_prompt(
            original_question,
            num_alternatives,
            preserve_difficulty
        )

        generated_questions = []

        for i in range(num_alternatives):
            try:
                # Genereer alternatieve vraag
                response = self.llm_client.generate_json(
                    prompt=user_prompt,
                    system_prompt=system_prompt,
                    temperature=0.8  # Hogere temp voor meer variatie
                )

                # Parse de gegenereerde vraag
                generated_q = self._parse_generated_question(
                    response,
                    original_question
                )

                # Analyseer moeilijkheidsgraad
                if preserve_difficulty:
                    difficulty_analysis = self._analyze_difficulty(
                        original_question,
                        generated_q
                    )
                    generated_q.generation_metadata = {
                        "difficulty_preserved": difficulty_analysis["is_similar"],
                        "difficulty_reasoning": difficulty_analysis["reasoning"],
                        "iteration": i + 1
                    }

                generated_questions.append(generated_q)

            except Exception as e:
                print(f"Fout bij genereren alternatief {i+1}: {e}")
                continue

        return generated_questions

    def bulk_generate(
        self,
        questions: List[Question],
        alternatives_per_question: int = 3,
        preserve_difficulty: bool = True
    ) -> dict[str, List[GeneratedQuestion]]:
        """
        Genereer bulk alternatieven voor meerdere vragen.

        Args:
            questions: Lijst met originele vragen
            alternatives_per_question: Aantal alternatieven per vraag
            preserve_difficulty: Of moeilijkheidsgraad behouden moet blijven

        Returns:
            Dictionary met question_id -> lijst van alternatieven
        """
        results = {}

        for question in questions:
            print(f"Genereren van alternatieven voor vraag: {question.id}")
            alternatives = self.generate_alternative(
                question,
                num_alternatives=alternatives_per_question,
                preserve_difficulty=preserve_difficulty
            )
            results[question.id] = alternatives

        return results

    def _create_system_prompt(self) -> str:
        """Maak de system prompt voor de LLM."""
        return """Je bent een expert in het maken van toetsvragen voor educatieve doeleinden.
Je taak is om alternatieve versies van bestaande vragen te maken die:
1. Dezelfde leerdoelen testen
2. Een vergelijkbare moeilijkheidsgraad hebben
3. Variëren in formulering en context
4. Pedagogisch verantwoord zijn

Genereer ALLEEN de JSON output zonder extra uitleg."""

    def _create_generation_prompt(
        self,
        question: Question,
        num_alternatives: int,
        preserve_difficulty: bool
    ) -> str:
        """Maak de user prompt voor het genereren van alternatieven."""
        # Serialize de vraag naar JSON voor de prompt
        question_json = question.model_dump_json(indent=2)

        difficulty_instruction = ""
        if preserve_difficulty:
            difficulty_instruction = f"""
BELANGRIJK: De alternatieve vraag MOET dezelfde moeilijkheidsgraad hebben: {question.difficulty.value}
"""

        prompt = f"""Genereer 1 alternatieve versie van de volgende toetsvraag.

ORIGINELE VRAAG:
{question_json}

{difficulty_instruction}

INSTRUCTIES:
1. Behoud dezelfde leerdoelen exact
2. Behoud hetzelfde vraagtype
3. Maak een inhoudelijk andere vraag die dezelfde concepten test
4. Voor meerkeuzevragen: genereer nieuwe antwoordopties met dezelfde structuur
5. Zorg dat de vraag pedagogisch verantwoord is

OUTPUT FORMAT:
Geef de output als een JSON object met de volgende structuur:
{{
    "id": "nieuw_uniek_id",
    "question_text": "De nieuwe vraag",
    "question_type": "{question.question_type.value}",
    "difficulty": "{question.difficulty.value}",
    "learning_objectives": [/* zelfde als origineel */],
    "answers": [/* voor meerkeuze vragen */],
    "correct_answer": "/* voor open vragen */",
    "explanation": "Uitleg van het antwoord",
    "hints": [/* optionele hints */],
    "tags": [/* optionele tags */]
}}

Genereer NU de alternatieve vraag als JSON:"""

        return prompt

    def _parse_generated_question(
        self,
        response: dict,
        original_question: Question
    ) -> GeneratedQuestion:
        """Parse de LLM response naar een GeneratedQuestion object."""
        # Parse de vraag
        try:
            generated_q = Question(**response)
        except Exception as e:
            raise ValueError(f"Kon vraag niet parsen: {e}\nResponse: {response}")

        # Maak een GeneratedQuestion object
        return GeneratedQuestion(
            original_question_id=original_question.id,
            generated_question=generated_q,
            similarity_score=None,  # Kan later worden berekend
            generation_metadata={"raw_response": response}
        )

    def _analyze_difficulty(
        self,
        original: Question,
        generated: Question
    ) -> dict:
        """
        Analyseer of de gegenereerde vraag een vergelijkbare moeilijkheidsgraad heeft.

        Args:
            original: Originele vraag
            generated: Gegenereerde vraag

        Returns:
            Dictionary met analyse resultaten
        """
        analysis_prompt = f"""Analyseer of deze twee vragen een vergelijkbare moeilijkheidsgraad hebben.

ORIGINELE VRAAG:
Moeilijkheidsgraad: {original.difficulty.value}
Vraag: {original.question_text}

GEGENEREERDE VRAAG:
Moeilijkheidsgraad: {generated.difficulty.value}
Vraag: {generated.question_text}

Geef je analyse in JSON formaat:
{{
    "is_similar": true/false,
    "reasoning": "Uitleg waarom wel of niet vergelijkbaar",
    "original_difficulty": "{original.difficulty.value}",
    "generated_difficulty": "{generated.difficulty.value}"
}}"""

        try:
            response = self.llm_client.generate_json(
                prompt=analysis_prompt,
                temperature=0.3  # Lagere temp voor consistente analyse
            )
            return response
        except Exception as e:
            return {
                "is_similar": original.difficulty == generated.difficulty,
                "reasoning": f"Automatische vergelijking: {str(e)}",
                "original_difficulty": original.difficulty.value,
                "generated_difficulty": generated.difficulty.value
            }

    def analyze_question_difficulty(self, question: Question) -> dict:
        """
        Analyseer de moeilijkheidsgraad van een vraag en geef aanbevelingen.

        Args:
            question: De te analyseren vraag

        Returns:
            Dictionary met analyse en aanbevelingen
        """
        analysis_prompt = f"""Analyseer de moeilijkheidsgraad van deze toetsvraag in detail.

VRAAG:
{question.model_dump_json(indent=2)}

Geef een gedetailleerde analyse in JSON formaat:
{{
    "stated_difficulty": "{question.difficulty.value}",
    "assessed_difficulty": "je beoordeling (zeer_makkelijk/makkelijk/gemiddeld/moeilijk/zeer_moeilijk)",
    "difficulty_factors": [
        "Factor 1 die moeilijkheid beïnvloedt",
        "Factor 2 die moeilijkheid beïnvloedt"
    ],
    "is_appropriate": true/false,
    "reasoning": "Uitgebreide uitleg van je beoordeling",
    "recommendations": [
        "Aanbeveling 1 om vraag te verbeteren",
        "Aanbeveling 2"
    ]
}}"""

        try:
            response = self.llm_client.generate_json(
                prompt=analysis_prompt,
                temperature=0.3
            )
            return response
        except Exception as e:
            return {
                "error": str(e),
                "stated_difficulty": question.difficulty.value
            }
