import os
from typing import Any, Dict
from app.core.mcp_client import get_mcp_client
from app.app_logging.logger import setup_logger

logger = setup_logger(__name__)

def _get_attr(obj: Any, key: str, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _schema_to_example(schema: Dict[str, Any]) -> str:
    if not isinstance(schema, dict):
        return "{}"

    props = schema.get("properties", {}) or {}
    if not props:
        return "{}"

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

    return str(example).replace("'", '"')


async def generate_mcp_tool_descriptions():
    """
    Generate tool documentation under:
      ../servers/{server_name}/
        index.md
        {tool_name}.md
    """
    logger.info("Generating MCP tool descriptions")
    mcp = get_mcp_client()
    await mcp.initialize()

    # Resolve ../servers relative to orchestrator file
    orchestrator_dir = os.path.dirname(os.path.abspath(__file__))
    servers_root = os.path.abspath(os.path.join(orchestrator_dir, "..", "..", "servers"))
    os.makedirs(servers_root, exist_ok=True)

    for server in mcp.get_available_servers():
        if not mcp.is_server_connected(server):
            continue

        tools = await mcp.list_tools(server)
        if not tools:
            continue

        # Create ../servers/{server_name}/
        server_dir = os.path.join(servers_root, server)
        os.makedirs(server_dir, exist_ok=True)

        index_lines = [
            f"# MCP Tools — {server}",
            "",
            "Read a tool file before calling it.",
            "",
        ]

        for t in tools:
            tool_name = _get_attr(t, "name")
            description = _get_attr(t, "description", "") or ""
            input_schema = _get_attr(t, "inputSchema", {}) or {}

            tool_file = f"{tool_name}.md"
            tool_path = os.path.join(server_dir, tool_file)

            example_args = _schema_to_example(input_schema)

            content = [
                f"# {server}.{tool_name}",
                "",
                description if description else "_No description provided._",
                "",
                "## Input Schema",
                "```json",
                str(input_schema) if input_schema else "{}",
                "```",
                "",
                "## Example Usage",
                "```python",
                f'mcp_call_http(name="{server}.{tool_name}", args={example_args})',
                "```",
                "",
            ]

            with open(tool_path, "w", encoding="utf-8") as f:
                f.write("\n".join(content))

            index_lines.append(f"- `{tool_file}`")

        # Write server-specific index.md
        index_path = os.path.join(server_dir, "index.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("\n".join(index_lines))

