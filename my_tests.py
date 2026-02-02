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

# Checking tools_bridge.py 
# on terminal run: 
# curl -X GET "http://localhost:8080/health"

# curl -X GET "http://localhost:8080/tools/available"

# curl -X POST "http://localhost:8080/tools/list_directory" \
#   -H "Content-Type: application/json" \
#   -d '{"path": "."}'

# curl -X POST "http://localhost:8080/tools/inspect_csv" \
#   -H "Content-Type: application/json" \
#   -d '{"path": "./data/file.csv"}'

# curl -X POST "http://localhost:8080/tools/read_file" \
#   -H "Content-Type: application/json" \
#   -d '{"path": "./README.md"}'

# # curl -X POST "http://localhost:8080/tools/write_file" \
#   -H "Content-Type: application/json" \
#   -d '{"path": "./output.txt", "content": "Hello World"}'


# Using the tool_bridge from docker with interactive terminal: 
# - Make sure the tool_bridge is running: uv run tools_bridge.py
# Start the conteiner: docker run -it python:3.8 "bash"
# then hit the server using curl with the url 'http://host.docker.internal:8080/tools/list_directory'