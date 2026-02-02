"""
List directory tool wrapper.
"""
from typing import Dict, Any
from ._request import make_request, BASE_URL, TIMEOUT


def list_directory(path: str, base_url: str = BASE_URL, timeout: int = TIMEOUT) -> Dict[str, Any]:
    """
    List files and directories at the specified path.
    
    Args:
        path: Path to the directory to list
        base_url: Base URL of the API (default: http://localhost:8080)
        timeout: Request timeout in seconds (default: 30)
        
    Returns:
        Dictionary with success, result, and message
        
    Example:
        >>> from tools_client import list_directory
        >>> response = list_directory("/data")
        >>> if response['success']:
        ...     print(response['result'])
    """
    data = {"path": path}
    return make_request("POST", "/tools/list_directory", data, base_url=base_url, timeout=timeout)

