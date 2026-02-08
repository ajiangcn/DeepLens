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


def _get_azure_ad_token() -> str:
    """
    Get an Azure AD token for Azure OpenAI using DefaultAzureCredential.
    
    This supports authentication via:
    - Azure CLI (az login)
    - Environment variables (AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
    - Managed Identity
    - Visual Studio Code credential
    - And other methods in the DefaultAzureCredential chain
    
    Returns:
        Bearer token string for Azure OpenAI
    """
    from azure.identity import DefaultAzureCredential
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    return token.token


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
        model: str = "gpt-5.2-chat",
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
            api_key: API key for the provider (not needed for Azure with DefaultAzureCredential)
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
        if self.provider == LLMProvider.AZURE_OPENAI:
            # Azure OpenAI uses DefaultAzureCredential (no API key needed)
            if self.api_base:
                os.environ["AZURE_API_BASE"] = self.api_base
            if self.api_version:
                os.environ["AZURE_API_VERSION"] = self.api_version
        elif self.api_key:
            if self.provider == LLMProvider.OPENAI:
                os.environ["OPENAI_API_KEY"] = self.api_key
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
            }
            
            # For Azure OpenAI, use DefaultAzureCredential token.
            # Note: some Azure models (e.g. gpt-5.2-chat) do NOT support
            # custom temperature — only the default (1.0) is allowed.
            # We therefore skip temperature for Azure unless explicitly
            # overridden by the caller.
            if self.provider == LLMProvider.AZURE_OPENAI:
                params["azure_ad_token"] = _get_azure_ad_token()
                if self.api_base:
                    params["api_base"] = self.api_base.rstrip("/")
                if self.api_version:
                    params["api_version"] = self.api_version
                # Only send temperature if caller explicitly passes it
                if "temperature" in kwargs:
                    params["temperature"] = kwargs.pop("temperature")
            else:
                params["temperature"] = kwargs.pop("temperature", self.temperature)
            
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
    model: str = "gpt-5.2-chat",
    api_key: Optional[str] = None,
    **kwargs
) -> BaseLLMClient:
    """
    Factory function to create LLM client
    
    Args:
        provider: Provider name (openai, azure_openai, anthropic, etc.)
        model: Model identifier
        api_key: API key for provider (not needed for Azure with DefaultAzureCredential)
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
