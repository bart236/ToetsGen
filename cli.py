#!/usr/bin/env python3
"""
Command-line interface voor ToetsGen.
"""
import click
import json
from pathlib import Path
from src import (
    QuestionGenerator,
    load_questions_from_json,
    load_question_bank,
    save_questions_to_json,
    save_generated_questions,
    create_example_question_bank,
    save_question_bank,
    settings
)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """ToetsGen - Genereer alternatieve toetsvragen met AI."""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output bestand voor gegenereerde vragen"
)
@click.option(
    "--num-alternatives",
    "-n",
    default=3,
    type=int,
    help="Aantal alternatieven per vraag (default: 3)"
)
@click.option(
    "--preserve-difficulty/--no-preserve-difficulty",
    default=True,
    help="Behoud moeilijkheidsgraad (default: aan)"
)
@click.option(
    "--provider",
    type=click.Choice(["anthropic", "openai"]),
    help="LLM provider (default: uit .env)"
)
def generate(input_file, output, num_alternatives, preserve_difficulty, provider):
    """Genereer alternatieve vragen uit een JSON bestand."""
    click.echo(f"📚 Laden van vragen uit: {input_file}")

    try:
        # Laad vragen
        questions = load_questions_from_json(input_file)
        click.echo(f"✓ {len(questions)} vragen geladen")

        # Maak generator
        from src.llm_client import LLMClient
        llm_client = LLMClient(provider=provider) if provider else None
        generator = QuestionGenerator(llm_client=llm_client)

        # Genereer alternatieven
        click.echo(f"\n🤖 Genereren van {num_alternatives} alternatieven per vraag...")
        click.echo(f"   Provider: {generator.llm_client.provider}")
        click.echo(f"   Model: {generator.llm_client.model}")

        all_generated = []
        with click.progressbar(
            questions,
            label="Genereren",
            item_show_func=lambda q: q.id if q else ""
        ) as bar:
            for question in bar:
                alternatives = generator.generate_alternative(
                    question,
                    num_alternatives=num_alternatives,
                    preserve_difficulty=preserve_difficulty
                )
                all_generated.extend(alternatives)

        click.echo(f"\n✓ {len(all_generated)} alternatieve vragen gegenereerd")

        # Sla op
        if output:
            output_path = Path(output)
        else:
            input_path = Path(input_file)
            output_path = input_path.parent / f"{input_path.stem}_generated.json"

        save_generated_questions(all_generated, output_path)
        click.echo(f"✓ Opgeslagen naar: {output_path}")

    except Exception as e:
        click.echo(f"❌ Fout: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--question-id",
    "-q",
    help="Specifieke vraag ID om te analyseren"
)
def analyze(input_file, question_id):
    """Analyseer de moeilijkheidsgraad van vragen."""
    click.echo(f"📚 Laden van vragen uit: {input_file}")

    try:
        questions = load_questions_from_json(input_file)

        if question_id:
            questions = [q for q in questions if q.id == question_id]
            if not questions:
                click.echo(f"❌ Vraag met ID '{question_id}' niet gevonden", err=True)
                raise click.Abort()

        click.echo(f"✓ {len(questions)} vragen gevonden\n")

        generator = QuestionGenerator()

        for question in questions:
            click.echo(f"🔍 Analyseren van vraag: {question.id}")
            click.echo(f"   Vraag: {question.question_text[:80]}...")

            analysis = generator.analyze_question_difficulty(question)

            click.echo(f"\n   Gestelde moeilijkheidsgraad: {analysis.get('stated_difficulty')}")
            click.echo(f"   Beoordeelde moeilijkheidsgraad: {analysis.get('assessed_difficulty')}")
            click.echo(f"   Passend: {'Ja' if analysis.get('is_appropriate') else 'Nee'}")
            click.echo(f"\n   Redenering:")
            click.echo(f"   {analysis.get('reasoning', 'Geen redenering beschikbaar')}")

            if analysis.get('recommendations'):
                click.echo(f"\n   Aanbevelingen:")
                for rec in analysis['recommendations']:
                    click.echo(f"   - {rec}")

            click.echo("\n" + "-" * 80 + "\n")

    except Exception as e:
        click.echo(f"❌ Fout: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("output_file", type=click.Path())
def create_example(output_file):
    """Maak een voorbeeld vragenbank."""
    click.echo("📝 Aanmaken van voorbeeld vragenbank...")

    try:
        question_bank = create_example_question_bank()
        save_question_bank(question_bank, output_file)

        click.echo(f"✓ Voorbeeld vragenbank aangemaakt met {len(question_bank.questions)} vragen")
        click.echo(f"✓ Opgeslagen naar: {output_file}")
        click.echo("\nJe kunt nu alternatieven genereren met:")
        click.echo(f"  python cli.py generate {output_file}")

    except Exception as e:
        click.echo(f"❌ Fout: {e}", err=True)
        raise click.Abort()


@cli.command()
def check_config():
    """Controleer de configuratie."""
    click.echo("⚙️  Configuratie controle:\n")

    click.echo(f"Provider: {settings.default_llm_provider}")
    click.echo(f"Model (Anthropic): {settings.anthropic_model}")
    click.echo(f"Model (OpenAI): {settings.openai_model}")
    click.echo(f"Temperature: {settings.temperature}")
    click.echo(f"Max tokens: {settings.max_tokens}")

    click.echo("\nAPI Keys:")
    if settings.anthropic_api_key:
        click.echo(f"✓ Anthropic API key ingesteld")
    else:
        click.echo(f"✗ Anthropic API key NIET ingesteld")

    if settings.openai_api_key:
        click.echo(f"✓ OpenAI API key ingesteld")
    else:
        click.echo(f"✗ OpenAI API key NIET ingesteld")

    click.echo("\nOm API keys in te stellen:")
    click.echo("  1. Kopieer .env.example naar .env")
    click.echo("  2. Vul je API keys in")
    click.echo("  3. Of stel environment variables in")


if __name__ == "__main__":
    cli()
