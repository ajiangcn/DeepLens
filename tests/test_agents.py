"""
Comprehensive tests for DeepLens agents
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from deeplens.base_agent import BaseAgent
from deeplens.agents.translation_agent import TranslationAgent
from deeplens.agents.analysis_agent import AnalysisAgent, ResearchStage
from deeplens.agents.researcher_evaluation_agent import ResearcherEvaluationAgent, ResearcherPattern
from deeplens.agents.trend_assessment_agent import TrendAssessmentAgent, TrendStatus, ProblemType
from deeplens.llm_provider import LiteLLMClient


class MockLLMClient:
    """Mock LLM client for testing"""
    
    async def chat_completion(self, messages, **kwargs):
        """Mock chat completion"""
        return "Mock LLM response"


class TestBaseAgent:
    """Tests for BaseAgent functionality"""
    
    def test_base_agent_is_abstract(self):
        """Test that BaseAgent cannot be instantiated"""
        mock_client = MockLLMClient()
        with pytest.raises(TypeError):
            BaseAgent(mock_client)
    
    def test_concrete_agent_initialization(self):
        """Test concrete agent can be initialized"""
        class ConcreteAgent(BaseAgent):
            def _get_system_prompt(self):
                return "Test system prompt"
        
        mock_client = MockLLMClient()
        agent = ConcreteAgent(mock_client, name="TestAgent")
        
        assert agent.name == "TestAgent"
        assert agent.system_prompt == "Test system prompt"
        assert agent.llm_client == mock_client
    
    def test_agent_default_name(self):
        """Test agent uses class name when name not provided"""
        class MyAgent(BaseAgent):
            def _get_system_prompt(self):
                return "Test"
        
        mock_client = MockLLMClient()
        agent = MyAgent(mock_client)
        assert agent.name == "MyAgent"
    
    @pytest.mark.asyncio
    async def test_invoke_prompt(self):
        """Test invoke_prompt method"""
        class TestAgent(BaseAgent):
            def _get_system_prompt(self):
                return "System prompt"
        
        mock_client = MockLLMClient()
        agent = TestAgent(mock_client)
        
        result = await agent.invoke_prompt("Test prompt")
        assert result == "Mock LLM response"
    
    @pytest.mark.asyncio
    async def test_invoke_prompt_with_parameters(self):
        """Test invoke_prompt with custom parameters"""
        class TestAgent(BaseAgent):
            def _get_system_prompt(self):
                return "System prompt"
        
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(return_value="Response with params")
        agent = TestAgent(mock_client)
        
        result = await agent.invoke_prompt(
            "Test prompt",
            temperature=0.5,
            max_tokens=100
        )
        
        assert result == "Response with params"
        # Verify parameters were passed
        call_args = mock_client.chat_completion.call_args
        assert call_args[1]["temperature"] == 0.5
        assert call_args[1]["max_tokens"] == 100
    
    @pytest.mark.asyncio
    async def test_invoke_prompt_error_handling(self):
        """Test error handling in invoke_prompt"""
        class TestAgent(BaseAgent):
            def _get_system_prompt(self):
                return "System prompt"
        
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(side_effect=Exception("API Error"))
        agent = TestAgent(mock_client, name="TestAgent")
        
        result = await agent.invoke_prompt("Test prompt")
        assert "Error in TestAgent" in result
        assert "API Error" in result
    
    def test_get_capabilities(self):
        """Test get_capabilities method"""
        class TestAgent(BaseAgent):
            """Test agent for testing"""
            def _get_system_prompt(self):
                return "Test"
        
        mock_client = MockLLMClient()
        agent = TestAgent(mock_client, name="TestAgent")
        
        capabilities = agent.get_capabilities()
        assert capabilities["name"] == "TestAgent"
        assert "Test agent for testing" in capabilities["description"]


class TestTranslationAgent:
    """Tests for Translation Agent"""
    
    def test_initialization(self):
        """Test TranslationAgent initialization"""
        mock_client = MockLLMClient()
        agent = TranslationAgent(mock_client)
        
        assert agent.name == "TranslationAgent"
        assert "translating complex research papers" in agent.system_prompt.lower()
    
    @pytest.mark.asyncio
    async def test_translate(self):
        """Test translate method"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(
            return_value="This is a simplified explanation of the research."
        )
        agent = TranslationAgent(mock_client)
        
        result = await agent.translate("Complex technical content")
        
        assert result["status"] == "success"
        assert "simplified" in result
        assert "This is a simplified explanation" in result["simplified"]
    
    @pytest.mark.asyncio
    async def test_explain_buzzword(self):
        """Test explain_buzzword method"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(
            return_value="A transformer is a neural network architecture..."
        )
        agent = TranslationAgent(mock_client)
        
        result = await agent.explain_buzzword("transformer")
        
        assert result["status"] == "success"
        assert result["buzzword"] == "transformer"
        assert "explanation" in result
        assert "transformer" in result["explanation"].lower()


class TestAnalysisAgent:
    """Tests for Analysis Agent"""
    
    def test_initialization(self):
        """Test AnalysisAgent initialization"""
        mock_client = MockLLMClient()
        agent = AnalysisAgent(mock_client)
        
        assert agent.name == "AnalysisAgent"
        assert "research analyst" in agent.system_prompt.lower()
    
    def test_research_stage_enum(self):
        """Test ResearchStage enum"""
        assert ResearchStage.EXPLORATION == "exploration"
        assert ResearchStage.SCALING == "scaling"
        assert ResearchStage.CONVERGENCE == "convergence"
    
    @pytest.mark.asyncio
    async def test_analyze(self):
        """Test analyze method"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(
            return_value="This research is in the scaling stage..."
        )
        agent = AnalysisAgent(mock_client)
        
        result = await agent.analyze("Research content to analyze")
        
        assert result["status"] == "success"
        assert "analysis" in result
    
    @pytest.mark.asyncio
    async def test_analyze_with_context(self):
        """Test analyze with additional context"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(return_value="Analysis with context")
        agent = AnalysisAgent(mock_client)
        
        context = {"related_work": "Previous studies", "citations": 50}
        result = await agent.analyze("Research content", context=context)
        
        assert result["status"] == "success"
        assert "analysis" in result
    
    @pytest.mark.asyncio
    async def test_identify_problem_hierarchy(self):
        """Test identify_problem_hierarchy method"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(
            return_value="Surface: stated problem; Actual: real problem; Fundamental: core issue"
        )
        agent = AnalysisAgent(mock_client)
        
        result = await agent.identify_problem_hierarchy("Research content")
        
        assert result["status"] == "success"
        assert "hierarchy" in result


class TestResearcherEvaluationAgent:
    """Tests for Researcher Evaluation Agent"""
    
    def test_initialization(self):
        """Test ResearcherEvaluationAgent initialization"""
        mock_client = MockLLMClient()
        agent = ResearcherEvaluationAgent(mock_client)
        
        assert agent.name == "ResearcherEvaluationAgent"
        assert "researcher career patterns" in agent.system_prompt.lower()
    
    def test_researcher_pattern_enum(self):
        """Test ResearcherPattern enum"""
        assert ResearcherPattern.TREND_FOLLOWER == "trend_follower"
        assert ResearcherPattern.DEEP_SPECIALIST == "deep_specialist"
        assert ResearcherPattern.ABSTRACTION_UPLEVELER == "abstraction_upleveler"
    
    @pytest.mark.asyncio
    async def test_evaluate_researcher(self):
        """Test evaluate_researcher method"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(
            return_value="This researcher shows pattern of deep specialist..."
        )
        agent = ResearcherEvaluationAgent(mock_client)
        
        publications = [
            {"year": 2020, "title": "Paper 1", "abstract": "Abstract 1"},
            {"year": 2021, "title": "Paper 2", "abstract": "Abstract 2"}
        ]
        
        result = await agent.evaluate_researcher(publications, "Dr. Smith")
        
        assert result["status"] == "success"
        assert "evaluation" in result
    
    @pytest.mark.asyncio
    async def test_evaluate_researcher_without_name(self):
        """Test evaluate_researcher without researcher name"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(return_value="Evaluation result")
        agent = ResearcherEvaluationAgent(mock_client)
        
        publications = [{"year": 2020, "title": "Paper", "abstract": "Abstract"}]
        result = await agent.evaluate_researcher(publications)
        
        assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_compare_researchers(self):
        """Test compare_researchers method"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(
            return_value="Comparison: Researcher 1 vs Researcher 2..."
        )
        agent = ResearcherEvaluationAgent(mock_client)
        
        researchers_data = [
            {"name": "Dr. A", "publications": [{"year": 2020, "title": "Paper A"}]},
            {"name": "Dr. B", "publications": [{"year": 2020, "title": "Paper B"}]}
        ]
        
        result = await agent.compare_researchers(researchers_data)
        
        assert result["status"] == "success"
        assert "comparison" in result


class TestTrendAssessmentAgent:
    """Tests for Trend Assessment Agent"""
    
    def test_initialization(self):
        """Test TrendAssessmentAgent initialization"""
        mock_client = MockLLMClient()
        agent = TrendAssessmentAgent(mock_client)
        
        assert agent.name == "TrendAssessmentAgent"
        assert "technical trends" in agent.system_prompt.lower()
    
    def test_trend_status_enum(self):
        """Test TrendStatus enum"""
        assert TrendStatus.EMERGING == "emerging"
        assert TrendStatus.HYPED == "hyped"
        assert TrendStatus.MATURE == "mature"
        assert TrendStatus.DECLINING == "declining"
        assert TrendStatus.OBSOLETE == "obsolete"
    
    def test_problem_type_enum(self):
        """Test ProblemType enum"""
        assert ProblemType.HARD_PROBLEM == "hard_problem"
        assert ProblemType.ENGINEERING_PROBLEM == "engineering_problem"
        assert ProblemType.SOLVED_PROBLEM == "solved_problem"
        assert ProblemType.FAKE_PROBLEM == "fake_problem"
    
    @pytest.mark.asyncio
    async def test_assess_trend(self):
        """Test assess_trend method"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(
            return_value="This trend is currently hyped but has potential..."
        )
        agent = TrendAssessmentAgent(mock_client)
        
        result = await agent.assess_trend("Large Language Models")
        
        assert result["status"] == "success"
        assert result["topic"] == "Large Language Models"
        assert "assessment" in result
    
    @pytest.mark.asyncio
    async def test_assess_trend_with_context(self):
        """Test assess_trend with additional context"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(return_value="Trend assessment with context")
        agent = TrendAssessmentAgent(mock_client)
        
        context = {"recent_developments": "GPT-4 release", "adoption": "high"}
        result = await agent.assess_trend("LLMs", context=context)
        
        assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_compare_trends(self):
        """Test compare_trends method"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(
            return_value="Comparison of trends on obsolescence risk..."
        )
        agent = TrendAssessmentAgent(mock_client)
        
        trends = ["Trend A", "Trend B", "Trend C"]
        result = await agent.compare_trends(trends, criteria="obsolescence_risk")
        
        assert result["status"] == "success"
        assert result["criteria"] == "obsolescence_risk"
        assert result["trends"] == trends
    
    @pytest.mark.asyncio
    async def test_detect_oversupply(self):
        """Test detect_oversupply method"""
        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(
            return_value="This area shows high saturation with many similar papers..."
        )
        agent = TrendAssessmentAgent(mock_client)
        
        recent_papers = [
            {"title": "Paper 1", "year": 2023},
            {"title": "Paper 2", "year": 2023}
        ]
        
        result = await agent.detect_oversupply("BERT fine-tuning", recent_papers)
        
        assert result["status"] == "success"
        assert result["research_area"] == "BERT fine-tuning"
        assert "oversupply_analysis" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
