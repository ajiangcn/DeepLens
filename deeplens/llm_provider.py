"""
LLM Provider: Flexible interface for multiple LLM providers
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import os
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    COHERE = "cohere"


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """
        Get chat completion from LLM
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Response text from LLM
        """
        pass


class LiteLLMClient(BaseLLMClient):
    """
    LLM client using LiteLLM for unified interface across providers
    """
    
    def __init__(
        self,
        provider: LLMProvider = LLMProvider.OPENAI,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """
        Initialize LiteLLM client
        
        Args:
            provider: LLM provider to use
            model: Model name/identifier
            api_key: API key for the provider
            api_base: Base URL for API (e.g., Azure endpoint)
            api_version: API version (for Azure)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional provider-specific parameters
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.api_base = api_base
        self.api_version = api_version
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra_params = kwargs
        
        # Set environment variables for LiteLLM
        self._setup_environment()
    
    def _setup_environment(self):
        """Setup environment variables for LiteLLM"""
        if self.api_key:
            if self.provider == LLMProvider.OPENAI:
                os.environ["OPENAI_API_KEY"] = self.api_key
            elif self.provider == LLMProvider.AZURE_OPENAI:
                os.environ["AZURE_API_KEY"] = self.api_key
                if self.api_base:
                    os.environ["AZURE_API_BASE"] = self.api_base
                if self.api_version:
                    os.environ["AZURE_API_VERSION"] = self.api_version
            elif self.provider == LLMProvider.ANTHROPIC:
                os.environ["ANTHROPIC_API_KEY"] = self.api_key
            elif self.provider == LLMProvider.GEMINI:
                os.environ["GEMINI_API_KEY"] = self.api_key
            elif self.provider == LLMProvider.COHERE:
                os.environ["COHERE_API_KEY"] = self.api_key
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """
        Get chat completion using LiteLLM
        
        Args:
            messages: List of message dicts
            **kwargs: Override parameters for this call
            
        Returns:
            Response text from LLM
        """
        try:
            import litellm
            
            # Prepare parameters
            params = {
                "model": self._get_model_identifier(),
                "messages": messages,
                "temperature": kwargs.get("temperature", self.temperature),
            }
            
            if self.max_tokens or kwargs.get("max_tokens"):
                params["max_tokens"] = kwargs.get("max_tokens", self.max_tokens)
            
            # Add provider-specific params
            params.update(self.extra_params)
            params.update(kwargs)
            
            # Call LiteLLM
            response = await litellm.acompletion(**params)
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"LLM API call failed: {str(e)}")
    
    def _get_model_identifier(self) -> str:
        """Get the full model identifier for LiteLLM"""
        if self.provider == LLMProvider.AZURE_OPENAI:
            # Azure format: azure/<deployment_name>
            return f"azure/{self.model}"
        elif self.provider == LLMProvider.ANTHROPIC:
            # Anthropic format: claude-<version>
            return self.model if self.model.startswith("claude-") else f"claude-{self.model}"
        elif self.provider == LLMProvider.GEMINI:
            # Gemini format: gemini/<model>
            return f"gemini/{self.model}" if not self.model.startswith("gemini/") else self.model
        else:
            # Default format (OpenAI, Cohere, etc.)
            return self.model


def create_llm_client(
    provider: str = "openai",
    model: str = "gpt-4",
    api_key: Optional[str] = None,
    **kwargs
) -> BaseLLMClient:
    """
    Factory function to create LLM client
    
    Args:
        provider: Provider name (openai, azure_openai, anthropic, etc.)
        model: Model identifier
        api_key: API key for provider
        **kwargs: Additional configuration
        
    Returns:
        Initialized LLM client
    """
    provider_enum = LLMProvider(provider.lower())
    
    return LiteLLMClient(
        provider=provider_enum,
        model=model,
        api_key=api_key,
        **kwargs
    )
