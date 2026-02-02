"""
Common HTTP request helper for tools client.
"""
import requests
from typing import Dict, Any, Optional


# Default configuration
BASE_URL = "http://host.docker.internal:8080"
TIMEOUT = 30


def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    base_url: str = BASE_URL,
    timeout: int = TIMEOUT
) -> Dict[str, Any]:
    """
    Make an HTTP request to the tools bridge API.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint path
        data: Optional request data
        base_url: Base URL of the API
        timeout: Request timeout in seconds
        
    Returns:
        Response JSON as dictionary
        
    Raises:
        Exception: If the request fails
    """
    url = f"{base_url.rstrip('/')}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request to {endpoint} failed: {str(e)}")

