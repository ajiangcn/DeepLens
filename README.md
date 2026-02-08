# DeepLens

Looking deeply beyond the surface of research hype

## Overview

DeepLens is a multi-agent system built on the Microsoft Semantic Kernel framework that helps researchers and practitioners cut through research hype and understand what's genuinely important. It provides four key capabilities:

1. **Translation**: Translates research buzzwords and papers into plain language
2. **Analysis**: Identifies fundamental problems, research stage (exploration/scaling/convergence), and industry demand
3. **Researcher Evaluation**: Evaluates a researcher's history to determine if they follow trends, go deep, or uplevel problem abstractions
4. **Trend Assessment**: Assesses technical trends — predicting obsolescence, distinguishing hype from hard problems, and detecting oversupply

## Architecture

DeepLens uses a multi-agent architecture with specialized agents:

- **TranslationAgent**: Simplifies research jargon and explains buzzwords
- **AnalysisAgent**: Analyzes research to identify core problems and maturity
- **ResearcherEvaluationAgent**: Evaluates researcher patterns (trend follower, deep specialist, abstraction upleveler)
- **TrendAssessmentAgent**: Assesses trends, detects hype, and predicts obsolescence

All agents are coordinated by the `DeepLensOrchestrator`.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ajiangcn/DeepLens.git
cd DeepLens
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### As a Python Library

```python
import asyncio
from deeplens import DeepLensOrchestrator

async def main():
    # Initialize the orchestrator
    orchestrator = DeepLensOrchestrator()
    
    # Translate a buzzword
    result = await orchestrator.explain_buzzword("transformer architecture")
    print(result['explanation'])
    
    # Analyze a research paper
    paper = "We propose a novel approach to few-shot learning..."
    result = await orchestrator.analyze_research_paper(paper)
    print(result['translation']['simplified'])
    print(result['analysis']['analysis'])
    
    # Evaluate a researcher
    publications = [
        {"year": 2020, "title": "Paper 1", "abstract": "..."},
        {"year": 2021, "title": "Paper 2", "abstract": "..."}
    ]
    result = await orchestrator.evaluate_researcher(publications)
    print(result['evaluation'])
    
    # Assess a trend
    result = await orchestrator.assess_trend("Large Language Models")
    print(result['assessment'])

asyncio.run(main())
```

### Command-Line Interface

```bash
# Translate a buzzword
python main.py translate --buzzword "transformer architecture"

# Analyze a research paper
python main.py analyze --file paper.txt

# Evaluate a researcher (requires JSON file with publications)
python main.py evaluate --publications researcher.json

# Assess a trend
python main.py trend "Large Language Models"

# Detect oversupply in a research area
python main.py trend "BERT fine-tuning" --oversupply

# Get JSON output
python main.py translate "attention mechanism" --json
```

### Running Examples

```bash
python examples.py
```

This will run through examples of all four agents. Make sure you have set your `OPENAI_API_KEY` in the `.env` file first.

## Agent Capabilities

### 1. TranslationAgent

Translates technical research language into plain English:
- Identifies and explains technical jargon
- Breaks down complex concepts
- Provides analogies and examples
- Distinguishes genuinely novel concepts from rebranded ideas

**Example:**
```python
result = await orchestrator.explain_buzzword("attention mechanism")
```

### 2. AnalysisAgent

Identifies core problems and research maturity:
- Extracts fundamental problems (beyond surface claims)
- Classifies research stage:
  - **Exploration**: New problem space
  - **Scaling**: Proven concept, needs efficiency
  - **Convergence**: Mature field, incremental improvements
- Assesses real industry demand vs. academic interest

**Example:**
```python
result = await orchestrator.analyze_research_paper(paper_text)
```

### 3. ResearcherEvaluationAgent

Evaluates researcher strategies:
- **Trend Follower**: Jumps between hot topics
- **Deep Specialist**: Sustained focus on core problems
- **Abstraction Upleveler**: Progressively tackles more fundamental problems

**Example:**
```python
publications = [
    {"year": 2020, "title": "...", "abstract": "..."},
    {"year": 2021, "title": "...", "abstract": "..."}
]
result = await orchestrator.evaluate_researcher(publications)
```

### 4. TrendAssessmentAgent

Assesses technical trends with a critical lens:
- Predicts obsolescence and timelines
- Distinguishes hype from genuinely hard problems
- Detects oversupply (too many researchers on similar problems)
- Identifies fundamental vs. engineering challenges

**Example:**
```python
result = await orchestrator.assess_trend("Large Language Models")
# Or detect oversupply
result = await orchestrator.detect_oversupply("BERT fine-tuning", recent_papers)
```

## Configuration

DeepLens supports both OpenAI and Azure OpenAI:

### OpenAI (Default)
```python
orchestrator = DeepLensOrchestrator(
    api_key="your-key",  # Or set OPENAI_API_KEY in .env
    model="gpt-4"
)
```

### Azure OpenAI (Coming Soon)
```python
orchestrator = DeepLensOrchestrator(
    use_azure=True
    # Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT in .env
)
```

## Input Formats

### Researcher Publications JSON
```json
{
  "researcher_name": "Dr. Example",
  "publications": [
    {
      "year": 2020,
      "title": "Paper Title",
      "abstract": "Paper abstract..."
    }
  ]
}
```

### Recent Papers JSON (for oversupply detection)
```json
[
  {
    "title": "Paper Title",
    "year": 2023
  }
]
```

## Requirements

- Python 3.8+
- OpenAI API key (GPT-4 recommended)
- See `requirements.txt` for Python package dependencies

## Philosophy

DeepLens is designed with a contrarian, skeptical lens:
- **Call out hype**: Distinguish marketing from substance
- **Identify fundamentals**: Look past buzzwords to real problems
- **Think long-term**: Predict what will matter in 5-10 years
- **Be honest**: Acknowledge oversupply and diminishing returns

The system is optimized for researchers who want to:
- Understand what problems truly matter
- Avoid crowded research areas
- Work on genuinely difficult challenges
- See through academic and commercial hype

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or PR.

## Support

For questions or issues, please open a GitHub issue.
