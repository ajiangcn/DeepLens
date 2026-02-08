# DeepLens Project Constitution

## Core Principles

1. **User-Workflow First**: Organize features around what users want to DO, not around internal agents
2. **Skeptical Lens**: Always prioritize honesty over hype — call out overhyped research
3. **Single Interaction**: Users should get complete results without knowing about internal agents
4. **Multi-Provider**: Support any LLM provider via LiteLLM — never lock into one vendor

## Technology Constraints

- Language: Python 3.8+
- LLM Layer: LiteLLM (unified interface for 100+ providers)
- Auth: Azure DefaultAzureCredential for Azure OpenAI (no API keys)
- Web UI: Gradio
- CLI: Rich (interactive terminal)
- Testing: pytest with pytest-asyncio
- Config: python-dotenv (.env files)

## Architecture

- `deeplens/` — core library (agents, orchestrator, config, LLM provider)
- `specs/` — user workflow specifications (speckit format)
- `.specify/` — speckit templates and project memory
- Agents are **internal implementation details** — users interact through workflows
- The orchestrator maps user workflows to agent calls

## Quality Standards

- All workflows must have specifications in `specs/`
- All new features start with a spec before implementation
- Tests must cover core orchestrator and agent logic
- Error messages must be user-friendly (no agent internals exposed)

## Recent Decisions

### 2026-02-08: Azure OpenAI Auth
- Using DefaultAzureCredential instead of API keys
- Supports az login, managed identity, environment variables
- No AZURE_API_KEY needed in .env

### 2026-02-08: Speckit Workflow Organization
- Adopted speckit-style specifications for defining user workflows
- Workflows organized by user intent, not by agent
- Three initial workflows: Understand Paper, Evaluate Researcher, Assess Trend

### 2026-02-08: Two-Function UX
- Simplified the entire UX to just two user workflows:
  1. **Understand Paper** — paste a paper link (arXiv, DOI, …) or raw text
  2. **Evaluate Researcher** — paste a Google Scholar profile URL
- Removed the trend assessment workflow (specs/003 deleted)
- Added `deeplens/scraper.py` for web scraping (papers + Google Scholar)
- Added `beautifulsoup4` dependency
- UI: 2 Gradio tabs instead of 4
- CLI: `paper` and `researcher` commands instead of 6 commands
- main.py: `paper` and `researcher` subcommands
