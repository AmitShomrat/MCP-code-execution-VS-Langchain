"""
List available tools wrapper.
"""
from typing import Dict, Any
from ._request import make_request, BASE_URL, TIMEOUT


def list_available_tools(base_url: str = BASE_URL, timeout: int = TIMEOUT) -> Dict[str, Any]:
    """
    Get list of all available tools from the API.
    
    Args:
        base_url: Base URL of the API (default: http://localhost:8080)
        timeout: Request timeout in seconds (default: 30)
    
    Returns:
        Dictionary containing list of available tools with their descriptions
        
    Example:
        >>> from tools_client import list_available_tools
        >>> tools = list_available_tools()
        >>> for tool in tools['tools']:
        ...     print(f"{tool['name']}: {tool['description']}")
    """
    return make_request("GET", "/tools/available", base_url=base_url, timeout=timeout)

