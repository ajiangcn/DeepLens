# DeepLens

Looking deeply beyond the surface of research hype

## Overview

DeepLens is a multi-agent system built with flexible LLM provider support that helps researchers and practitioners cut through research hype and understand what's genuinely important. It provides four key capabilities:

1. **Translation**: Translates research buzzwords and papers into plain language
2. **Analysis**: Identifies fundamental problems, research stage (exploration/scaling/convergence), and industry demand
3. **Researcher Evaluation**: Evaluates a researcher's history to determine if they follow trends, go deep, or uplevel problem abstractions
4. **Trend Assessment**: Assesses technical trends — predicting obsolescence, distinguishing hype from hard problems, and detecting oversupply

## ✨ Features (v0.3.0)

- **🌐 Multi-Provider Support**: Works with OpenAI, Azure OpenAI, Anthropic, Google Gemini, Cohere, and more
- **🎨 Interactive Web UI**: Beautiful Gradio-based interface for easy interaction
- **💻 Rich Interactive CLI**: Enhanced terminal interface with colors and formatting
- **🔌 Extensible Architecture**: Easy-to-use plugin system for adding new agents
- **⚙️ Configuration Management**: Centralized configuration with agent-specific settings
- **🛡️ Better Error Handling**: Custom exceptions and improved error messages
- **🧰 Utility Functions**: Common formatting and validation helpers
- **✅ Comprehensive Testing**: 92.6% test coverage for core modules

## Architecture

DeepLens uses a modular multi-agent architecture with specialized agents:

- **TranslationAgent**: Simplifies research jargon and explains buzzwords
- **AnalysisAgent**: Analyzes research to identify core problems and maturity
- **ResearcherEvaluationAgent**: Evaluates researcher patterns (trend follower, deep specialist, abstraction upleveler)
- **TrendAssessmentAgent**: Assesses trends, detects hype, and predicts obsolescence

All agents use a flexible LLM provider layer (via LiteLLM) that supports 100+ LLM providers, coordinated by the `DeepLensOrchestrator`.

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

## Quick Start

### Web UI (Recommended)

Launch the interactive web interface:

```bash
python launch.py --ui
```

Or with a custom port:

```bash
python launch.py --ui --port 8080
```

The web UI provides:
- 🌐 **Translate**: Simplify research text and explain buzzwords
- 🔬 **Analyze**: Identify research stage and demand
- 👨‍🔬 **Evaluate**: Assess researcher patterns
- 📈 **Trends**: Detect hype and oversupply

### Interactive CLI

For terminal users, launch the interactive CLI:

```bash
python launch.py --cli
```

Features:
- Rich formatted output with colors
- Progress indicators
- Interactive prompts
- Easy command navigation

### Simple Launcher

Just run:

```bash
python launch.py
```

Choose your preferred interface from the menu.

## Usage

### As a Python Library

```python
import asyncio
from deeplens import DeepLensOrchestrator

async def main():
    # Initialize with OpenAI (default)
    orchestrator = DeepLensOrchestrator(
        provider="openai",
        model="gpt-4",
        api_key="your-key"  # Or set OPENAI_API_KEY in .env
    )
    
    # Or use Azure OpenAI
    orchestrator = DeepLensOrchestrator(
        provider="azure_openai",
        model="gpt-35-turbo",
        api_key="your-azure-key",
        api_base="https://your-resource.openai.azure.com",
        api_version="2023-05-15"
    )
    
    # Or use Anthropic Claude
    orchestrator = DeepLensOrchestrator(
        provider="anthropic",
        model="claude-3-opus",
        api_key="your-anthropic-key"
    )
    
    # Or use Google Gemini
    orchestrator = DeepLensOrchestrator(
        provider="gemini",
        model="gemini-pro",
        api_key="your-gemini-key"
    )
    
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

DeepLens uses LiteLLM to support 100+ LLM providers:

### OpenAI (Default)
```python
orchestrator = DeepLensOrchestrator(
    provider="openai",
    model="gpt-4",
    api_key="your-key"  # Or set OPENAI_API_KEY in .env
)
```

### Azure OpenAI
```python
orchestrator = DeepLensOrchestrator(
    provider="azure_openai",
    model="gpt-35-turbo",  # Your deployment name
    api_key="your-azure-key",
    api_base="https://your-resource.openai.azure.com",
    api_version="2023-05-15"
)
```

### Anthropic Claude
```python
orchestrator = DeepLensOrchestrator(
    provider="anthropic",
    model="claude-3-opus",
    api_key="your-anthropic-key"
)
```

### Google Gemini & Others
```python
# Google Gemini
orchestrator = DeepLensOrchestrator(
    provider="gemini",
    model="gemini-pro",
    api_key="your-gemini-key"
)

# Cohere
orchestrator = DeepLensOrchestrator(
    provider="cohere",
    model="command",
    api_key="your-cohere-key"
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

## Extending DeepLens

DeepLens is designed to be easily extensible. Add new agents in just a few lines:

```python
from deeplens.base_agent import BaseAgent
from deeplens.registry import register_agent

@register_agent("my_agent")
class MyAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """You are an expert at [domain]..."""
    
    async def analyze(self, content: str):
        result = await self.invoke_prompt(
            prompt=f"Analyze: {content}",
            function_name="analyze"
        )
        return {"result": result, "status": "success"}
```

See [EXTENDING.md](EXTENDING.md) for a complete guide on:
- Creating new agents
- Registering agents with the system
- Adding UI components
- Best practices for agent design

## Documentation

- **[README.md](README.md)** - Main documentation (this file)
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute getting started guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture details
- **[EXTENDING.md](EXTENDING.md)** - Guide to adding new agents
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines

## License

MIT License

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

To add a new agent:
1. Read [EXTENDING.md](EXTENDING.md)
2. Create your agent class inheriting from `BaseAgent`
3. Register it with `@register_agent("name")`
4. Add UI components and tests
5. Submit a PR!

## Support

For questions or issues, please open a GitHub issue.
