"""
DeepLens Orchestrator: Main coordination layer for the multi-agent system
"""

import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from .llm_provider import create_llm_client, LLMProvider, BaseLLMClient
from .agents.translation_agent import TranslationAgent
from .agents.analysis_agent import AnalysisAgent
from .agents.researcher_evaluation_agent import ResearcherEvaluationAgent
from .agents.trend_assessment_agent import TrendAssessmentAgent


class DeepLensOrchestrator:
    """
    Main orchestrator for the DeepLens multi-agent system.
    
    Coordinates four specialized agents:
    1. TranslationAgent - Simplifies research jargon and buzzwords
    2. AnalysisAgent - Identifies problems, research stages, and demand
    3. ResearcherEvaluationAgent - Evaluates researcher patterns
    4. TrendAssessmentAgent - Assesses trends, hype, and obsolescence
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
        
        # Set up API key if not provided
        if api_key is None:
            provider_lower = provider.lower()
            if provider_lower == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
            elif provider_lower == "azure_openai":
                api_key = os.getenv("AZURE_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
                api_base = api_base or os.getenv("AZURE_API_BASE") or os.getenv("AZURE_OPENAI_ENDPOINT")
                api_version = api_version or os.getenv("AZURE_API_VERSION") or os.getenv("AZURE_OPENAI_API_VERSION")
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
    
    async def analyze_research_paper(
        self, 
        content: str,
        include_translation: bool = True,
        include_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive analysis of a research paper
        
        Args:
            content: Research paper text or abstract
            include_translation: Whether to include plain language translation
            include_analysis: Whether to include problem/stage/demand analysis
            
        Returns:
            Dictionary with results from requested analyses
        """
        results = {}
        
        if include_translation:
            results["translation"] = await self.translation_agent.translate(content)
        
        if include_analysis:
            results["analysis"] = await self.analysis_agent.analyze(content)
        
        return results
    
    async def explain_buzzword(self, buzzword: str) -> Dict[str, Any]:
        """
        Explain a research buzzword in plain language
        
        Args:
            buzzword: Technical term or buzzword
            
        Returns:
            Plain language explanation
        """
        return await self.translation_agent.explain_buzzword(buzzword)
    
    async def evaluate_researcher(
        self, 
        publications: List[Dict[str, Any]],
        researcher_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a researcher's pattern and strategy
        
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
    
    async def assess_trend(
        self, 
        topic: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Assess a technical trend
        
        Args:
            topic: Technical trend or research area
            context: Optional additional context
            
        Returns:
            Trend assessment with hype analysis and predictions
        """
        return await self.trend_agent.assess_trend(topic, context)
    
    async def detect_oversupply(
        self,
        research_area: str,
        recent_papers: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Detect if a research area has too many researchers
        
        Args:
            research_area: Research area to analyze
            recent_papers: Optional list of recent papers
            
        Returns:
            Oversupply analysis
        """
        return await self.trend_agent.detect_oversupply(
            research_area,
            recent_papers
        )
    
    async def comprehensive_analysis(
        self,
        research_content: str,
        trend_topics: Optional[List[str]] = None,
        researcher_publications: Optional[List[Dict[str, Any]]] = None,
        researcher_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run a comprehensive analysis using all agents
        
        Args:
            research_content: Research paper or content to analyze
            trend_topics: Optional list of trends to assess
            researcher_publications: Optional publications for researcher evaluation
            researcher_name: Optional researcher name
            
        Returns:
            Complete analysis from all agents
        """
        results = {
            "analyses": {}
        }
        
        # Translation and Analysis
        results["analyses"]["paper"] = await self.analyze_research_paper(
            research_content,
            include_translation=True,
            include_analysis=True
        )
        
        # Trend Assessment
        if trend_topics:
            results["analyses"]["trends"] = []
            for topic in trend_topics:
                trend_result = await self.assess_trend(topic)
                results["analyses"]["trends"].append(trend_result)
        
        # Researcher Evaluation
        if researcher_publications:
            results["analyses"]["researcher"] = await self.evaluate_researcher(
                researcher_publications,
                researcher_name
            )
        
        return results
    
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
            "trend": self.trend_agent
        }
        
        if agent_name not in agents:
            raise ValueError(
                f"Unknown agent: {agent_name}. "
                f"Available agents: {', '.join(agents.keys())}"
            )
        
        return agents[agent_name]
