"""
Comprehensive tests for DeepLens Orchestrator
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from deeplens.orchestrator import DeepLensOrchestrator
from deeplens.llm_provider import LLMProvider


class TestDeepLensOrchestrator:
    """Tests for DeepLensOrchestrator"""
    
    def test_initialization_with_api_key(self):
        """Test initialization with API key provided"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            model="gpt-4",
            api_key="test_key"
        )
        
        assert orchestrator.llm_client is not None
        assert orchestrator.translation_agent is not None
        assert orchestrator.analysis_agent is not None
        assert orchestrator.researcher_agent is not None
        assert orchestrator.trend_agent is not None
    
    def test_initialization_with_env_openai(self):
        """Test initialization with OpenAI from environment"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'env_key'}):
            orchestrator = DeepLensOrchestrator(provider="openai")
            assert orchestrator.llm_client is not None
    
    def test_initialization_with_env_azure(self):
        """Test initialization with Azure OpenAI from environment"""
        with patch.dict('os.environ', {
            'AZURE_API_KEY': 'azure_key',
            'AZURE_API_BASE': 'https://test.openai.azure.com',
            'AZURE_API_VERSION': '2023-05-15'
        }):
            orchestrator = DeepLensOrchestrator(provider="azure_openai", model="gpt-35-turbo")
            assert orchestrator.llm_client is not None
    
    def test_initialization_missing_api_key(self):
        """Test initialization fails without API key"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                DeepLensOrchestrator(provider="openai")
            assert "API key not provided" in str(exc_info.value)
    
    def test_initialization_custom_temperature(self):
        """Test initialization with custom temperature"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key",
            temperature=0.5
        )
        assert orchestrator.llm_client.temperature == 0.5
    
    @pytest.mark.asyncio
    async def test_analyze_research_paper_translation_only(self):
        """Test analyzing paper with translation only"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        # Mock the translation agent
        orchestrator.translation_agent.translate = AsyncMock(
            return_value={"simplified": "Simplified text", "status": "success"}
        )
        
        result = await orchestrator.analyze_research_paper(
            "Research content",
            include_translation=True,
            include_analysis=False
        )
        
        assert "translation" in result
        assert "analysis" not in result
        assert result["translation"]["simplified"] == "Simplified text"
    
    @pytest.mark.asyncio
    async def test_analyze_research_paper_analysis_only(self):
        """Test analyzing paper with analysis only"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        orchestrator.analysis_agent.analyze = AsyncMock(
            return_value={"analysis": "Analysis text", "status": "success"}
        )
        
        result = await orchestrator.analyze_research_paper(
            "Research content",
            include_translation=False,
            include_analysis=True
        )
        
        assert "translation" not in result
        assert "analysis" in result
    
    @pytest.mark.asyncio
    async def test_analyze_research_paper_both(self):
        """Test analyzing paper with both translation and analysis"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        orchestrator.translation_agent.translate = AsyncMock(
            return_value={"simplified": "Simplified", "status": "success"}
        )
        orchestrator.analysis_agent.analyze = AsyncMock(
            return_value={"analysis": "Analysis", "status": "success"}
        )
        
        result = await orchestrator.analyze_research_paper(
            "Research content",
            include_translation=True,
            include_analysis=True
        )
        
        assert "translation" in result
        assert "analysis" in result
    
    @pytest.mark.asyncio
    async def test_explain_buzzword(self):
        """Test explain_buzzword method"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        orchestrator.translation_agent.explain_buzzword = AsyncMock(
            return_value={
                "buzzword": "transformer",
                "explanation": "Explanation text",
                "status": "success"
            }
        )
        
        result = await orchestrator.explain_buzzword("transformer")
        
        assert result["buzzword"] == "transformer"
        assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_evaluate_researcher(self):
        """Test evaluate_researcher method"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        orchestrator.researcher_agent.evaluate_researcher = AsyncMock(
            return_value={"evaluation": "Evaluation text", "status": "success"}
        )
        
        publications = [
            {"year": 2020, "title": "Paper 1", "abstract": "Abstract 1"}
        ]
        
        result = await orchestrator.evaluate_researcher(publications, "Dr. Smith")
        
        assert result["status"] == "success"
        assert "evaluation" in result
    
    @pytest.mark.asyncio
    async def test_assess_trend(self):
        """Test assess_trend method"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        orchestrator.trend_agent.assess_trend = AsyncMock(
            return_value={
                "topic": "AI",
                "assessment": "Assessment text",
                "status": "success"
            }
        )
        
        result = await orchestrator.assess_trend("AI", context={"key": "value"})
        
        assert result["status"] == "success"
        assert result["topic"] == "AI"
    
    @pytest.mark.asyncio
    async def test_detect_oversupply(self):
        """Test detect_oversupply method"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        orchestrator.trend_agent.detect_oversupply = AsyncMock(
            return_value={
                "research_area": "ML",
                "oversupply_analysis": "Analysis text",
                "status": "success"
            }
        )
        
        papers = [{"title": "Paper", "year": 2023}]
        result = await orchestrator.detect_oversupply("ML", papers)
        
        assert result["research_area"] == "ML"
        assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_comprehensive_analysis_paper_only(self):
        """Test comprehensive_analysis with paper only"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        orchestrator.analyze_research_paper = AsyncMock(
            return_value={"translation": {}, "analysis": {}}
        )
        
        result = await orchestrator.comprehensive_analysis("Research content")
        
        assert "analyses" in result
        assert "paper" in result["analyses"]
    
    @pytest.mark.asyncio
    async def test_comprehensive_analysis_with_trends(self):
        """Test comprehensive_analysis with trend topics"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        orchestrator.analyze_research_paper = AsyncMock(
            return_value={"translation": {}, "analysis": {}}
        )
        orchestrator.assess_trend = AsyncMock(
            return_value={"topic": "AI", "assessment": "text", "status": "success"}
        )
        
        result = await orchestrator.comprehensive_analysis(
            "Research content",
            trend_topics=["AI", "ML"]
        )
        
        assert "analyses" in result
        assert "trends" in result["analyses"]
        assert len(result["analyses"]["trends"]) == 2
    
    @pytest.mark.asyncio
    async def test_comprehensive_analysis_with_researcher(self):
        """Test comprehensive_analysis with researcher evaluation"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        orchestrator.analyze_research_paper = AsyncMock(
            return_value={"translation": {}, "analysis": {}}
        )
        orchestrator.evaluate_researcher = AsyncMock(
            return_value={"evaluation": "text", "status": "success"}
        )
        
        publications = [{"year": 2020, "title": "Paper"}]
        result = await orchestrator.comprehensive_analysis(
            "Research content",
            researcher_publications=publications,
            researcher_name="Dr. Smith"
        )
        
        assert "analyses" in result
        assert "researcher" in result["analyses"]
    
    def test_get_agent_valid(self):
        """Test get_agent with valid agent name"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        translation_agent = orchestrator.get_agent("translation")
        assert translation_agent == orchestrator.translation_agent
        
        analysis_agent = orchestrator.get_agent("analysis")
        assert analysis_agent == orchestrator.analysis_agent
    
    def test_get_agent_invalid(self):
        """Test get_agent with invalid agent name"""
        orchestrator = DeepLensOrchestrator(
            provider="openai",
            api_key="test_key"
        )
        
        with pytest.raises(ValueError) as exc_info:
            orchestrator.get_agent("nonexistent")
        assert "Unknown agent" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
