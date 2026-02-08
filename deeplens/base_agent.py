"""
Base Agent: Abstract base class for all DeepLens agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .llm_provider import BaseLLMClient


class BaseAgent(ABC):
    """
    Abstract base class for all DeepLens agents.
    Provides common functionality and enforces consistent interface.
    """
    
    def __init__(self, llm_client: BaseLLMClient, name: str = None):
        """
        Initialize the base agent
        
        Args:
            llm_client: LLM client instance for making API calls
            name: Agent name (defaults to class name)
        """
        self.llm_client = llm_client
        self.name = name or self.__class__.__name__
        self.system_prompt = self._get_system_prompt()
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent.
        Must be implemented by subclasses.
        
        Returns:
            System prompt string
        """
        pass
    
    async def invoke_prompt(
        self, 
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Common method to invoke LLM with a prompt
        
        Args:
            prompt: User prompt to send
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            LLM response as string
        """
        # Construct messages for chat completion
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Prepare kwargs
            kwargs = {}
            if temperature is not None:
                kwargs["temperature"] = temperature
            if max_tokens is not None:
                kwargs["max_tokens"] = max_tokens
            
            result = await self.llm_client.chat_completion(messages, **kwargs)
            return str(result)
        except Exception as e:
            return self._handle_error(e, "invoke_prompt")
    
    def _handle_error(self, error: Exception, context: str = "") -> str:
        """
        Handle errors in a consistent way
        
        Args:
            error: The exception that occurred
            context: Context about where the error occurred
            
        Returns:
            Error message string
        """
        error_msg = f"Error in {self.name}"
        if context:
            error_msg += f" ({context})"
        error_msg += f": {str(error)}"
        return error_msg
    
    def get_capabilities(self) -> Dict[str, str]:
        """
        Get a description of this agent's capabilities
        
        Returns:
            Dictionary mapping method names to descriptions
        """
        return {
            "name": self.name,
            "description": self.__doc__ or "No description available"
        }
