"""
DeepLens: A multi-agent system for deep research analysis
"""

__version__ = "0.2.0"
__author__ = "DeepLens Team"

from .orchestrator import DeepLensOrchestrator
from .config import DeepLensConfig, AgentConfig
from .base_agent import BaseAgent
from .registry import AgentRegistry, register_agent
from .exceptions import (
    DeepLensException,
    AgentException,
    ConfigurationException,
    APIException,
    ValidationException
)

__all__ = [
    "DeepLensOrchestrator",
    "DeepLensConfig",
    "AgentConfig",
    "BaseAgent",
    "AgentRegistry",
    "register_agent",
    "DeepLensException",
    "AgentException",
    "ConfigurationException",
    "APIException",
    "ValidationException",
]
