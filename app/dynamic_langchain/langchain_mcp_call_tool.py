# app/langchain/mcp_dynamic_tool.py
from typing import Any, Dict
from langchain.tools import tool
from pydantic import BaseModel, Field
from app.core.mcp_client import get_mcp_client

class MCPCallInput(BaseModel):
    name: str = Field(..., description="The fully-qualified name of the MCP tool to call")
    args: Dict[str, Any] = Field(..., description="The arguments to pass to the MCP tool")

@tool("mcp_call", args_schema=MCPCallInput)
async def mcp_call(name: str, args: Dict[str, Any]) -> Any:
    """
    Call an MCP tool by fully-qualified name "<server>.<tool>".
    Expected inputs:
      - name: str
      - args: dict
    """
    server_name, tool_name = name.split(".", 1)

    mcp = get_mcp_client()
    await mcp.initialize()

    result = await mcp.call_tool(server_name=server_name, tool_name=tool_name, arguments=args)

    content = getattr(result, "content", None)
    if content:
        texts = [getattr(c, "text", "") for c in content if getattr(c, "text", None)]
        return "\n".join(texts) if texts else result

    return result
