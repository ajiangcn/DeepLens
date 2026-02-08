# DeepLens

Looking deeply beyond the surface of research hype

## Overview

DeepLens is a multi-agent system built with flexible LLM provider support that helps researchers and practitioners cut through research hype and understand what's genuinely important. It provides two core workflows:

1. **Understand Paper** — paste a paper link (arXiv, DOI, Semantic Scholar, or any URL) and get a plain-language summary plus research-stage analysis
2. **Evaluate Researcher** — paste a Google Scholar profile URL and get a classification of the researcher's strategy (trend follower, deep specialist, or abstraction upleveler)

## ✨ Features

- **🔗 Link-Based Input**: Just paste a URL — no data wrangling required
- **🌐 Multi-Provider Support**: Works with OpenAI, Azure OpenAI, Anthropic, Google Gemini, Cohere, and more via LiteLLM
- **🎨 Interactive Web UI**: Clean two-tab Gradio interface
- **💻 Rich Interactive CLI**: Terminal interface with rich formatting
- **🔌 Extensible Architecture**: Plugin system for adding new agents
- **🔐 Azure AD Auth**: DefaultAzureCredential for Azure OpenAI (no API keys)

## Installation

```bash
git clone https://github.com/ajiangcn/DeepLens.git
cd DeepLens
pip install -r requirements.txt
```

Set up your `.env` file:

```env
# For Azure OpenAI (recommended — uses DefaultAzureCredential, no API key needed)
USE_AZURE=true
AZURE_API_BASE=https://your-resource.cognitiveservices.azure.com/
AZURE_API_VERSION=2024-12-01-preview
OPENAI_MODEL=gpt-4

# Or for vanilla OpenAI
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4
```

## Quick Start

### Web UI (Recommended)

```bash
python launch.py --ui
```

Two tabs:
- **📄 Understand Paper** — paste a paper link or text
- **👨‍🔬 Evaluate Researcher** — paste a Google Scholar profile URL

### Interactive CLI

```bash
python launch.py --cli
```

Commands: `paper`, `researcher`, `help`, `exit`

### Direct CLI

```bash
# Understand a paper from an arXiv link
python main.py paper "https://arxiv.org/abs/2301.07041"

# Understand a paper from a local file
python main.py paper --file paper.txt

# Evaluate a researcher from Google Scholar
python main.py researcher "https://scholar.google.com/citations?user=XXXXXXXX"

# JSON output
python main.py --json paper "https://arxiv.org/abs/2301.07041"
```

### As a Python Library

```python
import asyncio
from deeplens import DeepLensOrchestrator

async def main():
    orchestrator = DeepLensOrchestrator(
        provider="azure_openai",
        model="gpt-4",
        api_base="https://your-resource.cognitiveservices.azure.com/",
        api_version="2024-12-01-preview",
    )
    
    # Workflow 1: Understand a paper
    result = await orchestrator.understand_paper("https://arxiv.org/abs/2301.07041")
    print(result["translation"]["simplified"])
    print(result["analysis"]["analysis"])
    
    # Workflow 2: Evaluate a researcher
    result = await orchestrator.evaluate_researcher_from_url(
        "https://scholar.google.com/citations?user=XXXXXXXX"
    )
    print(result["name"], "—", result["evaluation"]["evaluation"])

asyncio.run(main())
```

## Architecture

DeepLens uses a modular multi-agent system coordinated by the `DeepLensOrchestrator`.
Users interact through **workflows** — the agents are internal implementation details:

| User Workflow | Internal Agents Used |
|---|---|
| Understand Paper | TranslationAgent → AnalysisAgent |
| Evaluate Researcher | (scraper) → ResearcherEvaluationAgent |

Key components:
- `deeplens/scraper.py` — Fetches papers (arXiv, Semantic Scholar, DOI, generic) and Google Scholar profiles
- `deeplens/orchestrator.py` — Maps user workflows to agent calls
- `deeplens/agents/` — Specialized LLM agents (translation, analysis, researcher evaluation)
- `deeplens/llm_provider.py` — LiteLLM-based provider with Azure AD token support
- `specs/` — Speckit workflow specifications

## Configuration

DeepLens uses LiteLLM to support 100+ LLM providers. See `.env` for configuration.

For Azure OpenAI, authentication is handled via `DefaultAzureCredential` (supports `az login`, managed identity, service principal, etc.) — no API key needed.

## Philosophy

DeepLens is designed with a contrarian, skeptical lens:
- **Call out hype**: Distinguish marketing from substance
- **Identify fundamentals**: Look past buzzwords to real problems
- **Think long-term**: Predict what will matter in 5-10 years
- **Just paste a link**: No data wrangling — the system handles fetching

## Documentation

- [QUICKSTART.md](QUICKSTART.md) — 5-minute getting started guide
- [ARCHITECTURE.md](ARCHITECTURE.md) — Technical architecture details
- [EXTENDING.md](EXTENDING.md) — Guide to adding new agents
- [CONTRIBUTING.md](CONTRIBUTING.md) — Contribution guidelines
- [UI_GUIDE.md](UI_GUIDE.md) — Web UI guide

## License

MIT License
