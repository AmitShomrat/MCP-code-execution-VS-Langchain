# app/langchain/mcp_catalog.py
from typing import Any, Dict, List, Optional
from app.core.mcp_client import get_mcp_client

def _get(obj: Any, key: str, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)

def _schema_example(input_schema: Optional[Dict[str, Any]]) -> str:
    if not isinstance(input_schema, dict):
        return "{}"
    props = input_schema.get("properties") or {}
    if not props:
        return "{}"
    # Create a tiny example object with placeholder values
    example = {}
    for k, v in props.items():
        t = (v or {}).get("type")
        if t == "string":
            example[k] = "<string>"
        elif t == "integer":
            example[k] = 0
        elif t == "number":
            example[k] = 0.0
        elif t == "boolean":
            example[k] = False
        elif t == "array":
            example[k] = []
        elif t == "object":
            example[k] = {}
        else:
            example[k] = "<value>"
    return str(example).replace("'", '"')  # JSON-ish

async def build_mcp_tool_catalog() -> str:
    """
    Returns a markdown-ish catalog describing available MCP tools
    for use inside a system prompt.
    """
    mcp = get_mcp_client()
    await mcp.initialize()

    lines: List[str] = []
    lines.append("## MCP TOOL CATALOG")
    lines.append("Use the tool `mcp_call(name, args)` to call any MCP tool.")
    lines.append('`name` must be "<server>.<tool>" and `args` must be a JSON object.\n')

    for server in mcp.get_available_servers():
        if not mcp.is_server_connected(server):
            continue

        tools = await mcp.list_tools(server)
        if not tools:
            continue

        lines.append(f"### Server: {server}")
        for t in tools:
            tool_name = _get(t, "name")
            desc = _get(t, "description", "") or ""
            input_schema = _get(t, "inputSchema", None)

            fq = f"{server}.{tool_name}"
            example_args = _schema_example(input_schema)

            # Keep it compact
            if desc:
                lines.append(f"- **{fq}** — {desc}")
            else:
                lines.append(f"- **{fq}**")

            lines.append(f'  - Example: `mcp_call(name="{fq}", args={example_args})`')

        lines.append("")  # blank line between servers

    return "\n".join(lines)
