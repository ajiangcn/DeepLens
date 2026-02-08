"""
Configuration management for DeepLens
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class AgentConfig:
    """Configuration for individual agents"""
    enabled: bool = True
    model: Optional[str] = None  # Override default model
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    custom_prompt: Optional[str] = None


@dataclass
class DeepLensConfig:
    """
    Main configuration for DeepLens system
    """
    # API Configuration
    api_key: Optional[str] = None
    model: str = "gpt-4"
    use_azure: bool = False
    temperature: float = 0.7
    
    # Agent-specific configurations
    agent_configs: Dict[str, AgentConfig] = field(default_factory=dict)
    
    # UI Configuration
    ui_theme: str = "default"
    ui_port: int = 7860
    
    # System Configuration
    max_retries: int = 3
    timeout: int = 60
    verbose: bool = False
    
    @classmethod
    def from_env(cls, env_file: str = ".env") -> "DeepLensConfig":
        """
        Load configuration from environment variables
        
        Args:
            env_file: Path to .env file
            
        Returns:
            DeepLensConfig instance
        """
        load_dotenv(env_file)
        
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            use_azure=os.getenv("USE_AZURE", "false").lower() == "true",
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            ui_port=int(os.getenv("UI_PORT", "7860")),
            verbose=os.getenv("VERBOSE", "false").lower() == "true",
        )
    
    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """
        Get configuration for a specific agent
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            AgentConfig instance
        """
        return self.agent_configs.get(agent_name, AgentConfig())
    
    def set_agent_config(self, agent_name: str, config: AgentConfig):
        """
        Set configuration for a specific agent
        
        Args:
            agent_name: Name of the agent
            config: AgentConfig instance
        """
        self.agent_configs[agent_name] = config
