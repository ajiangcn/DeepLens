"""
Agent Registry: Manages available agents and enables dynamic agent loading
"""

from typing import Dict, Type, List, Optional
from .base_agent import BaseAgent


class AgentRegistry:
    """
    Registry for managing available agents.
    Enables dynamic discovery and instantiation of agents.
    """
    
    _instance = None
    _agents: Dict[str, Type[BaseAgent]] = {}
    
    def __new__(cls):
        """Singleton pattern to ensure single registry instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, name: str, agent_class: Type[BaseAgent]):
        """
        Register an agent class
        
        Args:
            name: Agent identifier
            agent_class: Agent class (must inherit from BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise TypeError(f"{agent_class} must inherit from BaseAgent")
        cls._agents[name] = agent_class
    
    @classmethod
    def unregister(cls, name: str):
        """
        Unregister an agent
        
        Args:
            name: Agent identifier
        """
        if name in cls._agents:
            del cls._agents[name]
    
    @classmethod
    def get(cls, name: str) -> Optional[Type[BaseAgent]]:
        """
        Get an agent class by name
        
        Args:
            name: Agent identifier
            
        Returns:
            Agent class or None if not found
        """
        return cls._agents.get(name)
    
    @classmethod
    def list_agents(cls) -> List[str]:
        """
        List all registered agent names
        
        Returns:
            List of agent names
        """
        return list(cls._agents.keys())
    
    @classmethod
    def get_all(cls) -> Dict[str, Type[BaseAgent]]:
        """
        Get all registered agents
        
        Returns:
            Dictionary of agent name to agent class
        """
        return cls._agents.copy()
    
    @classmethod
    def clear(cls):
        """Clear all registered agents"""
        cls._agents.clear()


def register_agent(name: str):
    """
    Decorator to register an agent class
    
    Usage:
        @register_agent("my_agent")
        class MyAgent(BaseAgent):
            ...
    
    Args:
        name: Agent identifier
    """
    def decorator(agent_class: Type[BaseAgent]):
        AgentRegistry.register(name, agent_class)
        return agent_class
    return decorator
