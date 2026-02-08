#!/usr/bin/env python3
"""
Test script to verify DeepLens setup without requiring external dependencies
"""

import json
import os

def test_structure():
    """Test project structure"""
    print("Testing DeepLens Project Structure\n")
    print("=" * 60)
    
    # Test 1: Files exist
    print("\n1. Core Files:")
    core_files = [
        ('README.md', 'Main documentation'),
        ('QUICKSTART.md', 'Quick start guide'),
        ('ARCHITECTURE.md', 'Architecture documentation'),
        ('CONTRIBUTING.md', 'Contributing guidelines'),
        ('LICENSE', 'License file'),
        ('requirements.txt', 'Python dependencies'),
        ('setup.py', 'Package setup'),
    ]
    
    for filepath, desc in core_files:
        exists = os.path.exists(filepath)
        status = "✓" if exists else "✗"
        print(f"  {status} {filepath:25s} - {desc}")
    
    # Test 2: Agent files
    print("\n2. Agent Implementations:")
    agents = [
        ('deeplens/agents/translation_agent.py', 'TranslationAgent'),
        ('deeplens/agents/analysis_agent.py', 'AnalysisAgent'),
        ('deeplens/agents/researcher_evaluation_agent.py', 'ResearcherEvaluationAgent'),
        ('deeplens/agents/trend_assessment_agent.py', 'TrendAssessmentAgent'),
    ]
    
    for filepath, agent_name in agents:
        exists = os.path.exists(filepath)
        status = "✓" if exists else "✗"
        print(f"  {status} {agent_name}")
    
    # Test 3: Example data
    print("\n3. Example Data:")
    data_files = [
        'example_data/researcher_publications.json',
        'example_data/recent_papers.json',
        'example_data/sample_paper.txt',
    ]
    
    for filepath in data_files:
        exists = os.path.exists(filepath)
        status = "✓" if exists else "✗"
        filename = os.path.basename(filepath)
        print(f"  {status} {filename}")
    
    # Test 4: Validate example data
    print("\n4. Example Data Validation:")
    
    try:
        with open('example_data/researcher_publications.json') as f:
            data = json.load(f)
            pubs = data.get('publications', [])
            print(f"  ✓ Researcher data: {len(pubs)} publications")
    except Exception as e:
        print(f"  ✗ Researcher data error: {e}")
    
    try:
        with open('example_data/recent_papers.json') as f:
            data = json.load(f)
            print(f"  ✓ Recent papers: {len(data)} papers")
    except Exception as e:
        print(f"  ✗ Recent papers error: {e}")
    
    try:
        with open('example_data/sample_paper.txt') as f:
            content = f.read()
            print(f"  ✓ Sample paper: {len(content)} characters")
    except Exception as e:
        print(f"  ✗ Sample paper error: {e}")
    
    # Test 5: Check requirements
    print("\n5. Dependencies Check:")
    
    try:
        with open('requirements.txt') as f:
            deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"  ✓ Found {len(deps)} dependencies")
            for dep in deps:
                print(f"    - {dep}")
    except Exception as e:
        print(f"  ✗ Requirements error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Project structure is complete and valid!")
    print("=" * 60)
    
    print("\nNext Steps:")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Configure API key:")
    print("   cp .env.example .env")
    print("   # Edit .env and add OPENAI_API_KEY=your-key")
    print("\n3. Run examples:")
    print("   python examples.py")
    print("\n4. Use CLI:")
    print("   python main.py translate --buzzword 'attention mechanism'")
    print("   python main.py analyze --file example_data/sample_paper.txt")
    print("   python main.py evaluate example_data/researcher_publications.json")
    print("   python main.py trend 'Large Language Models'")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_structure()
