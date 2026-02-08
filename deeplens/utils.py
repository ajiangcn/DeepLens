"""
Utility functions for DeepLens
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime


def format_response(
    data: Any,
    format_type: str = "json",
    pretty: bool = True
) -> str:
    """
    Format response data for display
    
    Args:
        data: Data to format
        format_type: Format type (json, text, markdown)
        pretty: Whether to pretty-print
        
    Returns:
        Formatted string
    """
    if format_type == "json":
        if pretty:
            return json.dumps(data, indent=2, default=str)
        return json.dumps(data, default=str)
    elif format_type == "text":
        if isinstance(data, dict):
            return "\n".join(f"{k}: {v}" for k, v in data.items())
        return str(data)
    elif format_type == "markdown":
        return format_as_markdown(data)
    return str(data)


def format_as_markdown(data: Dict[str, Any]) -> str:
    """
    Format dictionary as markdown
    
    Args:
        data: Dictionary to format
        
    Returns:
        Markdown formatted string
    """
    lines = []
    for key, value in data.items():
        lines.append(f"## {key.replace('_', ' ').title()}")
        lines.append("")
        if isinstance(value, (list, tuple)):
            for item in value:
                lines.append(f"- {item}")
        elif isinstance(value, dict):
            for k, v in value.items():
                lines.append(f"**{k}**: {v}")
        else:
            lines.append(str(value))
        lines.append("")
    return "\n".join(lines)


def validate_input(
    content: str,
    min_length: int = 1,
    max_length: Optional[int] = None
) -> bool:
    """
    Validate input content
    
    Args:
        content: Content to validate
        min_length: Minimum length
        max_length: Maximum length (None for no limit)
        
    Returns:
        True if valid
        
    Raises:
        ValidationException if invalid
    """
    from .exceptions import ValidationException
    
    if not content or len(content.strip()) < min_length:
        raise ValidationException(
            f"Input must be at least {min_length} characters"
        )
    
    if max_length and len(content) > max_length:
        raise ValidationException(
            f"Input must be at most {max_length} characters"
        )
    
    return True


def add_timestamp(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add timestamp to data dictionary
    
    Args:
        data: Dictionary to add timestamp to
        
    Returns:
        Dictionary with timestamp added
    """
    data["timestamp"] = datetime.utcnow().isoformat()
    return data


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_key_points(text: str, num_points: int = 5) -> List[str]:
    """
    Extract key points from text (simple sentence splitting)
    
    Args:
        text: Text to extract from
        num_points: Number of points to extract
        
    Returns:
        List of key point strings
    """
    # Simple implementation - split by periods and take first sentences
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    return sentences[:num_points]
