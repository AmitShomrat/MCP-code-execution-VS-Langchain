"""
Write File Tool Wrapper

Wraps the official MCP filesystem server's write_file tool.
Enables agent-generated code to write content to files via MCP.
"""

from app.core.mcp_client import get_mcp_client
from langchain.tools import tool


# Core function - can be called directly as a regular async function
async def write_file(path: str, content: str) -> str:
    """
    Write content to file using official MCP filesystem server.
    
    This wrapper calls the underlying MCP server's write_file tool
    and returns a success message.
    
    Args:
        path: Path to file (e.g., "output.txt", "./results/data.csv")
        content: Content to write to the file
        
    Returns:
        Success message from MCP server
        
    Example:
        result = await write_file_func("output.txt", "Hello World")
        print(result)  # Print success message
    """
    # Get singleton MCP client instance
    mcp_client = get_mcp_client()
    
    # Call official MCP filesystem server's write_file tool
    result = await mcp_client.call_tool(
        server_name="filesystem",
        tool_name="write_file",
        arguments={"path": path, "content": content}
    )
    
    # Extract and return result message from MCP response
    return result.content[0].text


# LangChain tool version - for use with agents
@tool
async def write_file_decorated(path: str, content: str) -> str:
    """
    Write content to file using official MCP filesystem server.
    
    This wrapper calls the underlying MCP server's write_file tool
    and returns a success message.
    
    Args:
        path: Path to file (e.g., "output.txt", "./results/data.csv")
        content: Content to write to the file
        
    Returns:
        Success message from MCP server
        
    Example:
        result = await write_file("output.txt", "Hello World")
        print(result)  # Print success message
    """
    return await write_file(path, content)

