import asyncio
from app.core.mcp_client import get_mcp_client

mcp_client = get_mcp_client()

async def test_mcp_client():
    await mcp_client.initialize()
    tools = await mcp_client.list_tools("filesystem")
    print(f"list_tools:\n\n {tools} \n\n")
    result = await mcp_client.call_tool(
        server_name="filesystem",
        tool_name="list_directory",
        arguments={"path": "./"}
    )
    print(f"list_directory:\n\n {result} \n\n")

asyncio.run(test_mcp_client())