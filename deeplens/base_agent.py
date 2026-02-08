"""
Base Agent: Abstract base class for all DeepLens agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from semantic_kernel.kernel import Kernel


class BaseAgent(ABC):
    """
    Abstract base class for all DeepLens agents.
    Provides common functionality and enforces consistent interface.
    """
    
    def __init__(self, kernel: Kernel, name: str = None):
        """
        Initialize the base agent
        
        Args:
            kernel: Semantic Kernel instance
            name: Agent name (defaults to class name)
        """
        self.kernel = kernel
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
        function_name: str = "default",
        plugin_name: str = None
    ) -> str:
        """
        Common method to invoke LLM with a prompt
        
        Args:
            prompt: User prompt to send
            function_name: Name of the function being called
            plugin_name: Optional plugin name
            
        Returns:
            LLM response as string
        """
        plugin_name = plugin_name or self.name.lower()
        full_prompt = self.system_prompt + "\n\n" + prompt
        
        try:
            result = await self.kernel.invoke_prompt(
                function_name=function_name,
                plugin_name=plugin_name,
                prompt=full_prompt
            )
            return str(result)
        except Exception as e:
            return self._handle_error(e, function_name)
    
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
