#!/usr/bin/env python3
"""
Voorbeeld script voor het gebruik van ToetsGen als Python library.

Dit script demonstreert:
1. Het maken van een vragenbank
2. Het genereren van alternatieve vragen
3. Het analyseren van moeilijkheidsgraad
4. Het opslaan van resultaten
"""

from src import (
    Question,
    QuestionBank,
    QuestionType,
    DifficultyLevel,
    LearningObjective,
    Answer,
    QuestionGenerator,
    save_question_bank,
    save_generated_questions
)


def main():
    print("🎓 ToetsGen - Voorbeeld Script\n")

    # Stap 1: Maak een vragenbank
    print("📝 Stap 1: Vragenbank aanmaken...")

    questions = [
        Question(
            id="demo001",
            question_text="Wat is 25% van 80?",
            question_type=QuestionType.MEERKEUZE,
            difficulty=DifficultyLevel.MAKKELIJK,
            learning_objectives=[
                LearningObjective(
                    id="wiskunde-percentage-1",
                    description="Kan percentages berekenen",
                    category="rekenen"
                )
            ],
            answers=[
                Answer(text="15", is_correct=False),
                Answer(text="20", is_correct=True),
                Answer(text="25", is_correct=False),
                Answer(text="30", is_correct=False)
            ],
            explanation="25% van 80 = 0.25 × 80 = 20",
            tags=["percentage", "rekenen"]
        ),
        Question(
            id="demo002",
            question_text="Los op: x + 7 = 12",
            question_type=QuestionType.OPEN,
            difficulty=DifficultyLevel.MAKKELIJK,
            learning_objectives=[
                LearningObjective(
                    id="wiskunde-algebra-1",
                    description="Kan eenvoudige vergelijkingen oplossen",
                    category="algebra"
                )
            ],
            correct_answer="5",
            explanation="x = 12 - 7 = 5",
            hints=["Trek 7 af van beide kanten"],
            tags=["algebra", "vergelijkingen"]
        )
    ]

    question_bank = QuestionBank(
        name="Demo Vragenbank",
        description="Demonstratie vragenbank voor ToetsGen",
        questions=questions
    )

    print(f"✓ Vragenbank aangemaakt met {len(questions)} vragen\n")

    # Stap 2: Genereer alternatieven
    print("🤖 Stap 2: Alternatieve vragen genereren...")
    print("   (Dit kan een paar seconden duren...)\n")

    try:
        generator = QuestionGenerator()

        all_alternatives = []
        for question in question_bank.questions:
            print(f"   Genereren voor vraag: {question.id}")
            alternatives = generator.generate_alternative(
                question,
                num_alternatives=2,  # Genereer 2 alternatieven per vraag
                preserve_difficulty=True
            )
            all_alternatives.extend(alternatives)
            print(f"   ✓ {len(alternatives)} alternatieven gegenereerd")

        print(f"\n✓ Totaal {len(all_alternatives)} alternatieve vragen gegenereerd\n")

        # Toon voorbeelden
        print("📋 Voorbeelden van gegenereerde vragen:\n")
        for i, alt in enumerate(all_alternatives[:2], 1):  # Toon eerste 2
            print(f"   {i}. Originele vraag ID: {alt.original_question_id}")
            print(f"      Nieuwe vraag: {alt.generated_question.question_text[:80]}...")
            print(f"      Moeilijkheid: {alt.generated_question.difficulty.value}")
            print()

        # Stap 3: Analyseer moeilijkheidsgraad
        print("🔍 Stap 3: Moeilijkheidsgraad analyseren...\n")

        for question in questions[:1]:  # Analyseer alleen eerste vraag als voorbeeld
            print(f"   Analyseren van: {question.id}")
            analysis = generator.analyze_question_difficulty(question)

            print(f"   Gesteld: {analysis.get('stated_difficulty')}")
            print(f"   Beoordeeld: {analysis.get('assessed_difficulty')}")
            print(f"   Passend: {'Ja' if analysis.get('is_appropriate') else 'Nee'}")
            print()

        # Stap 4: Sla resultaten op
        print("💾 Stap 4: Resultaten opslaan...\n")

        save_question_bank(question_bank, "output/demo_vragenbank.json")
        print("   ✓ Vragenbank opgeslagen: output/demo_vragenbank.json")

        save_generated_questions(all_alternatives, "output/demo_alternatieven.json")
        print("   ✓ Alternatieven opgeslagen: output/demo_alternatieven.json")

        print("\n✅ Klaar! Bekijk de output/ directory voor de resultaten.")
        print("\n💡 Tip: Gebruik de CLI voor meer opties:")
        print("   python cli.py --help")

    except ValueError as e:
        if "API" in str(e):
            print("❌ Fout: API key niet gevonden!")
            print("\n📝 Om dit op te lossen:")
            print("   1. Kopieer .env.example naar .env")
            print("   2. Vul je API key in (.env bestand)")
            print("   3. Run dit script opnieuw")
            print("\nOf stel een environment variable in:")
            print("   export ANTHROPIC_API_KEY=your_key_here")
        else:
            print(f"❌ Fout: {e}")
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        print("\n💡 Zorg dat je een API key hebt geconfigureerd.")
        print("   Zie .env.example voor instructies.")


if __name__ == "__main__":
    main()
