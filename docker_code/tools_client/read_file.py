"""
Read file tool wrapper.
"""
from typing import Dict, Any
from ._request import make_request, BASE_URL, TIMEOUT


def read_file(path: str, base_url: str = BASE_URL, timeout: int = TIMEOUT) -> Dict[str, Any]:
    """
    Read contents of a file at the specified path.
    
    Args:
        path: Path to the file to read
        base_url: Base URL of the API (default: http://localhost:8080)
        timeout: Request timeout in seconds (default: 30)
        
    Returns:
        Dictionary with success, result (file contents), and message
        
    Example:
        >>> from tools_client import read_file
        >>> response = read_file("/data/config.txt")
        >>> if response['success']:
        ...     print(response['result'])
    """
    data = {"path": path}
    return make_request("POST", "/tools/read_file", data, base_url=base_url, timeout=timeout)

