"""
Main entry point for DeepLens CLI.

Two commands:
  paper      <url_or_text>       – understand a research paper
  researcher <google_scholar_url> – evaluate a researcher
"""

import asyncio
import argparse
import json
import sys
import os

from dotenv import load_dotenv

from deeplens import DeepLensOrchestrator
from deeplens.config import DeepLensConfig


async def paper_command(orchestrator: DeepLensOrchestrator, args):
    """Handle the 'paper' command."""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            url_or_text = f.read()
    else:
        url_or_text = args.input

    result = await orchestrator.understand_paper(url_or_text)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        if result.get("title"):
            print(f"# {result['title']}\n")
        if result.get("authors"):
            print(f"Authors: {', '.join(result['authors'])}\n")
        if result.get("url"):
            print(f"Source: {result['source']} — {result['url']}\n")

        print("--- PLAIN-LANGUAGE SUMMARY ---\n")
        print(result["translation"].get("simplified", ""))
        print("\n--- RESEARCH ANALYSIS ---\n")
        print(result["analysis"].get("analysis", ""))


async def researcher_command(orchestrator: DeepLensOrchestrator, args):
    """Handle the 'researcher' command."""
    result = await orchestrator.evaluate_researcher_from_url(args.url)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"# {result['name']}\n")
        if result.get("affiliation"):
            print(f"Affiliation: {result['affiliation']}")
        print(f"Publications found: {result['pub_count']}\n")
        print("--- RESEARCHER EVALUATION ---\n")
        print(result["evaluation"].get("evaluation", ""))


def _build_orchestrator(args) -> DeepLensOrchestrator:
    """Create orchestrator from CLI args + .env config."""
    load_dotenv()
    config = DeepLensConfig.from_env()

    if config.use_azure:
        return DeepLensOrchestrator(
            provider="azure_openai",
            model=args.model or config.model,
            api_base=config.azure_api_base,
            api_version=config.azure_api_version,
        )
    else:
        return DeepLensOrchestrator(
            api_key=args.api_key or config.api_key,
            model=args.model or config.model,
        )


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DeepLens — research analysis from just a link",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Understand a paper from an arXiv link
  python main.py paper "https://arxiv.org/abs/2301.07041"

  # Understand a paper from a local file
  python main.py paper --file paper.txt

  # Evaluate a researcher from Google Scholar
  python main.py researcher "https://scholar.google.com/citations?user=XXXXXXXX"
        """,
    )

    parser.add_argument(
        "--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)"
    )
    parser.add_argument("--model", default=None, help="Model to use")
    parser.add_argument(
        "--json", action="store_true", help="Output results as JSON"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # --- paper ---
    paper_parser = subparsers.add_parser(
        "paper", help="Understand a research paper (link or text)"
    )
    paper_parser.add_argument(
        "input", nargs="?", help="Paper URL or text (or use --file)"
    )
    paper_parser.add_argument(
        "--file", help="File containing paper text"
    )

    # --- researcher ---
    researcher_parser = subparsers.add_parser(
        "researcher", help="Evaluate a researcher from Google Scholar"
    )
    researcher_parser.add_argument(
        "url", help="Google Scholar profile URL"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        orchestrator = _build_orchestrator(args)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.command == "paper":
            if not args.input and not args.file:
                print("Error: provide a paper URL/text or --file", file=sys.stderr)
                sys.exit(1)
            await paper_command(orchestrator, args)
        elif args.command == "researcher":
            await researcher_command(orchestrator, args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
