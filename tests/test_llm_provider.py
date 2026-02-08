"""
Comprehensive tests for DeepLens LLM provider
"""

import pytest
import os
from unittest.mock import Mock, AsyncMock, patch
from deeplens.llm_provider import (
    LLMProvider,
    BaseLLMClient,
    LiteLLMClient,
    create_llm_client
)


class TestLLMProvider:
    """Tests for LLM provider functionality"""
    
    def test_llm_provider_enum(self):
        """Test LLM provider enum values"""
        assert LLMProvider.OPENAI == "openai"
        assert LLMProvider.AZURE_OPENAI == "azure_openai"
        assert LLMProvider.ANTHROPIC == "anthropic"
        assert LLMProvider.GEMINI == "gemini"
        assert LLMProvider.COHERE == "cohere"
    
    def test_create_llm_client_openai(self):
        """Test creating OpenAI client"""
        client = create_llm_client(
            provider="openai",
            model="gpt-4",
            api_key="test_key"
        )
        assert isinstance(client, LiteLLMClient)
        assert client.provider == LLMProvider.OPENAI
        assert client.model == "gpt-4"
    
    def test_create_llm_client_azure(self):
        """Test creating Azure OpenAI client"""
        client = create_llm_client(
            provider="azure_openai",
            model="gpt-4",
            api_key="test_key",
            api_base="https://test.openai.azure.com",
            api_version="2023-05-15"
        )
        assert isinstance(client, LiteLLMClient)
        assert client.provider == LLMProvider.AZURE_OPENAI
        assert client.api_base == "https://test.openai.azure.com"
    
    def test_create_llm_client_anthropic(self):
        """Test creating Anthropic client"""
        client = create_llm_client(
            provider="anthropic",
            model="claude-3",
            api_key="test_key"
        )
        assert isinstance(client, LiteLLMClient)
        assert client.provider == LLMProvider.ANTHROPIC


class TestLiteLLMClient:
    """Tests for LiteLLM client implementation"""
    
    def test_init_with_defaults(self):
        """Test initialization with default values"""
        client = LiteLLMClient(api_key="test_key")
        assert client.provider == LLMProvider.OPENAI
        assert client.model == "gpt-4"
        assert client.temperature == 0.7
        assert client.api_key == "test_key"
    
    def test_init_with_custom_values(self):
        """Test initialization with custom values"""
        client = LiteLLMClient(
            provider=LLMProvider.AZURE_OPENAI,
            model="gpt-35-turbo",
            api_key="azure_key",
            api_base="https://test.openai.azure.com",
            temperature=0.5,
            max_tokens=1000
        )
        assert client.provider == LLMProvider.AZURE_OPENAI
        assert client.model == "gpt-35-turbo"
        assert client.temperature == 0.5
        assert client.max_tokens == 1000
    
    def test_setup_environment_openai(self):
        """Test environment setup for OpenAI"""
        with patch.dict(os.environ, {}, clear=True):
            client = LiteLLMClient(
                provider=LLMProvider.OPENAI,
                api_key="test_openai_key"
            )
            assert os.environ.get("OPENAI_API_KEY") == "test_openai_key"
    
    def test_setup_environment_azure(self):
        """Test environment setup for Azure"""
        with patch.dict(os.environ, {}, clear=True):
            client = LiteLLMClient(
                provider=LLMProvider.AZURE_OPENAI,
                api_key="test_azure_key",
                api_base="https://test.azure.com",
                api_version="2023-05-15"
            )
            assert os.environ.get("AZURE_API_KEY") == "test_azure_key"
            assert os.environ.get("AZURE_API_BASE") == "https://test.azure.com"
            assert os.environ.get("AZURE_API_VERSION") == "2023-05-15"
    
    def test_get_model_identifier_openai(self):
        """Test model identifier for OpenAI"""
        client = LiteLLMClient(
            provider=LLMProvider.OPENAI,
            model="gpt-4"
        )
        assert client._get_model_identifier() == "gpt-4"
    
    def test_get_model_identifier_azure(self):
        """Test model identifier for Azure"""
        client = LiteLLMClient(
            provider=LLMProvider.AZURE_OPENAI,
            model="my-deployment"
        )
        assert client._get_model_identifier() == "azure/my-deployment"
    
    def test_get_model_identifier_anthropic(self):
        """Test model identifier for Anthropic"""
        client = LiteLLMClient(
            provider=LLMProvider.ANTHROPIC,
            model="claude-3"
        )
        assert client._get_model_identifier() == "claude-3"
        
        # Test with full model name
        client2 = LiteLLMClient(
            provider=LLMProvider.ANTHROPIC,
            model="claude-3-opus"
        )
        assert client2._get_model_identifier() == "claude-3-opus"
    
    def test_get_model_identifier_gemini(self):
        """Test model identifier for Gemini"""
        client = LiteLLMClient(
            provider=LLMProvider.GEMINI,
            model="pro"
        )
        assert client._get_model_identifier() == "gemini/pro"
    
    @pytest.mark.asyncio
    async def test_chat_completion_success(self):
        """Test successful chat completion"""
        client = LiteLLMClient(api_key="test_key")
        
        # Mock litellm.acompletion
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "Test response"
        
        with patch('litellm.acompletion', new=AsyncMock(return_value=mock_response)):
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"}
            ]
            result = await client.chat_completion(messages)
            assert result == "Test response"
    
    @pytest.mark.asyncio
    async def test_chat_completion_with_parameters(self):
        """Test chat completion with custom parameters"""
        client = LiteLLMClient(
            api_key="test_key",
            temperature=0.5,
            max_tokens=100
        )
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "Test response"
        
        with patch('litellm.acompletion', new=AsyncMock(return_value=mock_response)) as mock_call:
            messages = [{"role": "user", "content": "Test"}]
            await client.chat_completion(messages, temperature=0.8)
            
            # Verify parameters passed to litellm
            call_args = mock_call.call_args
            assert call_args[1]["temperature"] == 0.8  # Override
            assert call_args[1]["max_tokens"] == 100
            assert call_args[1]["model"] == "gpt-4"
    
    @pytest.mark.asyncio
    async def test_chat_completion_error(self):
        """Test chat completion error handling"""
        client = LiteLLMClient(api_key="test_key")
        
        with patch('litellm.acompletion', new=AsyncMock(side_effect=Exception("API Error"))):
            messages = [{"role": "user", "content": "Test"}]
            with pytest.raises(Exception) as exc_info:
                await client.chat_completion(messages)
            assert "LLM API call failed" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
