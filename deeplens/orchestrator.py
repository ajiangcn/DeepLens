"""
DeepLens Orchestrator: Main coordination layer for the multi-agent system.

Exposes two primary user workflows:
  1. understand_paper(url_or_text)    – fetch a paper via link and produce a
     plain-language summary + research-stage analysis.
  2. evaluate_researcher_from_url(scholar_url) – scrape a Google Scholar
     profile and classify the researcher's strategy.
"""

import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from .llm_provider import create_llm_client, LLMProvider, BaseLLMClient
from .scraper import fetch_paper, fetch_google_scholar_profile, is_url
from .agents.translation_agent import TranslationAgent
from .agents.analysis_agent import AnalysisAgent
from .agents.researcher_evaluation_agent import ResearcherEvaluationAgent
from .agents.trend_assessment_agent import TrendAssessmentAgent


class DeepLensOrchestrator:
    """
    Main orchestrator for the DeepLens multi-agent system.
    
    Two primary workflows:
    1. understand_paper      – Link → fetch → translate + analyse
    2. evaluate_researcher   – Google Scholar link → scrape → classify
    """
    
    def __init__(
        self, 
        provider: str = "openai",
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ):
        """
        Initialize the DeepLens orchestrator
        
        Args:
            provider: LLM provider (openai, azure_openai, anthropic, etc.)
            model: Model identifier
            api_key: API key (or None to load from .env)
            api_base: Base URL for API (e.g., Azure endpoint)
            api_version: API version (for Azure)
            temperature: Sampling temperature
            **kwargs: Additional provider-specific parameters
        """
        # Load environment variables
        load_dotenv()
        
        # Set up API key / credentials if not provided
        provider_lower = provider.lower()
        if provider_lower == "azure_openai":
            # Azure OpenAI uses DefaultAzureCredential — no API key needed
            api_base = api_base or os.getenv("AZURE_API_BASE") or os.getenv("AZURE_OPENAI_ENDPOINT")
            api_version = api_version or os.getenv("AZURE_API_VERSION") or os.getenv("AZURE_OPENAI_API_VERSION")
        elif api_key is None:
            if provider_lower == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
            elif provider_lower == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")
            elif provider_lower == "gemini":
                api_key = os.getenv("GEMINI_API_KEY")
            elif provider_lower == "cohere":
                api_key = os.getenv("COHERE_API_KEY")
            
            if not api_key:
                raise ValueError(
                    f"API key not provided for {provider}. Either pass api_key parameter "
                    f"or set appropriate environment variable."
                )
        
        # Create LLM client
        self.llm_client = create_llm_client(
            provider=provider,
            model=model,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            temperature=temperature,
            **kwargs
        )
        
        # Initialize agents with the LLM client
        self.translation_agent = TranslationAgent(self.llm_client)
        self.analysis_agent = AnalysisAgent(self.llm_client)
        self.researcher_agent = ResearcherEvaluationAgent(self.llm_client)
        self.trend_agent = TrendAssessmentAgent(self.llm_client)

    # ------------------------------------------------------------------
    # Primary workflow 1: Understand a paper
    # ------------------------------------------------------------------

    async def understand_paper(self, url_or_text: str) -> Dict[str, Any]:
        """
        Given a paper link (arXiv, Semantic Scholar, DOI, or generic URL)
        **or** raw text, fetch the content, translate it to plain language,
        and analyse the research stage & demand.

        Args:
            url_or_text: A paper URL or pasted paper text.

        Returns:
            {
                "title":       str,
                "authors":     list[str],
                "source":      str,           # "arxiv" | "web" | "text" | …
                "url":         str | None,
                "translation": { "simplified": str, … },
                "analysis":    { "analysis": str, … },
            }
        """
        # Step 1 — resolve content
        if is_url(url_or_text):
            paper = fetch_paper(url_or_text)
            content = paper.get("content") or paper.get("abstract") or ""
            title = paper.get("title", "")
            authors = paper.get("authors", [])
            source = paper.get("source", "web")
            paper_url = paper.get("url", url_or_text)
        else:
            content = url_or_text
            title = ""
            authors = []
            source = "text"
            paper_url = None

        if not content.strip():
            raise ValueError("Could not extract content from the provided input.")

        # Step 2 — translate + analyse in sequence (agents share context)
        translation = await self.translation_agent.translate(content)
        analysis = await self.analysis_agent.analyze(content)

        return {
            "title": title,
            "authors": authors,
            "source": source,
            "url": paper_url,
            "translation": translation,
            "analysis": analysis,
        }

    # ------------------------------------------------------------------
    # Primary workflow 2: Evaluate a researcher
    # ------------------------------------------------------------------

    async def evaluate_researcher_from_url(
        self, scholar_url: str
    ) -> Dict[str, Any]:
        """
        Scrape a Google Scholar profile and evaluate the researcher's
        pattern (trend follower / deep specialist / abstraction upleveler).

        Args:
            scholar_url: Google Scholar profile URL.

        Returns:
            {
                "name":         str,
                "affiliation":  str,
                "pub_count":    int,
                "url":          str,
                "evaluation":   { "evaluation": str, … },
            }
        """
        profile = fetch_google_scholar_profile(scholar_url)
        name = profile.get("name", "Unknown")
        publications = profile.get("publications", [])

        if not publications:
            raise ValueError(
                f"No publications found for {name}. "
                "The profile may be private or empty."
            )

        evaluation = await self.researcher_agent.evaluate_researcher(
            publications, name
        )

        return {
            "name": name,
            "affiliation": profile.get("affiliation", ""),
            "pub_count": len(publications),
            "url": profile.get("url", scholar_url),
            "evaluation": evaluation,
        }

    # ------------------------------------------------------------------
    # Legacy / lower-level helpers (kept for programmatic use)
    # ------------------------------------------------------------------

    async def evaluate_researcher(
        self, 
        publications: List[Dict[str, Any]],
        researcher_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a researcher's pattern from raw publication data.
        
        Args:
            publications: List of publications (with title, abstract, year)
            researcher_name: Optional researcher name
            
        Returns:
            Evaluation of researcher pattern
        """
        return await self.researcher_agent.evaluate_researcher(
            publications, 
            researcher_name
        )

    def get_agent(self, agent_name: str):
        """
        Get a specific agent by name
        
        Args:
            agent_name: One of 'translation', 'analysis', 'researcher', 'trend'
            
        Returns:
            The requested agent
        """
        agents = {
            "translation": self.translation_agent,
            "analysis": self.analysis_agent,
            "researcher": self.researcher_agent,
            "trend": self.trend_agent,
        }

        if agent_name not in agents:
            raise ValueError(
                f"Unknown agent: {agent_name}. "
                f"Available agents: {', '.join(agents.keys())}"
            )

        return agents[agent_name]
