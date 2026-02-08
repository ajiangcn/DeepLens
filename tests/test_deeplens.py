"""
Unit tests for DeepLens agents and utilities
"""

import pytest
from deeplens.base_agent import BaseAgent
from deeplens.registry import AgentRegistry, register_agent
from deeplens.config import DeepLensConfig, AgentConfig
from deeplens.utils import format_response, validate_input, truncate_text
from deeplens.exceptions import ValidationException


# Test Agent Registry
class TestAgentRegistry:
    """Tests for the agent registry system"""
    
    def test_register_agent(self):
        """Test registering an agent"""
        @register_agent("test_agent")
        class TestAgent(BaseAgent):
            def _get_system_prompt(self):
                return "Test prompt"
        
        # Check if registered
        assert "test_agent" in AgentRegistry.list_agents()
        assert AgentRegistry.get("test_agent") == TestAgent
        
        # Cleanup
        AgentRegistry.unregister("test_agent")
    
    def test_list_agents(self):
        """Test listing all agents"""
        agents = AgentRegistry.list_agents()
        assert isinstance(agents, list)
        # Should have the built-in agents
        assert "translation" in agents
        assert "analysis" in agents


# Test Configuration
class TestConfiguration:
    """Tests for configuration management"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = DeepLensConfig()
        assert config.model == "gpt-4"
        assert config.temperature == 0.7
        assert config.ui_port == 7860


# Test Utilities
class TestUtilities:
    """Tests for utility functions"""
    
    def test_format_response_json(self):
        """Test JSON formatting"""
        data = {"key": "value", "number": 42}
        result = format_response(data, format_type="json")
        assert '"key"' in result
        assert '"value"' in result
    
    def test_truncate_text(self):
        """Test text truncation"""
        long_text = "a" * 200
        result = truncate_text(long_text, max_length=50)
        assert len(result) == 50
        assert result.endswith("...")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
