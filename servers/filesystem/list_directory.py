"""
List Directory Tool Wrapper

Wraps the official MCP filesystem server's list_directory tool.
Enables agent-generated code to list directory contents via MCP.
"""

from app.core.mcp_client import get_mcp_client
from langchain.tools import tool


# Core function - can be called directly as a regular async function
async def list_directory(path: str) -> list:
    """
    List directory contents using official MCP filesystem server.
    
    This wrapper calls the underlying MCP server's list_directory tool
    and returns a list of files and directories.
    
    Args:
        path: Directory path (e.g., "./", "./data", "./results")
        
    Returns:
        List of file and directory names
        
    Example:
        files = await list_directory_func("./data")
        csv_files = [f for f in files if f.endswith('.csv')]
        print(csv_files)
    """
    # Get singleton MCP client instance
    mcp_client = get_mcp_client()
    await mcp_client.initialize() # For debugging purposes (idealy the mcp_client should be initialized in the main.py file)
    
    # Call official MCP filesystem server's list_directory tool
    result = await mcp_client.call_tool(
        server_name="filesystem",
        tool_name="list_directory",
        arguments={"path": path}
    )
    
    # Extract text content from MCP response
    content = result.content[0].text
    
    # Parse content into list of items, filtering empty lines
    items = [line.strip() for line in content.split('\n') if line.strip()]
    
    return items


# LangChain tool version - for use with agents
@tool
async def list_directory_decorated(path: str) -> list:
    """
    List directory contents using official MCP filesystem server.
    
    This wrapper calls the underlying MCP server's list_directory tool
    and returns a list of files and directories.
    
    Args:
        path: Directory path (e.g., "./", "./data", "./results")
        
    Returns:
        List of file and directory names
        
    Example:
        files = await list_directory("./data")
        csv_files = [f for f in files if f.endswith('.csv')]
        print(csv_files)
    """
    return await list_directory(path)
