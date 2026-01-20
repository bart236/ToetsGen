# Quick Start Guide

Snel aan de slag met ToetsGen in 5 minuten!

## Stap 1: Installatie

```bash
# Clone de repository
git clone <repository-url>
cd ToetsGen

# Maak virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installeer dependencies
pip install -r requirements.txt
```

## Stap 2: API Key Configureren

```bash
# Kopieer voorbeeld config
cp .env.example .env

# Bewerk .env en voeg je API key toe
# Voor Anthropic (Claude):
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_LLM_PROVIDER=anthropic

# OF voor OpenAI:
OPENAI_API_KEY=sk-...
DEFAULT_LLM_PROVIDER=openai
```

## Stap 3: Maak Voorbeeld Vragen

```bash
# Genereer een voorbeeld vragenbank
python cli.py create-example examples/demo.json
```

Dit maakt een bestand aan met 3 voorbeeld vragen over verschillende onderwerpen.

## Stap 4: Genereer Alternatieven

```bash
# Genereer 3 alternatieven voor elke vraag
python cli.py generate examples/demo.json
```

Of gebruik de vooraf gemaakte voorbeelden:

```bash
# Genereer alternatieven voor wiskunde vragen
python cli.py generate examples/wiskunde_vragen.json -n 3

# Genereer alternatieven voor geschiedenis vragen
python cli.py generate examples/geschiedenis_vragen.json -n 3
```

## Stap 5: Bekijk Resultaten

De gegenereerde vragen worden opgeslagen in een nieuw bestand met `_generated` in de naam.

```bash
# Bijvoorbeeld:
cat examples/wiskunde_vragen_generated.json
```

## Bonus: Analyseer Moeilijkheidsgraad

```bash
# Analyseer hoe moeilijk de vragen zijn
python cli.py analyze examples/wiskunde_vragen.json
```

## Je Eigen Vragen Gebruiken

Maak een JSON bestand met je eigen vragen:

```json
{
  "name": "Mijn Vragenbank",
  "questions": [
    {
      "id": "q001",
      "question_text": "Jouw vraag hier?",
      "question_type": "meerkeuze",
      "difficulty": "gemiddeld",
      "learning_objectives": [
        {
          "id": "lo-1",
          "description": "Wat moet de student leren",
          "category": "categorie"
        }
      ],
      "answers": [
        {"text": "Optie A", "is_correct": false},
        {"text": "Optie B", "is_correct": true},
        {"text": "Optie C", "is_correct": false}
      ],
      "explanation": "Uitleg van het antwoord"
    }
  ]
}
```

Genereer dan alternatieven:

```bash
python cli.py generate jouw_vragen.json
```

## Hulp Nodig?

```bash
# Bekijk alle commando's
python cli.py --help

# Hulp voor een specifiek commando
python cli.py generate --help

# Controleer je configuratie
python cli.py check-config
```

## Volgende Stappen

- Lees de volledige [README.md](README.md) voor geavanceerde features
- Bekijk de [voorbeelden](examples/) voor inspiratie
- Pas de configuratie aan in `.env` voor custom instellingen

Veel succes met het genereren van toetsvragen! 🎓
