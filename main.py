"""
FastAPI application entry point for MCP Benchmark Dashboard.

This module serves as the main entry point for the web application.
Run with: python main.py
"""
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
    - Port: 8080
    - Reload: False (disabled for multiprocessing)
    - Log level: info
    """
    uvicorn.run(
        "docker_code.mcp_gateway_server:app",
        host="localhost",
        port=8080,
        reload=False,
        log_level="info"
    )


def main():
    """
    Start both FastAPI servers concurrently using multiprocessing.
    
    Servers:
    - Main Dashboard: http://localhost:8000
    - MCP Gateway: http://localhost:8080
    """
    # Log server startup information
    logger.info("=" * 80)
    logger.info("STARTING MCP BENCHMARK DASHBOARD & GATEWAY")
    logger.info("\nMain server starting at: http://localhost:8000")
    logger.info("API documentation at: http://localhost:8000/docs")
    logger.info("\nGateway server starting at: http://localhost:8080")
    logger.info("Gateway documentation at: http://localhost:8080/docs")
    logger.info("=" * 80)
    
    # Create processes for both servers
    main_process = Process(target=start_main_server, name="MainServer")
    gateway_process = Process(target=start_gateway_server, name="GatewayServer")
    
    try:
        # Start both servers
        main_process.start()
        gateway_process.start()
        
        # Wait for both processes to complete
        main_process.join()
        gateway_process.join()
        
    except KeyboardInterrupt:
        logger.info("\nShutting down servers...")
        # Terminate both processes on keyboard interrupt
        main_process.terminate()
        gateway_process.terminate()
        
        # Wait for processes to terminate
        main_process.join()
        gateway_process.join()
        
        logger.info("Servers shut down successfully")


if __name__ == "__main__":
    # Required for multiprocessing on Windows and macOS
    multiprocessing.set_start_method('spawn', force=True)
    
    # Run the main function when script is executed
    main()
