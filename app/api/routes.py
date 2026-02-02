"""
FastAPI routes for MCP benchmark comparison dashboard.

This module defines all API endpoints for running benchmarks,
retrieving results, and serving the web interface.
"""
from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.models import (
    QueryRequest,
    BenchmarkResponse,
    ComparisonResponse,
    HealthResponse
)
from app.benchmarks.traditional_mcp import TraditionalMCPBenchmark
from app.benchmarks.code_execution_mcp import CodeExecutionBenchmark
from app.utils import BenchmarkStorage
from app.app_logging.logger import setup_logger
from app.core import get_mcp_client, get_docker_executor

# Initialize logger for tracking API operations
logger = setup_logger(__name__)

# Initialize benchmark storage handler
storage = BenchmarkStorage()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - startup and shutdown.
    
    Startup: Log server initialization
    Shutdown: Cleanup MCP connections and Docker containers
    """
    # Startup
    logger.info("=" * 80)
    logger.info("FastAPI Application Starting Up")
    logger.info("=" * 80)
    
    # Start Docker executor
    docker_executor = get_docker_executor()
    await docker_executor.start_container()
    
    yield
    
    # Shutdown
    logger.info("=" * 80)
    logger.info("FastAPI Application Shutting Down")
    logger.info("Cleaning up resources...")
    logger.info("=" * 80)
    
    try:
        # Close MCP client singleton
        mcp_client = get_mcp_client()
        if mcp_client.initialized:
            logger.info("Closing MCP client connections...")
            await mcp_client.close()
            logger.info("MCP connections closed")
        
        # Cleanup Docker executor if it exists
        if docker_executor is not None:
            logger.info("Stopping Docker container...")
            await docker_executor.cleanup()
            logger.info("Docker container stopped")
        
        logger.info("Server shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown cleanup: {str(e)}")

# Create FastAPI application instance with metadata and lifecycle management
app = FastAPI(
    title="MCP Benchmark Dashboard API",
    description="Compare Traditional MCP vs Code Execution MCP performance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define directory paths for static files and data storage
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"

# Define JSON file paths for storing benchmark results
TRADITIONAL_RESULTS_PATH = DATA_DIR / "traditional_mcp_results.json"
CODE_EXEC_RESULTS_PATH = DATA_DIR / "code_execution_results.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Mount static files directory if it exists
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=FileResponse)
async def serve_dashboard():
    """
    Serve the main dashboard HTML page.
    
    Returns:
        HTML file response with the dashboard interface
    """
    # Construct path to HTML file
    html_path = STATIC_DIR / "index.html"
    
    # Check if HTML file exists
    if not html_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard HTML file not found"
        )
    
    # Return HTML file as response
    return FileResponse(html_path)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        HealthResponse with current status and timestamp
    """
    # Return health status with current timestamp
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/traditional-mcp", response_model=BenchmarkResponse)
async def run_traditional_mcp_benchmark(request: QueryRequest):
    """
    Execute Traditional MCP benchmark for the given query.
    
    This endpoint:
    1. Initializes Traditional MCP benchmark
    2. Runs the benchmark with the provided query
    3. Saves results to JSON file
    4. Returns benchmark results
    
    Args:
        request: QueryRequest containing the user query
        
    Returns:
        BenchmarkResponse with execution results
        
    Raises:
        HTTPException: If benchmark execution fails
    """
    try:
        # Log the benchmark request
        logger.info(f"Running Traditional MCP benchmark for query: {request.query}")
        
        # Create and initialize benchmark instance
        benchmark = TraditionalMCPBenchmark()
        await benchmark.initialize_async()
        
        # Run the benchmark with user query
        result = await benchmark.run_benchmark_async(request.query)
        
        # Save benchmark results to JSON file
        storage.save_result(
            file_path=TRADITIONAL_RESULTS_PATH,
            query=request.query,
            result=result
        )
        
        # Don't close MCP client - it's a singleton shared across requests
        # It will be closed during server shutdown
        
        # Format result to match response model
        formatted_result = storage.format_result(result)
        
        # Return successful response with results
        return BenchmarkResponse(
            success=True,
            approach="traditional_mcp",
            result=formatted_result,
            message="Traditional MCP benchmark completed successfully"
        )
        
    except Exception as e:
        # Log error and raise HTTP exception
        logger.error(f"Traditional MCP benchmark error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Benchmark execution failed: {str(e)}"
        )


@app.post("/code-execution-mcp", response_model=BenchmarkResponse)
async def run_code_execution_mcp_benchmark(request: QueryRequest):
    """
    Execute Code Execution MCP benchmark for the given query.
    
    This endpoint:
    1. Initializes Code Execution MCP benchmark
    2. Runs the benchmark with the provided query
    3. Saves results to JSON file
    4. Returns benchmark results
    
    Args:
        request: QueryRequest containing the user query
        
    Returns:
        BenchmarkResponse with execution results
        
    Raises:
        HTTPException: If benchmark execution fails
    """
    try:
        # Log the benchmark request
        logger.info(f"Running Code Execution MCP benchmark for query: {request.query}")
        
        # Create and initialize benchmark instance
        benchmark = CodeExecutionBenchmark()
        await benchmark.initialize_async()
        
        # Store Docker executor reference globally for shutdown cleanup
        global _global_docker_executor
        _global_docker_executor = benchmark.orchestrator.docker_executor
        
        # Run the benchmark with user query
        result = await benchmark.run_benchmark_async(request.query)
        
        # Save benchmark results to JSON file
        storage.save_result(
            file_path=CODE_EXEC_RESULTS_PATH,
            query=request.query,
            result=result
        )
        
        # Cleanup resources (doesn't close shared MCP/Docker - they stay alive)
        await benchmark.cleanup_async()
        
        # Format result to match response model
        formatted_result = storage.format_result(result)
        
        # Return successful response with results
        return BenchmarkResponse(
            success=True,
            approach="code_execution_mcp",
            result=formatted_result,
            message="Code Execution MCP benchmark completed successfully"
        )
        
    except Exception as e:
        # Log error with full traceback
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Code Execution MCP benchmark error:\n{error_details}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Benchmark execution failed: {str(e)}"
        )


@app.get("/compare", response_model=ComparisonResponse)
async def get_benchmark_comparison():
    """
    Retrieve and compare all benchmark results from both approaches.
    
    This endpoint:
    1. Loads Traditional MCP results from JSON
    2. Loads Code Execution MCP results from JSON
    3. Returns combined comparison data
    
    Returns:
        ComparisonResponse with all benchmark results
        
    Raises:
        HTTPException: If loading results fails
    """
    try:
        # Log comparison data request
        logger.info("Loading benchmark comparison data")
        
        # Load results from both approaches
        traditional_results = storage.load_results(TRADITIONAL_RESULTS_PATH)
        code_exec_results = storage.load_results(CODE_EXEC_RESULTS_PATH)
        
        # Return combined results with counts
        return ComparisonResponse(
            success=True,
            traditional_mcp=traditional_results,
            code_execution_mcp=code_exec_results,
            total_count={
                "traditional_mcp": len(traditional_results),
                "code_execution_mcp": len(code_exec_results)
            }
        )
        
    except Exception as e:
        # Log error and raise HTTP exception
        logger.error(f"Comparison data loading error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load comparison data: {str(e)}"
        )
