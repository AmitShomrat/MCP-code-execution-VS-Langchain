"""
FastAPI application entry point for MCP Benchmark Dashboard.

This module serves as the main entry point for the web application.
Run with: python main.py
"""
import uvicorn

from app.app_logging.logger import setup_logger

# Initialize logger for application startup
logger = setup_logger(__name__)


def main():
    """
    Start the FastAPI server.
    
    Configuration:
    - Host: 0.0.0.0 (accessible from network)
    - Port: 8000
    - Reload: True (auto-reload on code changes)
    - Log level: info
    """
    # Log server startup information
    logger.info("=" * 80)
    logger.info("STARTING MCP BENCHMARK DASHBOARD")
    logger.info("\nServer starting at: http://localhost:8000")
    logger.info("API documentation at: http://localhost:8000/docs")
    logger.info("=" * 80)
    
    # Start uvicorn server with hot reload enabled
    uvicorn.run(
        "app.api.routes:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    # Run the main function when script is executed
    main()
