"""
Interactive CLI with Rich formatting for DeepLens.

Two-command interface:
  paper      – paste a paper link or text → understand the paper
  researcher – paste a Google Scholar link → evaluate the researcher
"""

import asyncio
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box

from deeplens import DeepLensOrchestrator
from deeplens.config import DeepLensConfig


console = Console()


class InteractiveCLI:
    """
    Interactive command-line interface for DeepLens — two workflows.
    """
    
    def __init__(self, config: Optional[DeepLensConfig] = None):
        self.config = config or DeepLensConfig.from_env()
        self.orchestrator = None
    
    def _get_orchestrator(self) -> DeepLensOrchestrator:
        """Get or create orchestrator"""
        if self.orchestrator is None:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task("Initializing DeepLens...", total=None)
                if self.config.use_azure:
                    self.orchestrator = DeepLensOrchestrator(
                        provider="azure_openai",
                        model=self.config.model,
                        api_base=self.config.azure_api_base,
                        api_version=self.config.azure_api_version,
                    )
                else:
                    self.orchestrator = DeepLensOrchestrator(
                        api_key=self.config.api_key,
                        model=self.config.model,
                    )
        return self.orchestrator
    
    def show_welcome(self):
        """Display welcome message"""
        console.clear()
        welcome_text = """
# 🔬 DeepLens Interactive CLI

Looking deeply beyond the surface of research hype

## Available Commands:
1. **paper**      – Paste a paper link or text → understand the paper
2. **researcher** – Paste a Google Scholar link → evaluate the researcher
3. **help**       – Show this help message
4. **exit**       – Quit the application
        """
        console.print(Panel(Markdown(welcome_text), border_style="blue"))
    
    # ------------------------------------------------------------------
    # Workflow 1 — Understand Paper
    # ------------------------------------------------------------------

    async def paper_mode(self):
        """Interactive paper understanding mode."""
        console.print("\n[bold cyan]📄 Understand Paper[/bold cyan]")
        console.print("Paste a paper link (arXiv, DOI, …) or raw text.\n")

        url_or_text = Prompt.ask("Paper link or text")

        if not url_or_text.strip():
            console.print("[yellow]⚠️  No input provided[/yellow]")
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Fetching & analysing paper...", total=None)
            orchestrator = self._get_orchestrator()
            result = await orchestrator.understand_paper(url_or_text.strip())

        # Build output
        lines = []
        if result.get("title"):
            lines.append(f"# {result['title']}")
        if result.get("authors"):
            lines.append(f"\n**Authors:** {', '.join(result['authors'])}")
        if result.get("url"):
            lines.append(f"**Source:** {result['source']} — {result['url']}")

        lines.append("\n---\n## 📖 Plain-Language Summary\n")
        lines.append(result["translation"].get("simplified", ""))
        lines.append("\n---\n## 🔬 Research Analysis\n")
        lines.append(result["analysis"].get("analysis", ""))

        console.print(Panel(
            Markdown("\n".join(lines)),
            title="📄 Paper Understanding",
            border_style="green",
        ))

    # ------------------------------------------------------------------
    # Workflow 2 — Evaluate Researcher
    # ------------------------------------------------------------------

    async def researcher_mode(self):
        """Interactive researcher evaluation mode."""
        console.print("\n[bold cyan]👨‍🔬 Evaluate Researcher[/bold cyan]")
        console.print("Paste a Google Scholar profile URL.\n")

        scholar_url = Prompt.ask("Google Scholar URL")

        if not scholar_url.strip():
            console.print("[yellow]⚠️  No input provided[/yellow]")
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Fetching profile & evaluating...", total=None)
            orchestrator = self._get_orchestrator()
            result = await orchestrator.evaluate_researcher_from_url(
                scholar_url.strip()
            )

        lines = [f"# {result['name']}"]
        if result.get("affiliation"):
            lines.append(f"\n**Affiliation:** {result['affiliation']}")
        lines.append(f"**Publications found:** {result['pub_count']}")
        lines.append("\n---\n## 👨‍🔬 Researcher Evaluation\n")
        lines.append(result["evaluation"].get("evaluation", ""))

        console.print(Panel(
            Markdown("\n".join(lines)),
            title=f"🔎 Researcher: {result['name']}",
            border_style="magenta",
        ))

    # ------------------------------------------------------------------
    # Help & run loop
    # ------------------------------------------------------------------

    def show_help(self):
        """Show help information"""
        table = Table(title="DeepLens Commands", box=box.ROUNDED)
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")

        table.add_row("paper", "Paste a paper link or text → understand the paper")
        table.add_row("researcher", "Paste a Google Scholar link → evaluate the researcher")
        table.add_row("help", "Show this help message")
        table.add_row("exit", "Quit the application")

        console.print(table)

    async def run(self):
        """Run the interactive CLI"""
        self.show_welcome()

        while True:
            console.print()
            command = Prompt.ask(
                "[bold green]DeepLens[/bold green]",
                choices=["paper", "researcher", "help", "exit"],
                default="help",
            ).lower()

            try:
                if command == "exit":
                    console.print("[yellow]👋 Goodbye![/yellow]")
                    break
                elif command == "help":
                    self.show_help()
                elif command == "paper":
                    await self.paper_mode()
                elif command == "researcher":
                    await self.researcher_mode()
            except KeyboardInterrupt:
                console.print("\n[yellow]Operation cancelled[/yellow]")
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")


def main():
    """Main entry point for interactive CLI"""
    cli = InteractiveCLI()
    asyncio.run(cli.run())


if __name__ == "__main__":
    main()
