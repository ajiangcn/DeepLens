"""
Interactive Web UI for DeepLens using Gradio.

Two-function interface:
  1. Understand Paper   – paste a paper link (arXiv, DOI, …) or raw text
  2. Evaluate Researcher – paste a Google Scholar profile URL
"""

import asyncio
import re
import gradio as gr
from typing import Optional, Generator

from deeplens import DeepLensOrchestrator
from deeplens.config import DeepLensConfig


# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
_CUSTOM_CSS = """
* {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}
.paper-card {
    background: linear-gradient(135deg, #667eea11 0%, #764ba211 100%);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.paper-card h2 { margin: 0 0 8px 0; color: #1a202c; font-size: 1.4em; }
.paper-card .meta { color: #4a5568; font-size: 0.92em; line-height: 1.6; }
.paper-card .meta a { color: #4c51bf; text-decoration: none; }
.paper-card .meta a:hover { text-decoration: underline; }

.researcher-card {
    background: linear-gradient(135deg, #38b2ac11 0%, #4fd1c511 100%);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.researcher-card h2 { margin: 0 0 8px 0; color: #1a202c; font-size: 1.4em; }
.researcher-card .meta { color: #4a5568; font-size: 0.92em; line-height: 1.6; }

.stage-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 600;
    margin-right: 8px;
}
.stage-exploration { background: #fef3c7; color: #92400e; }
.stage-scaling { background: #dbeafe; color: #1e40af; }
.stage-convergence { background: #d1fae5; color: #065f46; }

.status-msg {
    padding: 12px 16px;
    border-radius: 8px;
    background: #eef2ff;
    color: #3730a3;
    font-size: 0.95em;
    margin: 8px 0;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

.progress-bar {
    padding: 14px 20px;
    border-radius: 10px;
    background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
    border: 1px solid #c7d2fe;
    margin: 12px 0;
}
.progress-bar .steps {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
}
.progress-bar .step {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 0.82em;
    font-weight: 500;
    white-space: nowrap;
}
.step-done { background: #d1fae5; color: #065f46; }
.step-active { background: #dbeafe; color: #1e40af; animation: pulse 1.5s infinite; }
.step-pending { background: #f1f5f9; color: #94a3b8; }
.progress-bar .step-arrow { color: #94a3b8; font-size: 0.9em; }
.progress-bar .current-action {
    font-size: 0.92em;
    color: #4338ca;
    font-weight: 600;
}

details.result-section {
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    margin-bottom: 10px;
    overflow: hidden;
}
details.result-section > summary {
    padding: 12px 18px;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    cursor: pointer;
    font-weight: 600;
    font-size: 1.05em;
    color: #1e293b;
    list-style: none;
    display: flex;
    align-items: center;
    gap: 8px;
}
details.result-section > summary::-webkit-details-marker { display: none; }
details.result-section > summary::before {
    content: '▶';
    font-size: 0.7em;
    transition: transform 0.2s;
}
details.result-section[open] > summary::before {
    transform: rotate(90deg);
}
details.result-section > .section-body {
    padding: 14px 20px;
}

/* Side-by-side panels on desktop, stacked on mobile */
.results-row {
    display: flex;
    gap: 16px;
    align-items: flex-start;
}
.results-row > .result-panel {
    flex: 1;
    min-width: 0;
}
@media (max-width: 768px) {
    .results-row {
        flex-direction: column;
    }
}
.result-panel-header {
    font-size: 1.1em;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 8px;
    padding-bottom: 6px;
    border-bottom: 2px solid #e2e8f0;
}
"""


def _md(text: str) -> str:
    """Lightweight markdown → HTML for use inside <details> blocks."""
    import markdown
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


class DeepLensUI:
    """
    Web interface for DeepLens — two simple workflows.
    """
    
    def __init__(self, config: Optional[DeepLensConfig] = None):
        self.config = config or DeepLensConfig.from_env()
        self.orchestrator = None
    
    def _get_orchestrator(self) -> DeepLensOrchestrator:
        """Get or create orchestrator instance"""
        if self.orchestrator is None:
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
    
    # ------------------------------------------------------------------
    # Helpers — build rich HTML / Markdown for results
    # ------------------------------------------------------------------

    @staticmethod
    def _paper_info_card(result: dict) -> str:
        """Build an HTML card for paper metadata."""
        title = result.get("title", "Untitled Paper")
        authors = result.get("authors", [])
        source = result.get("source", "")
        url = result.get("url")

        authors_str = ", ".join(authors) if authors else "Unknown"
        source_badge = source.upper() if source else ""
        link_html = (
            f'<a href="{url}" target="_blank">{url}</a>'
            if url else "N/A"
        )

        return (
            f'<div class="paper-card">'
            f'  <h2>📄 {title}</h2>'
            f'  <div class="meta">'
            f'    <b>Authors:</b> {authors_str}<br>'
            f'    <b>Source:</b> <span class="stage-badge stage-scaling">{source_badge}</span> {link_html}'
            f'  </div>'
            f'</div>'
        )

    @staticmethod
    def _researcher_info_card(result: dict) -> str:
        """Build an HTML card for researcher metadata."""
        name = result.get("name", "Unknown")
        affiliation = result.get("affiliation", "")
        pub_count = result.get("pub_count", 0)

        aff_html = f"<br><b>Affiliation:</b> {affiliation}" if affiliation else ""
        return (
            f'<div class="researcher-card">'
            f'  <h2>👨‍🔬 {name}</h2>'
            f'  <div class="meta">'
            f'    <b>Publications analysed:</b> {pub_count}'
            f'    {aff_html}'
            f'  </div>'
            f'</div>'
        )

    @staticmethod
    def _status_html(msg: str) -> str:
        return f'<div class="status-msg">⏳ {msg}</div>'

    @staticmethod
    def _progress_html(steps: list[tuple[str, str]], current_msg: str) -> str:
        """
        Build a visual step-progress bar.

        Args:
            steps: list of (label, state) where state is 'done', 'active', or 'pending'
            current_msg: text shown below the steps
        """
        parts = []
        for i, (label, state) in enumerate(steps):
            icon = {"done": "✅", "active": "🔄", "pending": "⬜"}[state]
            parts.append(
                f'<span class="step step-{state}">{icon} {label}</span>'
            )
            if i < len(steps) - 1:
                parts.append('<span class="step-arrow">→</span>')
        steps_html = "".join(parts)
        return (
            f'<div class="progress-bar">'
            f'  <div class="steps">{steps_html}</div>'
            f'  <div class="current-action">⏳ {current_msg}</div>'
            f'</div>'
        )

    @staticmethod
    def _progress_done() -> str:
        """Return an empty string to clear the progress bar when done."""
        return (
            '<div class="progress-bar" style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); '
            'border-color: #6ee7b7;">'
            '  <div class="current-action" style="color: #065f46;">✅ Analysis complete</div>'
            '</div>'
        )

    @staticmethod
    def _make_collapsible(md_text: str) -> str:
        """
        Split markdown by ## headers and wrap each section in a
        collapsible <details> block.  Sections are open by default.

        Any text *before* the first ## header is kept as-is.
        """
        if not md_text or not md_text.strip():
            return md_text

        # Split on lines that start with '## '
        parts = re.split(r'^(## .+)$', md_text, flags=re.MULTILINE)

        # parts looks like: [preamble, '## H1', body1, '## H2', body2, ...]
        if len(parts) < 3:
            # No ## headers found — return as plain markdown
            return md_text

        html_parts = []
        # Preamble (text before first ## header)
        preamble = parts[0].strip()
        if preamble:
            html_parts.append(f'<div class="section-body">{_md(preamble)}</div>')

        # Iterate header/body pairs
        for i in range(1, len(parts), 2):
            header = parts[i].lstrip('# ').strip()
            body = parts[i + 1].strip() if i + 1 < len(parts) else ""
            html_parts.append(
                f'<details class="result-section" open>'
                f'<summary>{header}</summary>'
                f'<div class="section-body">{_md(body)}</div>'
                f'</details>'
            )

        return "\n".join(html_parts)

    # ------------------------------------------------------------------
    # Workflow 1 — Understand a paper (streaming progress)
    # ------------------------------------------------------------------

    def understand_paper_stream(self, url_or_text: str):
        """
        Generator that yields incremental progress updates while processing.
        Gradio calls this and renders each yielded tuple into the outputs.
        Outputs: (progress_html, paper_info_html, summary_md, analysis_md)
        """
        EMPTY = ("", "", "", "")
        if not url_or_text or not url_or_text.strip():
            yield ("", "", "⚠️ Please paste a paper link or some text.", "")
            return

        try:
            orchestrator = self._get_orchestrator()
            from deeplens.scraper import is_url, fetch_paper

            # -- Step 1: fetch --
            progress = self._progress_html(
                [("Fetch", "active"), ("Translate", "pending"), ("Analyse", "pending")],
                "Fetching paper content…",
            )
            yield (progress, "", "", "")

            if is_url(url_or_text.strip()):
                paper = fetch_paper(url_or_text.strip())
                content = paper.get("content") or paper.get("abstract") or ""
                meta = paper
            else:
                content = url_or_text.strip()
                meta = {"title": "", "authors": [], "source": "text", "url": None}

            if not content.strip():
                yield ("", "", "❌ Could not extract content from the provided input.", "")
                return

            info_card = self._paper_info_card(meta)

            # -- Step 2: translate --
            progress = self._progress_html(
                [("Fetch", "done"), ("Translate", "active"), ("Analyse", "pending")],
                "Translating into plain language…",
            )
            yield (progress, info_card, "", "")

            translation = asyncio.run(
                orchestrator.translation_agent.translate(content)
            )
            summary_md = translation.get("simplified", "")
            summary_html = self._make_collapsible(summary_md)

            # -- Step 3: analyse --
            progress = self._progress_html(
                [("Fetch", "done"), ("Translate", "done"), ("Analyse", "active")],
                "Analysing research stage & demand\u2026",
            )
            yield (progress, info_card, summary_html, "")

            analysis = asyncio.run(
                orchestrator.analysis_agent.analyze(content)
            )
            analysis_md = analysis.get("analysis", "")
            analysis_html = self._make_collapsible(analysis_md)

            # -- Done --
            yield (self._progress_done(), info_card, summary_html, analysis_html)

        except Exception as e:
            yield ("", "", f"❌ Error: {e}", "")

    # ------------------------------------------------------------------
    # Workflow 2 — Evaluate a researcher (streaming progress)
    # ------------------------------------------------------------------

    def evaluate_researcher_stream(self, scholar_url: str):
        """Generator that yields incremental progress for researcher eval.
        Outputs: (progress_html, researcher_info_html, eval_md)
        """
        if not scholar_url or not scholar_url.strip():
            yield ("", "", "⚠️ Please paste a Google Scholar profile URL.")
            return

        try:
            orchestrator = self._get_orchestrator()
            from deeplens.scraper import fetch_google_scholar_profile

            # -- Step 1: scrape --
            progress = self._progress_html(
                [("Fetch Profile", "active"), ("Evaluate", "pending")],
                "Fetching Google Scholar profile…",
            )
            yield (progress, "", "")

            profile = fetch_google_scholar_profile(scholar_url.strip())
            info_card = self._researcher_info_card({
                "name": profile.get("name", "Unknown"),
                "affiliation": profile.get("affiliation", ""),
                "pub_count": len(profile.get("publications", [])),
            })

            # -- Step 2: evaluate --
            progress = self._progress_html(
                [("Fetch Profile", "done"), ("Evaluate", "active")],
                "Evaluating researcher strategy…",
            )
            yield (progress, info_card, "")

            evaluation = asyncio.run(
                orchestrator.researcher_agent.evaluate_researcher(
                    publications=profile.get("publications", []),
                    researcher_name=profile.get("name"),
                )
            )
            eval_md = evaluation.get("evaluation", "")
            eval_html = self._make_collapsible(eval_md)

            # -- Done --
            yield (self._progress_done(), info_card, eval_html)

        except Exception as e:
            yield ("", "", f"❌ Error: {e}")

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface with two workflows."""
        with gr.Blocks(
            title="DeepLens: Research Analysis System",
            theme=gr.themes.Soft(),
            css=_CUSTOM_CSS,
        ) as interface:
            gr.Markdown(
                "# 🔬 DeepLens\n\n"
                "**Looking deeply beyond the surface of research hype**"
            )

            with gr.Tabs():
                # ============================================================
                # Tab 1: Understand Paper
                # ============================================================
                with gr.Tab("📄 Understand Paper"):
                    gr.Markdown(
                        "Paste an arXiv / Semantic Scholar / DOI link, any URL, "
                        "or raw paper text."
                    )
                    paper_input = gr.Textbox(
                        label="Paper Link or Text",
                        placeholder="https://arxiv.org/abs/2301.12345  or paste text…",
                        lines=3,
                    )
                    paper_btn = gr.Button(
                        "🔍 Understand Paper", variant="primary", size="lg"
                    )
                    gr.Examples(
                        examples=[
                            ["https://arxiv.org/abs/2301.07041"],
                            ["We propose a novel neural architecture search method "
                             "using differentiable search spaces..."],
                        ],
                        inputs=[paper_input],
                    )

                    # -- Progress + Result areas (all full-width, stacked) --
                    paper_progress = gr.HTML(label="Progress")
                    paper_info = gr.HTML(label="Paper Info")

                    with gr.Row(equal_height=False, elem_classes="results-row"):
                        with gr.Column(elem_classes="result-panel"):
                            gr.HTML('<div class="result-panel-header">📖 Plain-Language Summary</div>')
                            paper_summary = gr.HTML()
                        with gr.Column(elem_classes="result-panel"):
                            gr.HTML('<div class="result-panel-header">🔬 Research Stage & Demand Analysis</div>')
                            paper_analysis = gr.HTML()

                    paper_btn.click(
                        fn=self.understand_paper_stream,
                        inputs=paper_input,
                        outputs=[paper_progress, paper_info, paper_summary, paper_analysis],
                    )

                # ============================================================
                # Tab 2: Evaluate Researcher
                # ============================================================
                with gr.Tab("👨‍🔬 Evaluate Researcher"):
                    gr.Markdown(
                        "Paste a Google Scholar profile link to evaluate the "
                        "researcher's publication strategy."
                    )
                    scholar_input = gr.Textbox(
                        label="Google Scholar Profile URL",
                        placeholder="https://scholar.google.com/citations?user=XXXXXXXX",
                        lines=1,
                    )
                    scholar_btn = gr.Button(
                        "🔎 Evaluate Researcher", variant="primary", size="lg"
                    )

                    # -- Progress + Result areas --
                    researcher_progress = gr.HTML(label="Progress")
                    researcher_info = gr.HTML(label="Researcher Info")

                    gr.Markdown("### 📊 Researcher Evaluation")
                    researcher_eval = gr.HTML()

                    scholar_btn.click(
                        fn=self.evaluate_researcher_stream,
                        inputs=scholar_input,
                        outputs=[researcher_progress, researcher_info, researcher_eval],
                    )

            gr.Markdown(
                "---\n"
                "**💡 Tips** · "
                "The *Summary* translates jargon into plain language. "
                "The *Analysis* classifies the research stage "
                "(Exploration → Scaling → Convergence) and assesses real-world demand."
            )

        return interface
    
    def launch(self, share: bool = False, server_port: Optional[int] = None):
        """Launch the web interface."""
        port = server_port or self.config.ui_port
        interface = self.create_interface()
        print(f"🚀 Launching DeepLens UI on port {port}...")
        interface.launch(share=share, server_port=port, server_name="0.0.0.0")


def main():
    """Main entry point for UI"""
    ui = DeepLensUI()
    ui.launch()


if __name__ == "__main__":
    main()
