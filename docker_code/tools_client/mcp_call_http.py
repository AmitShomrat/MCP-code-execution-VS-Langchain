import os, requests
from mcp.types import CallToolResult
MCP_GATEWAY = os.environ["MCP_GATEWAY"] if "MCP_GATEWAY" in os.environ else "http://host.docker.internal:8080" # e.g. http://host.docker.internal:8080

# def mcp_call_http(name: str, args: dict):
#     r = requests.post(f"{MCP_GATEWAY}/mcp/call", json={"name": name, "args": args, "timeout_s": 30}, timeout=35)
#     r.raise_for_status()
#     data = r.json()
#     if not data["ok"]:
#         raise RuntimeError(data["error"])
#     return data.get("content_text")

def mcp_call_http(name: str, args: dict) -> CallToolResult:
    r = requests.post(f"{MCP_GATEWAY}/mcp/call", json={"name": name, "args": args, "timeout_s": 30}, timeout=35)
    r.raise_for_status()
    return CallToolResult(**r.json())
