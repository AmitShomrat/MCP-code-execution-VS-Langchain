"""
Health check tool wrapper.
"""
from typing import Dict, Any
from ._request import make_request, BASE_URL, TIMEOUT


def health_check(base_url: str = BASE_URL, timeout: int = TIMEOUT) -> Dict[str, Any]:
    """
    Check if the tools bridge API is healthy and running.
    
    Args:
        base_url: Base URL of the API (default: http://localhost:8080)
        timeout: Request timeout in seconds (default: 30)
    
    Returns:
        Dictionary containing status, timestamp, and version
        
    Example:
        >>> from tools_client import health_check
        >>> health = health_check()
        >>> print(health['status'])
        'healthy'
    """
    return make_request("GET", "/health", base_url=base_url, timeout=timeout)

