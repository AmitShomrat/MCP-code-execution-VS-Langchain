"""
Write file tool wrapper.
"""
from typing import Dict, Any
from ._request import make_request, BASE_URL, TIMEOUT


def write_file(path: str, content: str, base_url: str = BASE_URL, timeout: int = TIMEOUT) -> Dict[str, Any]:
    """
    Write content to a file at the specified path.
    
    Args:
        path: Path to the file to write
        content: Content to write to the file
        base_url: Base URL of the API (default: http://localhost:8080)
        timeout: Request timeout in seconds (default: 30)
        
    Returns:
        Dictionary with success, result, and message
        
    Example:
        >>> from tools_client import write_file
        >>> response = write_file("/data/output.txt", "Hello World")
        >>> if response['success']:
        ...     print("File written successfully")
    """
    data = {"path": path, "content": content}
    return make_request("POST", "/tools/write_file", data, base_url=base_url, timeout=timeout)

