"""
Read File Tool Wrapper

Wraps the official MCP filesystem server's read_file tool.
Enables agent-generated code to read file contents via MCP.
"""

from app.core.mcp_client import get_mcp_client
from langchain.tools import tool
@tool

async def read_file(path: str) -> str:
    """
    Read file content using official MCP filesystem server.
    
    This wrapper calls the underlying MCP server's read_file tool
    and returns the file content as a string.
    
    Args:
        path: Path to file (e.g., "data.csv", "./folder/file.txt")
        
    Returns:
        File content as string
        
    Example:
        content = await read_file("Sales_Records.csv")
        lines = content.split('\\n')
        print(lines[0])  # Print first line
    """
    # Get singleton MCP client instance
    mcp_client = get_mcp_client()
    
    # Call official MCP filesystem server's read_file tool
    result = await mcp_client.call_tool(
        server_name="filesystem",
        tool_name="read_file",
        arguments={"path": path}
    )
    
    # Extract and return text content from MCP response
    return result.content[0].text

