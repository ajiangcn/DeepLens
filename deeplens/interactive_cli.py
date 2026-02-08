"""
Interactive CLI with Rich formatting for DeepLens
"""

import asyncio
import json
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box

from deeplens import DeepLensOrchestrator
from deeplens.config import DeepLensConfig


console = Console()


class InteractiveCLI:
    """
    Interactive command-line interface for DeepLens
    """
    
    def __init__(self, config: Optional[DeepLensConfig] = None):
        """
        Initialize the interactive CLI
        
        Args:
            config: DeepLensConfig instance
        """
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
                self.orchestrator = DeepLensOrchestrator(
                    api_key=self.config.api_key,
                    model=self.config.model
                )
        return self.orchestrator
    
    def show_welcome(self):
        """Display welcome message"""
        console.clear()
        welcome_text = """
# 🔬 DeepLens Interactive CLI

Looking deeply beyond the surface of research hype

## Available Commands:
1. **Translate** - Simplify research jargon and buzzwords
2. **Analyze** - Identify problems, stages, and demand
3. **Evaluate** - Assess researcher patterns
4. **Trends** - Evaluate technical trends and hype
5. **Help** - Show this help message
6. **Exit** - Quit the application
        """
        console.print(Panel(Markdown(welcome_text), border_style="blue"))
    
    async def translate_mode(self):
        """Interactive translation mode"""
        console.print("\n[bold cyan]🌐 Translation Mode[/bold cyan]")
        console.print("Translate research text to plain language\n")
        
        is_buzzword = Confirm.ask("Is this a single buzzword?", default=False)
        
        if is_buzzword:
            content = Prompt.ask("Enter buzzword")
        else:
            console.print("Enter research text (press Ctrl+D when done):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            content = "\n".join(lines)
        
        if not content.strip():
            console.print("[yellow]⚠️  No input provided[/yellow]")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("Translating...", total=None)
            orchestrator = self._get_orchestrator()
            
            if is_buzzword:
                result = await orchestrator.explain_buzzword(content)
                console.print(Panel(
                    f"[bold]Buzzword:[/bold] {result['buzzword']}\n\n{result['explanation']}",
                    title="🔍 Translation",
                    border_style="green"
                ))
            else:
                result = await orchestrator.translation_agent.translate(content)
                console.print(Panel(
                    result['simplified'],
                    title="📖 Plain Language Translation",
                    border_style="green"
                ))
    
    async def analyze_mode(self):
        """Interactive analysis mode"""
        console.print("\n[bold cyan]🔬 Analysis Mode[/bold cyan]")
        console.print("Analyze research stage and demand\n")
        
        console.print("Enter research text (press Ctrl+D when done):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        content = "\n".join(lines)
        
        if not content.strip():
            console.print("[yellow]⚠️  No input provided[/yellow]")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("Analyzing...", total=None)
            orchestrator = self._get_orchestrator()
            result = await orchestrator.analysis_agent.analyze(content)
            
            console.print(Panel(
                result['analysis'],
                title="📊 Research Analysis",
                border_style="blue"
            ))
    
    async def evaluate_mode(self):
        """Interactive researcher evaluation mode"""
        console.print("\n[bold cyan]👨‍🔬 Researcher Evaluation Mode[/bold cyan]")
        console.print("Evaluate researcher patterns\n")
        
        researcher_name = Prompt.ask("Researcher name (optional)", default="")
        
        console.print("Enter publications as JSON (press Ctrl+D when done):")
        console.print("Format: [{'year': 2020, 'title': '...', 'abstract': '...'}, ...]")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        try:
            publications = json.loads("\n".join(lines))
            if isinstance(publications, dict) and 'publications' in publications:
                publications = publications['publications']
        except json.JSONDecodeError as e:
            console.print(f"[red]❌ Invalid JSON: {e}[/red]")
            return
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("Evaluating...", total=None)
            orchestrator = self._get_orchestrator()
            result = await orchestrator.evaluate_researcher(
                publications,
                researcher_name if researcher_name else None
            )
            
            title = "🔎 Researcher Evaluation"
            if researcher_name:
                title += f": {researcher_name}"
            
            console.print(Panel(
                result['evaluation'],
                title=title,
                border_style="magenta"
            ))
    
    async def trend_mode(self):
        """Interactive trend assessment mode"""
        console.print("\n[bold cyan]📈 Trend Assessment Mode[/bold cyan]")
        console.print("Assess technical trends and hype\n")
        
        topic = Prompt.ask("Enter trend or research area")
        check_oversupply = Confirm.ask("Check for oversupply?", default=False)
        
        if not topic.strip():
            console.print("[yellow]⚠️  No topic provided[/yellow]")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("Assessing...", total=None)
            orchestrator = self._get_orchestrator()
            
            if check_oversupply:
                result = await orchestrator.detect_oversupply(topic)
                console.print(Panel(
                    result['oversupply_analysis'],
                    title=f"📊 Oversupply Analysis: {topic}",
                    border_style="yellow"
                ))
            else:
                result = await orchestrator.assess_trend(topic)
                console.print(Panel(
                    result['assessment'],
                    title=f"📈 Trend Assessment: {topic}",
                    border_style="yellow"
                ))
    
    def show_help(self):
        """Show help information"""
        table = Table(title="DeepLens Commands", box=box.ROUNDED)
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        
        table.add_row("translate", "Simplify research jargon and buzzwords")
        table.add_row("analyze", "Identify problems, stages, and demand")
        table.add_row("evaluate", "Assess researcher patterns")
        table.add_row("trends", "Evaluate technical trends and hype")
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
                choices=["translate", "analyze", "evaluate", "trends", "help", "exit"],
                default="help"
            ).lower()
            
            try:
                if command == "exit":
                    console.print("[yellow]👋 Goodbye![/yellow]")
                    break
                elif command == "help":
                    self.show_help()
                elif command == "translate":
                    await self.translate_mode()
                elif command == "analyze":
                    await self.analyze_mode()
                elif command == "evaluate":
                    await self.evaluate_mode()
                elif command == "trends":
                    await self.trend_mode()
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
