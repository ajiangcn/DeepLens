# DeepLens Quick Start Guide

Get started with DeepLens in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/ajiangcn/DeepLens.git
cd DeepLens

# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Your First Analysis

### Example 1: Explain a Buzzword

```python
import asyncio
from deeplens import DeepLensOrchestrator

async def main():
    orchestrator = DeepLensOrchestrator()
    result = await orchestrator.explain_buzzword("attention mechanism")
    print(result['explanation'])

asyncio.run(main())
```

### Example 2: Analyze a Research Paper

```python
import asyncio
from deeplens import DeepLensOrchestrator

async def main():
    paper = """
    We propose a novel neural architecture that combines 
    transformers with graph neural networks for molecular 
    property prediction...
    """
    
    orchestrator = DeepLensOrchestrator()
    result = await orchestrator.analyze_research_paper(
        paper,
        include_translation=True,
        include_analysis=True
    )
    
    print("Plain Language:")
    print(result['translation']['simplified'])
    print("\nAnalysis:")
    print(result['analysis']['analysis'])

asyncio.run(main())
```

### Example 3: Evaluate a Researcher

```python
import asyncio
from deeplens import DeepLensOrchestrator

async def main():
    publications = [
        {
            "year": 2020,
            "title": "Deep Learning for Computer Vision",
            "abstract": "We apply CNNs to image classification..."
        },
        {
            "year": 2021,
            "title": "Transformers for NLP",
            "abstract": "We apply transformers to text generation..."
        },
        {
            "year": 2022,
            "title": "Graph Neural Networks",
            "abstract": "We apply GNNs to social networks..."
        }
    ]
    
    orchestrator = DeepLensOrchestrator()
    result = await orchestrator.evaluate_researcher(publications)
    print(result['evaluation'])

asyncio.run(main())
```

### Example 4: Assess a Trend

```python
import asyncio
from deeplens import DeepLensOrchestrator

async def main():
    orchestrator = DeepLensOrchestrator()
    result = await orchestrator.assess_trend("Large Language Models")
    print(result['assessment'])

asyncio.run(main())
```

## Using the CLI

DeepLens also provides a command-line interface:

```bash
# Explain a buzzword
python main.py translate --buzzword "transformer architecture"

# Analyze a research paper
python main.py analyze --file example_data/sample_paper.txt

# Evaluate a researcher
python main.py evaluate example_data/researcher_publications.json

# Assess a trend
python main.py trend "Large Language Models"

# Detect oversupply
python main.py trend "BERT fine-tuning" --oversupply --papers example_data/recent_papers.json

# Get JSON output
python main.py translate "attention mechanism" --json
```

## Running Examples

We provide a comprehensive examples file:

```bash
python examples.py
```

This will run through all four agents with sample data.

## Common Use Cases

### 1. Understanding New Research Areas
Use TranslationAgent and AnalysisAgent together:
```python
result = await orchestrator.analyze_research_paper(paper_text)
```

### 2. Deciding Where to Focus Research
Use TrendAssessmentAgent to identify undersupplied areas:
```python
result = await orchestrator.assess_trend(topic)
result = await orchestrator.detect_oversupply(area, papers)
```

### 3. Evaluating Collaboration Opportunities
Use ResearcherEvaluationAgent:
```python
result = await orchestrator.evaluate_researcher(publications)
```

### 4. Literature Review
Use TranslationAgent for quick paper summaries:
```python
result = await orchestrator.translation_agent.translate(abstract)
```

## Configuration

### Using Different Models

```python
# Use GPT-3.5 for faster, cheaper analysis
orchestrator = DeepLensOrchestrator(model="gpt-3.5-turbo")

# Explicitly provide API key
orchestrator = DeepLensOrchestrator(api_key="sk-...")
```

### Accessing Individual Agents

```python
orchestrator = DeepLensOrchestrator()

# Get specific agent
translation_agent = orchestrator.get_agent("translation")
analysis_agent = orchestrator.get_agent("analysis")
researcher_agent = orchestrator.get_agent("researcher")
trend_agent = orchestrator.get_agent("trend")

# Use agent directly
result = await translation_agent.explain_buzzword("federated learning")
```

## Tips

1. **Start with Translation**: Use TranslationAgent first to understand unfamiliar research
2. **Be Specific**: Provide as much context as possible for better results
3. **Use Examples**: Check `examples.py` and `example_data/` for reference
4. **Iterate**: Try different phrasings if results aren't what you expected
5. **Combine Agents**: Use multiple agents for comprehensive analysis

## Troubleshooting

### "No module named 'semantic_kernel'"
```bash
pip install -r requirements.txt
```

### "OpenAI API key not provided"
Make sure you have `.env` file with `OPENAI_API_KEY=sk-...`

### "Rate limit exceeded"
Wait a moment and try again, or use a different API key

### Import errors
Make sure you're running from the DeepLens directory:
```bash
cd DeepLens
python your_script.py
```

## Next Steps

- Read the [full README](README.md) for detailed documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore `example_data/` for sample inputs

## Getting Help

- Open an issue on GitHub
- Check existing issues for similar problems
- Review the examples and documentation

Happy analyzing! 🔍
