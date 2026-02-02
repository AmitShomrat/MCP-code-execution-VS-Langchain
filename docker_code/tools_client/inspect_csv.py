"""
Inspect CSV tool wrapper.
"""
from typing import Dict, Any
from ._request import make_request, BASE_URL, TIMEOUT


def inspect_csv(path: str, base_url: str = BASE_URL, timeout: int = TIMEOUT) -> Dict[str, Any]:
    """
    Inspect a CSV file and return its structure and preview.
    
    Args:
        path: Path to the CSV file to inspect
        base_url: Base URL of the API (default: http://localhost:8080)
        timeout: Request timeout in seconds (default: 30)
        
    Returns:
        Dictionary with success, result (columns, row_count, preview), and message
        
    Example:
        >>> from tools_client import inspect_csv
        >>> response = inspect_csv("/data/sales.csv")
        >>> if response['success']:
        ...     print(f"Columns: {response['result']['columns']}")
        ...     print(f"Rows: {response['result']['row_count']}")
    """
    data = {"path": path}
    return make_request("POST", "/tools/inspect_csv", data, base_url=base_url, timeout=timeout)

