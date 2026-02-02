async def test_mcp_client():
    """
    Test MCP client initialization and list tools.
    """
    from app.core.mcp_client import get_mcp_client
    mcp_client = get_mcp_client()
    await mcp_client.initialize()
    tools = await mcp_client.list_tools("filesystem")
    print(f"list_tools:\n\n {tools} \n\n")
    result = await mcp_client.call_tool(
        server_name="filesystem",
        tool_name="list_directory",
        arguments={"path": "./"}
    )
    print(f"list_directory:\n\n {result} \n\n")

async def test_ce_benchmark_init_cleanup():
    """
    Test code execution benchmark initialization and cleanup.
    """
    from app.benchmarks import CodeExecutionBenchmark
    
    benchmark = CodeExecutionBenchmark()
    
    try:
        # All in one event loop context
        await benchmark.initialize_async()
        result = await benchmark.run_benchmark_async("Your query here")
        print(result)
    finally:
        # Cleanup in the SAME event loop
        await benchmark.cleanup_async()

async def test_tmcp_benchmark_init_cleanup():
    """
    Test traditional MCP benchmark initialization and cleanup.
    """
    from app.benchmarks import TraditionalMCPBenchmark
    
    benchmark = TraditionalMCPBenchmark()
    
    try:
        # All in one event loop context
        await benchmark.initialize_async()
        result = await benchmark.run_benchmark_async("Your query here")
        print(result)
    finally:
        # Cleanup in the SAME event loop
        await benchmark.cleanup_async()







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




# To do:
# - Have to unify the dynamic tools description for both traditional (up front) and the generated servers files description for code exec.
# - remove old irrelevant files from the project, once everything is tied and work properly. (checked)
# - make a single env's for docker image name and gateway route. (checked)
# - make sure everything is documented.
# - create the entire workflow scheme diagram.
