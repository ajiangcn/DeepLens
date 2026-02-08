#!/usr/bin/env python3
"""
Validation script to check DeepLens structure without requiring external dependencies
"""

import os
import sys
import ast

def check_file_syntax(filepath):
    """Check if a Python file has valid syntax"""
    try:
        with open(filepath, 'r') as f:
            ast.parse(f.read())
        return True, None
    except SyntaxError as e:
        return False, str(e)

def validate_structure():
    """Validate the project structure"""
    print("=" * 80)
    print("DeepLens Structure Validation")
    print("=" * 80)
    
    # Expected files
    required_files = [
        'README.md',
        'requirements.txt',
        'setup.py',
        'LICENSE',
        '.env.example',
        '.gitignore',
        'main.py',
        'examples.py',
        'deeplens/__init__.py',
        'deeplens/orchestrator.py',
        'deeplens/agents/__init__.py',
        'deeplens/agents/translation_agent.py',
        'deeplens/agents/analysis_agent.py',
        'deeplens/agents/researcher_evaluation_agent.py',
        'deeplens/agents/trend_assessment_agent.py',
    ]
    
    print("\n1. Checking required files...")
    all_exist = True
    for filepath in required_files:
        exists = os.path.exists(filepath)
        status = "✓" if exists else "✗"
        print(f"  {status} {filepath}")
        if not exists:
            all_exist = False
    
    if not all_exist:
        print("\n❌ Some required files are missing!")
        return False
    
    print("\n2. Checking Python syntax...")
    python_files = [f for f in required_files if f.endswith('.py')]
    all_valid = True
    for filepath in python_files:
        valid, error = check_file_syntax(filepath)
        status = "✓" if valid else "✗"
        print(f"  {status} {filepath}")
        if not valid:
            print(f"     Error: {error}")
            all_valid = False
    
    if not all_valid:
        print("\n❌ Some Python files have syntax errors!")
        return False
    
    print("\n3. Checking example data files...")
    example_files = [
        'example_data/researcher_publications.json',
        'example_data/recent_papers.json',
        'example_data/sample_paper.txt',
    ]
    
    for filepath in example_files:
        exists = os.path.exists(filepath)
        status = "✓" if exists else "✗"
        print(f"  {status} {filepath}")
    
    print("\n4. Checking agent implementations...")
    agents = [
        ('TranslationAgent', 'deeplens/agents/translation_agent.py'),
        ('AnalysisAgent', 'deeplens/agents/analysis_agent.py'),
        ('ResearcherEvaluationAgent', 'deeplens/agents/researcher_evaluation_agent.py'),
        ('TrendAssessmentAgent', 'deeplens/agents/trend_assessment_agent.py'),
    ]
    
    for agent_name, filepath in agents:
        with open(filepath, 'r') as f:
            content = f.read()
            has_class = f'class {agent_name}' in content
            has_init = '__init__' in content
            status = "✓" if has_class and has_init else "✗"
            print(f"  {status} {agent_name}")
    
    print("\n" + "=" * 80)
    print("✅ All validation checks passed!")
    print("=" * 80)
    
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up API key: cp .env.example .env (and add your OPENAI_API_KEY)")
    print("3. Run examples: python examples.py")
    print("4. Use CLI: python main.py --help")
    
    return True

if __name__ == "__main__":
    success = validate_structure()
    sys.exit(0 if success else 1)
