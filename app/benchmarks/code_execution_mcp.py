"""
Code Execution MCP Benchmark wrapper.

This module provides a benchmark wrapper around the Code Execution MCP approach,
where the LLM generates code that makes MCP calls programmatically.
"""
from typing import Dict, Any

from app.core.orchestrator import RealMCPOrchestrator
from app.app_logging.logger import setup_logger

# Initialize logger for tracking benchmark operations
logger = setup_logger(__name__)


class CodeExecutionBenchmark:
    """
    Wrapper for Code Execution MCP benchmark.
    
    This class wraps the RealMCPOrchestrator to provide a consistent
    interface with the TraditionalMCPBenchmark for API usage.
    
    The code execution approach:
    1. LLM generates Python code
    2. Code makes MCP calls programmatically
    3. Code is executed in sandbox
    4. Results are returned
    """
    
    def __init__(self, mcp_config_path: str = None):
        """
        Initialize Code Execution Benchmark.
        
        Args:
            mcp_config_path: Path to MCP configuration file (optional)
        """
        # Create orchestrator instance with optional config path
        self.orchestrator = RealMCPOrchestrator(mcp_config_path=mcp_config_path)
        
        # Log initialization
        logger.info("Code Execution MCP Benchmark initialized")
    
    async def initialize_async(self):
        """
        Initialize MCP connections asynchronously.
        
        This method initializes the underlying orchestrator which:
        1. Connects to MCP servers
        2. Discovers available tools
        3. Prepares code executor
        """
        # Log initialization start
        logger.info("Initializing Code Execution MCP Benchmark")
        
        # Initialize the orchestrator
        await self.orchestrator.initialize_async()
    
    async def run_benchmark_async(self, query: str, max_turns: int = 3) -> Dict[str, Any]:
        """
        Run code execution MCP benchmark for the given query.
        
        This method:
        1. Passes query to orchestrator
        2. Orchestrator runs multi-turn conversation
        3. Returns formatted benchmark results
        
        Args:
            query: User query to process
            max_turns: Maximum number of LLM turns allowed
            
        Returns:
            Dictionary with benchmark results:
                - success: Execution success status
                - output: Final output from code execution
                - error: Error message if any
                - time: Total execution time in seconds
                - llm_calls: List of LLM call details with tokens
                - tokens: Total token usage across all calls
        """
        # Log benchmark start
        logger.info(f"Running Code Execution MCP benchmark for query: {query}")
        
        # Run multi-turn conversation through orchestrator
        result = await self.orchestrator.run_multi_turn_async(
            user_query=query,
            max_turns=max_turns
        )
        
        # Log benchmark completion
        logger.info("Code Execution MCP benchmark completed")
        
        # Return results
        return result
    
    async def cleanup_async(self):
        """
        Cleanup MCP connections and resources.
        
        This method:
        1. Closes MCP client connections
        2. Releases any held resources
        """
        # Log cleanup start
        logger.info("Cleaning up Code Execution MCP Benchmark")
        
        # Cleanup orchestrator resources
        await self.orchestrator.cleanup_async()
