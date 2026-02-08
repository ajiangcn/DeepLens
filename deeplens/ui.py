"""
Interactive Web UI for DeepLens using Gradio
"""

import asyncio
import gradio as gr
from typing import Optional, Dict, Any
import json

from deeplens import DeepLensOrchestrator
from deeplens.config import DeepLensConfig


class DeepLensUI:
    """
    Interactive web interface for DeepLens multi-agent system
    """
    
    def __init__(self, config: Optional[DeepLensConfig] = None):
        """
        Initialize the UI
        
        Args:
            config: DeepLensConfig instance (or None to load from env)
        """
        self.config = config or DeepLensConfig.from_env()
        self.orchestrator = None
    
    def _get_orchestrator(self) -> DeepLensOrchestrator:
        """Get or create orchestrator instance"""
        if self.orchestrator is None:
            self.orchestrator = DeepLensOrchestrator(
                api_key=self.config.api_key,
                model=self.config.model
            )
        return self.orchestrator
    
    async def translate_text(
        self,
        content: str,
        is_buzzword: bool = False
    ) -> str:
        """
        Translate research text or explain buzzword
        
        Args:
            content: Research text or buzzword
            is_buzzword: Whether to treat as a single buzzword
            
        Returns:
            Formatted result
        """
        if not content or not content.strip():
            return "⚠️ Please enter some text to translate."
        
        try:
            orchestrator = self._get_orchestrator()
            
            if is_buzzword:
                result = await orchestrator.explain_buzzword(content.strip())
                output = f"## 🔍 Buzzword: {result['buzzword']}\n\n"
                output += f"{result['explanation']}"
            else:
                result = await orchestrator.translation_agent.translate(content)
                output = f"## 📖 Plain Language Translation\n\n"
                output += f"{result['simplified']}"
            
            return output
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def analyze_research(
        self,
        content: str
    ) -> str:
        """
        Analyze research paper or proposal
        
        Args:
            content: Research text to analyze
            
        Returns:
            Formatted analysis result
        """
        if not content or not content.strip():
            return "⚠️ Please enter research text to analyze."
        
        try:
            orchestrator = self._get_orchestrator()
            result = await orchestrator.analysis_agent.analyze(content)
            
            output = "## 🔬 Research Analysis\n\n"
            output += result['analysis']
            
            return output
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def evaluate_researcher(
        self,
        publications_json: str,
        researcher_name: Optional[str] = None
    ) -> str:
        """
        Evaluate researcher pattern
        
        Args:
            publications_json: JSON string of publications
            researcher_name: Optional researcher name
            
        Returns:
            Formatted evaluation result
        """
        if not publications_json or not publications_json.strip():
            return "⚠️ Please enter publications data in JSON format."
        
        try:
            publications = json.loads(publications_json)
            if isinstance(publications, dict) and 'publications' in publications:
                publications = publications['publications']
            
            orchestrator = self._get_orchestrator()
            result = await orchestrator.evaluate_researcher(
                publications,
                researcher_name
            )
            
            output = "## 👨‍🔬 Researcher Evaluation\n\n"
            if researcher_name:
                output += f"**Researcher**: {researcher_name}\n\n"
            output += result['evaluation']
            
            return output
        except json.JSONDecodeError:
            return "❌ Error: Invalid JSON format. Please check your input."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def assess_trend(
        self,
        topic: str,
        check_oversupply: bool = False
    ) -> str:
        """
        Assess a technical trend
        
        Args:
            topic: Trend or research area to assess
            check_oversupply: Whether to check for oversupply
            
        Returns:
            Formatted assessment result
        """
        if not topic or not topic.strip():
            return "⚠️ Please enter a trend or research area to assess."
        
        try:
            orchestrator = self._get_orchestrator()
            
            if check_oversupply:
                result = await orchestrator.detect_oversupply(topic)
                output = f"## 📊 Oversupply Analysis: {topic}\n\n"
                output += result['oversupply_analysis']
            else:
                result = await orchestrator.assess_trend(topic)
                output = f"## 📈 Trend Assessment: {topic}\n\n"
                output += result['assessment']
            
            return output
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def create_interface(self) -> gr.Blocks:
        """
        Create the Gradio interface
        
        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(
            title="DeepLens: Research Analysis System",
            theme=gr.themes.Soft()
        ) as interface:
            gr.Markdown("""
            # 🔬 DeepLens: Multi-Agent Research Analysis
            
            Looking deeply beyond the surface of research hype
            
            Use the tabs below to access different analysis agents:
            - **Translate**: Simplify research jargon and buzzwords
            - **Analyze**: Identify problems, stages, and demand
            - **Evaluate**: Assess researcher patterns
            - **Trends**: Evaluate technical trends and hype
            """)
            
            with gr.Tabs():
                # Translation Tab
                with gr.Tab("🌐 Translate"):
                    gr.Markdown("### Translate Research to Plain Language")
                    with gr.Row():
                        with gr.Column():
                            translate_input = gr.Textbox(
                                label="Research Text or Buzzword",
                                placeholder="Enter research paper text, abstract, or a technical buzzword...",
                                lines=6
                            )
                            translate_buzzword = gr.Checkbox(
                                label="Treat as single buzzword",
                                value=False
                            )
                            translate_btn = gr.Button("🔍 Translate", variant="primary")
                        with gr.Column():
                            translate_output = gr.Markdown(label="Translation")
                    
                    translate_btn.click(
                        fn=lambda x, y: asyncio.run(self.translate_text(x, y)),
                        inputs=[translate_input, translate_buzzword],
                        outputs=translate_output
                    )
                    
                    gr.Examples(
                        examples=[
                            ["attention mechanism", True],
                            ["We propose a novel neural architecture search method using differentiable search spaces...", False],
                        ],
                        inputs=[translate_input, translate_buzzword]
                    )
                
                # Analysis Tab
                with gr.Tab("🔬 Analyze"):
                    gr.Markdown("### Analyze Research Stage & Demand")
                    with gr.Row():
                        with gr.Column():
                            analyze_input = gr.Textbox(
                                label="Research Paper or Proposal",
                                placeholder="Enter research paper text or abstract...",
                                lines=8
                            )
                            analyze_btn = gr.Button("📊 Analyze", variant="primary")
                        with gr.Column():
                            analyze_output = gr.Markdown(label="Analysis")
                    
                    analyze_btn.click(
                        fn=lambda x: asyncio.run(self.analyze_research(x)),
                        inputs=analyze_input,
                        outputs=analyze_output
                    )
                
                # Researcher Evaluation Tab
                with gr.Tab("👨‍🔬 Evaluate Researcher"):
                    gr.Markdown("### Evaluate Researcher Patterns")
                    with gr.Row():
                        with gr.Column():
                            researcher_name = gr.Textbox(
                                label="Researcher Name (Optional)",
                                placeholder="Dr. Jane Smith"
                            )
                            researcher_pubs = gr.Textbox(
                                label="Publications (JSON format)",
                                placeholder='[{"year": 2020, "title": "...", "abstract": "..."}, ...]',
                                lines=8
                            )
                            evaluate_btn = gr.Button("🔎 Evaluate", variant="primary")
                        with gr.Column():
                            evaluate_output = gr.Markdown(label="Evaluation")
                    
                    evaluate_btn.click(
                        fn=lambda x, y: asyncio.run(self.evaluate_researcher(x, y)),
                        inputs=[researcher_pubs, researcher_name],
                        outputs=evaluate_output
                    )
                
                # Trend Assessment Tab
                with gr.Tab("📈 Assess Trends"):
                    gr.Markdown("### Assess Technical Trends & Hype")
                    with gr.Row():
                        with gr.Column():
                            trend_input = gr.Textbox(
                                label="Trend or Research Area",
                                placeholder="Large Language Models",
                                lines=2
                            )
                            trend_oversupply = gr.Checkbox(
                                label="Check for oversupply",
                                value=False
                            )
                            trend_btn = gr.Button("📊 Assess", variant="primary")
                        with gr.Column():
                            trend_output = gr.Markdown(label="Assessment")
                    
                    trend_btn.click(
                        fn=lambda x, y: asyncio.run(self.assess_trend(x, y)),
                        inputs=[trend_input, trend_oversupply],
                        outputs=trend_output
                    )
                    
                    gr.Examples(
                        examples=[
                            ["Large Language Models", False],
                            ["BERT fine-tuning", True],
                        ],
                        inputs=[trend_input, trend_oversupply]
                    )
            
            gr.Markdown("""
            ---
            ### 💡 Tips
            - Use the **Translate** tab to understand complex research papers
            - Use **Analyze** to identify research maturity and real-world demand
            - Use **Evaluate** to understand researcher strategies and patterns
            - Use **Trends** to detect hype and find underexplored areas
            
            **Note**: Requires OpenAI API key configured in `.env` file
            """)
        
        return interface
    
    def launch(
        self,
        share: bool = False,
        server_port: Optional[int] = None
    ):
        """
        Launch the web interface
        
        Args:
            share: Whether to create a public link
            server_port: Port to run server on (defaults to config)
        """
        port = server_port or self.config.ui_port
        interface = self.create_interface()
        
        print(f"🚀 Launching DeepLens UI on port {port}...")
        print(f"📝 Make sure your OPENAI_API_KEY is set in .env file")
        
        interface.launch(
            share=share,
            server_port=port,
            server_name="0.0.0.0"
        )


def main():
    """Main entry point for UI"""
    ui = DeepLensUI()
    ui.launch()


if __name__ == "__main__":
    main()
