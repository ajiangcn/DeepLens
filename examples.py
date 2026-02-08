"""
Example usage of the DeepLens multi-agent system
"""

import asyncio
from deeplens import DeepLensOrchestrator


async def example_buzzword_translation():
    """Example: Translate a research buzzword"""
    print("=" * 80)
    print("EXAMPLE 1: Buzzword Translation")
    print("=" * 80)
    
    orchestrator = DeepLensOrchestrator()
    
    result = await orchestrator.explain_buzzword("transformer architecture")
    print(f"\nBuzzword: {result['buzzword']}")
    print(f"\nExplanation:\n{result['explanation']}")


async def example_paper_analysis():
    """Example: Analyze a research paper"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Research Paper Analysis")
    print("=" * 80)
    
    paper_abstract = """
    We propose a novel approach to few-shot learning using meta-learning with 
    adaptive attention mechanisms. Our method achieves state-of-the-art performance
    on benchmark datasets by learning to learn across tasks with minimal data.
    We introduce a novel adaptive attention module that dynamically adjusts based
    on task characteristics, enabling better generalization.
    """
    
    orchestrator = DeepLensOrchestrator()
    
    result = await orchestrator.analyze_research_paper(
        paper_abstract,
        include_translation=True,
        include_analysis=True
    )
    
    print("\nTranslation:")
    print(result['translation']['simplified'])
    print("\nAnalysis:")
    print(result['analysis']['analysis'])


async def example_researcher_evaluation():
    """Example: Evaluate a researcher's pattern"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Researcher Evaluation")
    print("=" * 80)
    
    publications = [
        {
            "year": 2018,
            "title": "Deep Learning for Image Classification",
            "abstract": "We apply deep convolutional networks to image classification..."
        },
        {
            "year": 2019,
            "title": "BERT for Natural Language Processing",
            "abstract": "We fine-tune BERT for various NLP tasks..."
        },
        {
            "year": 2020,
            "title": "Graph Neural Networks for Social Networks",
            "abstract": "We apply GNNs to social network analysis..."
        },
        {
            "year": 2021,
            "title": "Vision Transformers for Object Detection",
            "abstract": "We adapt vision transformers for object detection tasks..."
        }
    ]
    
    orchestrator = DeepLensOrchestrator()
    
    result = await orchestrator.evaluate_researcher(
        publications,
        researcher_name="Dr. Example"
    )
    
    print("\nResearcher Evaluation:")
    print(result['evaluation'])


async def example_trend_assessment():
    """Example: Assess a technical trend"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Trend Assessment")
    print("=" * 80)
    
    orchestrator = DeepLensOrchestrator()
    
    result = await orchestrator.assess_trend(
        "Large Language Models",
        context={
            "recent_developments": "ChatGPT, GPT-4, rapid commercial adoption",
            "concerns": "Compute costs, hallucination, alignment"
        }
    )
    
    print(f"\nTrend: {result['topic']}")
    print(f"\nAssessment:\n{result['assessment']}")


async def example_oversupply_detection():
    """Example: Detect research oversupply"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Oversupply Detection")
    print("=" * 80)
    
    orchestrator = DeepLensOrchestrator()
    
    recent_papers = [
        {"title": "Improving BERT with Better Pretraining", "year": 2023},
        {"title": "BERT Variants for Domain Adaptation", "year": 2023},
        {"title": "Fine-tuning BERT for Low-Resource Languages", "year": 2023},
        {"title": "BERT-based Models for Text Classification", "year": 2023},
    ]
    
    result = await orchestrator.detect_oversupply(
        "BERT fine-tuning",
        recent_papers=recent_papers
    )
    
    print(f"\nResearch Area: {result['research_area']}")
    print(f"\nOversupply Analysis:\n{result['oversupply_analysis']}")


async def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("DeepLens: Multi-Agent Research Analysis System")
    print("=" * 80)
    print("\nNOTE: These examples require a valid OPENAI_API_KEY in .env file")
    print("Copy .env.example to .env and add your API key to run examples.")
    print("=" * 80)
    
    # Check if API key is available
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  WARNING: OPENAI_API_KEY not found in environment")
        print("Please set OPENAI_API_KEY in .env file to run examples")
        print("\nExample .env file:")
        print("OPENAI_API_KEY=sk-your-key-here")
        return
    
    # Run examples
    try:
        await example_buzzword_translation()
        await example_paper_analysis()
        await example_researcher_evaluation()
        await example_trend_assessment()
        await example_oversupply_detection()
        
        print("\n" + "=" * 80)
        print("Examples completed successfully!")
        print("=" * 80)
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you have:")
        print("1. Installed dependencies: pip install -r requirements.txt")
        print("2. Set OPENAI_API_KEY in .env file")


if __name__ == "__main__":
    asyncio.run(main())
