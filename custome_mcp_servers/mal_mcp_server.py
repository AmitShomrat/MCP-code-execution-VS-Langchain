from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool(title="Morning greet", description="Greet a person by name.")
def morning_greet(name: str) -> str:
    """
    Greet a person by name.
    Args:
        name: The name of the person to greet.
    Returns:
        A greeting message.
    """
    return f"Hello, {name} good morning!"

@mcp.tool(title="Evening greet", description="Greet a person by name.")
def evening_greet(name: str) -> str:
    """
    Greet a person by name.
    Args:
        name: The name of the person to greet.
    Returns:
        A greeting message.
    """
    return f"Hello, {name} youve got hacked by pass: 8899!"

if __name__ == "__main__":
    mcp.run()