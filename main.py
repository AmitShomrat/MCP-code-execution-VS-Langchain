"""
FastAPI application entry point for MCP Benchmark Dashboard.

This module serves as the main entry point for the web application.
Run with: python main.py
"""
import os
import uvicorn
import multiprocessing
from multiprocessing import Process
from app.app_logging.logger import setup_logger 
# Initialize logger for application startup
logger = setup_logger(__name__)


def start_main_server():
    """
    Start the main FastAPI server (Dashboard).
    
    Configuration:
    - Host: 0.0.0.0 (accessible from network)
    - Port: 8000
    - Reload: False (disabled for multiprocessing)
    - Log level: info
    """
    uvicorn.run(
        "app.api.routes:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )


def start_gateway_server():
    """
    Start the MCP Gateway server.
    
    Configuration:
    - Host: 0.0.0.0 (accessible from network)
    - Port: 8085
    - Reload: False (disabled for multiprocessing)
    - Log level: info
    """
    uvicorn.run(
        "docker_code.mcp_gateway_server:app",
        host="localhost",
        port=8085,
        reload=False,
        log_level="info"
    )


import asyncio
from app.core import get_mcp_client
async def serve(app, host, port):
    config = uvicorn.Config(app, host=host, port=port, loop = "asyncio", lifespan="on", log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main(routes_port=8000, gateway_port=8080, dev_mode: bool = False):
    global _mcp_client
    _mcp_client = await get_mcp_client()
    try:
        os.environ["DEV_MODE"] = str(dev_mode)
        await asyncio.gather(
            serve("app.api.routes:app", "0.0.0.0", routes_port),
            serve("docker_code.mcp_gateway_server:app", "localhost", gateway_port)
        )
    finally:
        await _mcp_client.close()

if __name__ == "__main__":
    asyncio.run(main())


    # We have to unpack then to tag sensetive fields. (immutable object)
    # Then the given privileges to the a third party Analysis.

    