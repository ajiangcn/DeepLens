"""
Custom exceptions for DeepLens
"""


class DeepLensException(Exception):
    """Base exception for all DeepLens errors"""
    pass


class AgentException(DeepLensException):
    """Exception raised by agents during processing"""
    pass


class ConfigurationException(DeepLensException):
    """Exception raised for configuration errors"""
    pass


class APIException(DeepLensException):
    """Exception raised for API-related errors"""
    pass


class ValidationException(DeepLensException):
    """Exception raised for input validation errors"""
    pass
