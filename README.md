# ToetsGen

Een intelligente toetsgenerator die op basis van bestaande toetsvragen alternatieve vragen genereert met vergelijkbare moeilijkheidsgraad en dezelfde leerdoelen.

## Features

- **Alternatieve vragen genereren**: Genereer automatisch variaties van bestaande vragen die dezelfde concepten testen
- **Moeilijkheidsgraad analyse**: Automatisch analyseren en matchen van moeilijkheidsgraad
- **Bulk generatie**: Genereer meerdere alternatieven voor vele vragen tegelijk
- **Multiple LLM providers**: Ondersteunt zowel Anthropic (Claude) als OpenAI (GPT)
- **JSON opslag**: Eenvoudig te beheren vragenbanken in JSON formaat
- **CLI interface**: Gebruiksvriendelijke command-line interface
- **Type-safe**: Volledig getypeerd met Pydantic modellen

## Installatie

### Vereisten

- Python 3.10 of hoger
- API key voor Anthropic of OpenAI

### Stappen

1. **Clone de repository**

```bash
git clone <repository-url>
cd ToetsGen
```

2. **Maak een virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Op Windows: venv\Scripts\activate
```

3. **Installeer dependencies**

```bash
pip install -r requirements.txt
```

4. **Configureer API keys**

Kopieer het voorbeeld configuratie bestand:

```bash
cp .env.example .env
```

Bewerk `.env` en vul je API key in:

```env
# Voor Anthropic (Claude)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEFAULT_LLM_PROVIDER=anthropic

# OF voor OpenAI
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_LLM_PROVIDER=openai
```

## Gebruik

### CLI Commands

#### 1. Maak een voorbeeld vragenbank

```bash
python cli.py create-example examples/mijn_vragen.json
```

Dit maakt een voorbeeld vragenbank aan met verschillende typen vragen.

#### 2. Genereer alternatieve vragen

```bash
python cli.py generate examples/wiskunde_vragen.json
```

Opties:
- `-n, --num-alternatives`: Aantal alternatieven per vraag (default: 3)
- `-o, --output`: Output bestand (default: `{input}_generated.json`)
- `--preserve-difficulty/--no-preserve-difficulty`: Behoud moeilijkheidsgraad (default: aan)
- `--provider`: Kies LLM provider (`anthropic` of `openai`)

Voorbeeld met opties:

```bash
python cli.py generate examples/wiskunde_vragen.json \
  --num-alternatives 5 \
  --output output/nieuwe_vragen.json \
  --provider anthropic
```

#### 3. Analyseer moeilijkheidsgraad

```bash
python cli.py analyze examples/wiskunde_vragen.json
```

Analyseer een specifieke vraag:

```bash
python cli.py analyze examples/wiskunde_vragen.json --question-id wisk001
```

#### 4. Controleer configuratie

```bash
python cli.py check-config
```

### Python API

Je kunt ToetsGen ook gebruiken als Python library:

```python
from src import (
    QuestionGenerator,
    load_questions_from_json,
    save_generated_questions
)

# Laad vragen
questions = load_questions_from_json("examples/wiskunde_vragen.json")

# Maak generator
generator = QuestionGenerator()

# Genereer alternatieven
for question in questions:
    alternatives = generator.generate_alternative(
        question,
        num_alternatives=3,
        preserve_difficulty=True
    )

    for alt in alternatives:
        print(f"Origineel: {question.question_text}")
        print(f"Alternatief: {alt.generated_question.question_text}")
        print("---")

# Sla gegenereerde vragen op
save_generated_questions(alternatives, "output/alternatieven.json")
```

### Bulk generatie

```python
from src import QuestionGenerator, load_questions_from_json

questions = load_questions_from_json("examples/wiskunde_vragen.json")
generator = QuestionGenerator()

# Genereer voor alle vragen tegelijk
results = generator.bulk_generate(
    questions,
    alternatives_per_question=3,
    preserve_difficulty=True
)

# results is een dict: {question_id: [list van alternatieven]}
for question_id, alternatives in results.items():
    print(f"\nVraag {question_id}: {len(alternatives)} alternatieven gegenereerd")
```

## Data Structuur

### Vraag Format

```json
{
  "id": "q001",
  "question_text": "Wat is de hoofdstad van Nederland?",
  "question_type": "meerkeuze",
  "difficulty": "makkelijk",
  "learning_objectives": [
    {
      "id": "geo-nl-1",
      "description": "Kan de hoofdstad van Nederland noemen",
      "category": "geografie"
    }
  ],
  "answers": [
    {
      "text": "Amsterdam",
      "is_correct": true,
      "explanation": "Amsterdam is de hoofdstad volgens de grondwet"
    },
    {
      "text": "Den Haag",
      "is_correct": false
    }
  ],
  "explanation": "Amsterdam is de officiële hoofdstad van Nederland",
  "hints": ["Hint 1", "Hint 2"],
  "tags": ["geografie", "nederland"]
}
```

### Vraagtypen

- `meerkeuze`: Meerkeuze vraag met meerdere antwoordopties
- `open`: Open vraag met een tekstueel antwoord
- `waar_onwaar`: Waar/onwaar vraag
- `invul`: Invulvraag

### Moeilijkheidsgraden

- `zeer_makkelijk`
- `makkelijk`
- `gemiddeld`
- `moeilijk`
- `zeer_moeilijk`

### Vragenbank Format

```json
{
  "name": "Wiskunde Vragenbank",
  "description": "Vragen over verschillende wiskunde onderwerpen",
  "questions": [
    // ... array van vragen
  ]
}
```

## Voorbeelden

De `examples/` directory bevat voorbeeld vragenbanken:

- `wiskunde_vragen.json`: Wiskunde vragen over verschillende onderwerpen
- `geschiedenis_vragen.json`: Nederlandse en wereldgeschiedenis

## Testing

Run de tests met pytest:

```bash
pytest tests/
```

Run tests met coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## Project Structuur

```
ToetsGen/
├── src/
│   ├── __init__.py          # Package exports
│   ├── models.py            # Data modellen (Question, QuestionBank, etc.)
│   ├── config.py            # Configuratie en settings
│   ├── llm_client.py        # LLM API wrapper
│   ├── generator.py         # Vraag generator logica
│   └── utils.py             # Utility functies (laden/opslaan)
├── tests/
│   ├── __init__.py
│   ├── test_models.py       # Tests voor data modellen
│   └── test_utils.py        # Tests voor utilities
├── examples/
│   ├── wiskunde_vragen.json
│   └── geschiedenis_vragen.json
├── cli.py                   # Command-line interface
├── requirements.txt         # Python dependencies
├── .env.example            # Voorbeeld configuratie
├── .gitignore
└── README.md
```

## Geavanceerd Gebruik

### Custom LLM Settings

Je kunt de LLM instellingen aanpassen in `.env`:

```env
# Temperature (0.0 - 2.0): hogere waarden = meer creativiteit
TEMPERATURE=0.7

# Max tokens voor response
MAX_TOKENS=2000

# Model selectie
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
OPENAI_MODEL=gpt-4-turbo-preview
```

### Programmatisch gebruik met custom settings

```python
from src.config import settings
from src.llm_client import LLMClient
from src.generator import QuestionGenerator

# Pas settings aan
settings.temperature = 0.9
settings.max_tokens = 3000

# Maak custom client
llm_client = LLMClient(provider="anthropic")
generator = QuestionGenerator(llm_client=llm_client)

# Gebruik de generator
alternatives = generator.generate_alternative(question)
```

### Moeilijkheidsgraad analyse

```python
from src import QuestionGenerator, load_questions_from_json

questions = load_questions_from_json("examples/wiskunde_vragen.json")
generator = QuestionGenerator()

for question in questions:
    analysis = generator.analyze_question_difficulty(question)

    print(f"Vraag: {question.id}")
    print(f"Gestelde moeilijkheid: {analysis['stated_difficulty']}")
    print(f"Geanalyseerde moeilijkheid: {analysis['assessed_difficulty']}")
    print(f"Passend: {analysis['is_appropriate']}")
    print(f"Redenering: {analysis['reasoning']}")
    print("---")
```

## Tips voor Beste Resultaten

1. **Gedetailleerde leerdoelen**: Hoe specifieker je leerdoelen, hoe beter de gegenereerde alternatieven
2. **Goede voorbeelden**: Start met duidelijke, goed geformuleerde vragen
3. **Consistente moeilijkheidsgraad**: Zorg dat de moeilijkheidsgraad van originele vragen accuraat is ingesteld
4. **Review gegenereerde vragen**: AI-gegenereerde vragen moeten altijd handmatig gecontroleerd worden
5. **Iteratief verbeteren**: Gebruik de `analyze` command om vragen te verbeteren

## Veelgestelde Vragen

**Q: Welke LLM provider moet ik gebruiken?**
A: Beide werken goed. Anthropic (Claude) is vaak beter in het begrijpen van Nederlandse tekst en het volgen van instructies. OpenAI (GPT) kan iets sneller zijn.

**Q: Kan ik dit offline gebruiken?**
A: Nee, ToetsGen vereist een internet connectie om de LLM API's te benaderen.

**Q: Hoe kan ik de kwaliteit van gegenereerde vragen verbeteren?**
A: Zorg voor duidelijke, goed gestructureerde originele vragen met specifieke leerdoelen. Gebruik de `analyze` functie om vragen te evalueren.

**Q: Kan ik meerdere vragenbanken combineren?**
A: Ja, je kunt vragen uit meerdere bestanden laden en samenvoegen in Python:

```python
from src import load_questions_from_json

vragen1 = load_questions_from_json("bank1.json")
vragen2 = load_questions_from_json("bank2.json")
alle_vragen = vragen1 + vragen2
```

## Licentie

[Voeg hier je licentie informatie toe]

## Contributing

Bijdragen zijn welkom! Open een issue of pull request.

## Support

Voor vragen of problemen, open een issue op GitHub.
