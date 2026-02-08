"""
Main entry point for DeepLens CLI
"""

import asyncio
import argparse
import json
import sys
from typing import Optional

from deeplens import DeepLensOrchestrator


async def translate_command(orchestrator: DeepLensOrchestrator, args):
    """Handle translate command"""
    if args.file:
        with open(args.file, 'r') as f:
            content = f.read()
    else:
        content = args.text
    
    if args.buzzword:
        result = await orchestrator.explain_buzzword(content)
    else:
        result = await orchestrator.translation_agent.translate(content)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if args.buzzword:
            print(f"Buzzword: {result['buzzword']}")
            print(f"\n{result['explanation']}")
        else:
            print(result['simplified'])


async def analyze_command(orchestrator: DeepLensOrchestrator, args):
    """Handle analyze command"""
    if args.file:
        with open(args.file, 'r') as f:
            content = f.read()
    else:
        content = args.text
    
    result = await orchestrator.analysis_agent.analyze(content)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result['analysis'])


async def evaluate_command(orchestrator: DeepLensOrchestrator, args):
    """Handle evaluate command"""
    # Load publications from JSON file
    with open(args.publications, 'r') as f:
        data = json.load(f)
    
    publications = data.get('publications', data)
    researcher_name = data.get('researcher_name', args.name)
    
    result = await orchestrator.evaluate_researcher(publications, researcher_name)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result['evaluation'])


async def trend_command(orchestrator: DeepLensOrchestrator, args):
    """Handle trend command"""
    context = None
    if args.context:
        with open(args.context, 'r') as f:
            context = json.load(f)
    
    if args.oversupply:
        recent_papers = None
        if args.papers:
            with open(args.papers, 'r') as f:
                recent_papers = json.load(f)
        result = await orchestrator.detect_oversupply(args.topic, recent_papers)
        key = 'oversupply_analysis'
    else:
        result = await orchestrator.assess_trend(args.topic, context)
        key = 'assessment'
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result[key])


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="DeepLens: Multi-agent research analysis system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate a buzzword
  python main.py translate --buzzword "transformer architecture"
  
  # Analyze a research paper
  python main.py analyze --file paper.txt
  
  # Evaluate a researcher
  python main.py evaluate --publications researcher.json
  
  # Assess a trend
  python main.py trend "Large Language Models"
  
  # Detect oversupply
  python main.py trend "BERT fine-tuning" --oversupply
        """
    )
    
    parser.add_argument(
        '--api-key',
        help='OpenAI API key (or set OPENAI_API_KEY env var)'
    )
    parser.add_argument(
        '--model',
        default='gpt-4',
        help='Model to use (default: gpt-4)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Translate command
    translate_parser = subparsers.add_parser(
        'translate',
        help='Translate research content to plain language'
    )
    translate_parser.add_argument(
        'text',
        nargs='?',
        help='Text to translate (or use --file)'
    )
    translate_parser.add_argument(
        '--file',
        help='File containing text to translate'
    )
    translate_parser.add_argument(
        '--buzzword',
        action='store_true',
        help='Treat input as a single buzzword to explain'
    )
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze research to identify problems, stage, and demand'
    )
    analyze_parser.add_argument(
        'text',
        nargs='?',
        help='Text to analyze (or use --file)'
    )
    analyze_parser.add_argument(
        '--file',
        help='File containing text to analyze'
    )
    
    # Evaluate command
    evaluate_parser = subparsers.add_parser(
        'evaluate',
        help='Evaluate researcher patterns'
    )
    evaluate_parser.add_argument(
        'publications',
        help='JSON file with publications list'
    )
    evaluate_parser.add_argument(
        '--name',
        help='Researcher name'
    )
    
    # Trend command
    trend_parser = subparsers.add_parser(
        'trend',
        help='Assess technical trends'
    )
    trend_parser.add_argument(
        'topic',
        help='Trend or research area to assess'
    )
    trend_parser.add_argument(
        '--context',
        help='JSON file with additional context'
    )
    trend_parser.add_argument(
        '--oversupply',
        action='store_true',
        help='Detect oversupply in the research area'
    )
    trend_parser.add_argument(
        '--papers',
        help='JSON file with recent papers (for oversupply detection)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize orchestrator
    try:
        orchestrator = DeepLensOrchestrator(
            api_key=args.api_key,
            model=args.model
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == 'translate':
            await translate_command(orchestrator, args)
        elif args.command == 'analyze':
            await analyze_command(orchestrator, args)
        elif args.command == 'evaluate':
            await evaluate_command(orchestrator, args)
        elif args.command == 'trend':
            await trend_command(orchestrator, args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
