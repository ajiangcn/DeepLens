"""
DeepLens Orchestrator: Main coordination layer for the multi-agent system
"""

import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase

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
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        use_azure: bool = False
    ):
        """
        Initialize the DeepLens orchestrator
        
        Args:
            api_key: OpenAI API key (or None to load from .env)
            model: Model to use (default: gpt-4)
            use_azure: Whether to use Azure OpenAI (NOT YET IMPLEMENTED - will raise NotImplementedError)
        
        Note:
            Azure OpenAI support is planned but not yet implemented. Setting use_azure=True
            will raise NotImplementedError. Use standard OpenAI for now.
        """
        # Load environment variables
        load_dotenv()
        
        # Set up API key
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not provided. Either pass api_key parameter "
                "or set OPENAI_API_KEY environment variable."
            )
        
        # Initialize Semantic Kernel
        self.kernel = Kernel()
        
        # Add chat completion service
        if use_azure:
            # Azure OpenAI configuration
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
            if not endpoint or not deployment:
                raise ValueError(
                    "Azure OpenAI requires AZURE_OPENAI_ENDPOINT and "
                    "AZURE_OPENAI_DEPLOYMENT environment variables"
                )
            # Note: Azure setup would go here
            raise NotImplementedError("Azure OpenAI support coming soon")
        else:
            # Standard OpenAI
            service_id = "default"
            self.kernel.add_service(
                OpenAIChatCompletion(
                    service_id=service_id,
                    ai_model_id=model,
                    api_key=api_key
                )
            )
        
        # Initialize agents
        self.translation_agent = TranslationAgent(self.kernel)
        self.analysis_agent = AnalysisAgent(self.kernel)
        self.researcher_agent = ResearcherEvaluationAgent(self.kernel)
        self.trend_agent = TrendAssessmentAgent(self.kernel)
    
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
