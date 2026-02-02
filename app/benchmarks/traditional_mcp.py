"""
Traditional MCP Benchmark using LangChain v1 create_agent.

This module implements the traditional approach to MCP where tools are
directly exposed to the LLM through LangChain's agent framework.
"""
# Standard library imports
import asyncio
import time
from typing import Dict, Any
import pandas as pd
from io import StringIO

# LangChain imports for agent framework
from langchain.agents import create_agent
from langchain.tools import tool

# Application imports
from app.app_logging.logger import setup_logger
from app.core.mcp_client import get_mcp_client
from app.config import OPENAI_MODEL
from servers.filesystem import list_directory, inspect_csv, read_file, write_file

# Initialize logger for tracking benchmark operations
logger = setup_logger(__name__)


class TraditionalMCPBenchmark:
    """
    Benchmark Traditional MCP using LangChain v1 create_agent.
    
    This class implements the traditional approach where:
    1. MCP tools are wrapped as LangChain tools
    2. LLM directly calls tools through agent framework
    3. Each tool call requires LLM invocation
    """
    
    def __init__(self):
        """
        Initialize Traditional MCP Benchmark.
        
        Sets up:
        - MCP client for filesystem operations
        - Token usage tracking
        - LLM call tracking
        """
        # Get singleton MCP client instance for filesystem operations
        self.mcp_client = get_mcp_client()
        
        # Initialize token usage tracking dictionary
        self.total_tokens = {"input": 0, "output": 0, "total": 0}
        
        # Initialize LLM call counters
        self.llm_calls = 0
        self.llm_calls_list = []

        # mcp_tools
        self.mcp_tools = [list_directory, inspect_csv, read_file, write_file]
        
    async def initialize_async(self):
        """
        Initialize MCP connections to filesystem server.
        
        This establishes the connection to the MCP server
        that provides file system tools.
        """
        # Initialize MCP client and connect to filesystem server
        await self.mcp_client.initialize()
        
    async def run_benchmark_async(self, query: str) -> Dict[str, Any]:
        """
        Run traditional MCP benchmark with timing and token tracking.
        
        Workflow:
        1. Create MCP tools for agent
        2. Initialize LangChain agent
        3. Execute query through agent
        4. Track token usage and timing
        5. Return formatted results
        
        Args:
            query: User query to process
            
        Returns:
            Dictionary with benchmark results:
                - success: Execution success status
                - output: Final output text
                - time: Total execution time
                - llm_calls: List of LLM call details
                - tokens: Token usage information
        """
        # Reset token tracking for new benchmark run
        self.total_tokens = {"input": 0, "output": 0, "total": 0}
        
        # Reset LLM call counters for new benchmark run
        self.llm_calls = 0
        self.llm_calls_list = []
        
        # Start timing the benchmark execution
        start_time = time.time()
        
        # Log benchmark start with banner
        logger.info(f"\n{'=' * 80}\nTRADITIONAL MCP BENCHMARK (LangChain v1)\n{'=' * 80}\n")
        logger.info(f"Query: {query}\n")
        
        # Initialize LangChain agent with model, tools, and system prompt
        agent = create_agent(
            model=OPENAI_MODEL,
            tools=self.mcp_tools,
            system_prompt=self._get_system_prompt()
        )
        
        try:
            # Invoke agent with user query
            result = await agent.ainvoke({
                "messages": [
                    {"role": "user", "content": query}
                ]
            })
            
            # Initialize variables for output and call tracking
            output = ""
            call_count = 0
            
            # Process agent result messages
            if "messages" in result:
                # Iterate through all messages in result
                for msg in result["messages"]:
                    # Check if message is from AI assistant
                    if hasattr(msg, 'content') and msg.type == "ai":
                        # Extract AI response content
                        output = msg.content
                        call_count += 1
                        
                        # Check if message has token usage metadata
                        if hasattr(msg, 'response_metadata'):
                            token_usage = msg.response_metadata.get('token_usage', {})
                            
                            # Process token usage if available
                            if token_usage:
                                # Extract individual token counts
                                prompt_tokens = token_usage.get('prompt_tokens', 0)
                                completion_tokens = token_usage.get('completion_tokens', 0)
                                total_tokens = token_usage.get('total_tokens', 0)
                                
                                # Accumulate token counts
                                self.total_tokens["input"] += prompt_tokens
                                self.total_tokens["output"] += completion_tokens
                                self.total_tokens["total"] += total_tokens
                                
                                # Append LLM call details to list
                                self.llm_calls_list.append({
                                    "call_number": call_count,
                                    "latency": 0,
                                    "tokens": {
                                        "prompt_tokens": prompt_tokens,
                                        "completion_tokens": completion_tokens,
                                        "total_tokens": total_tokens
                                    }
                                })
                                
                                # Log LLM call details
                                logger.info(f"\n{'=' * 80}\nLLM CALL {call_count}\n{'=' * 80}")
                                logger.info(f"\nTOKEN USAGE (Call {call_count})")
                                logger.info(f"{'=' * 80}")
                                logger.info(f"Input Tokens: {prompt_tokens}")
                                logger.info(f"Output Tokens: {completion_tokens}")
                                logger.info(f"Total Tokens: {total_tokens}")
                                logger.info(f"{'=' * 80}\n")
            
            # Store total LLM call count
            self.llm_calls = call_count
            
            # Calculate total execution time
            total_time = time.time() - start_time
            
            # Calculate average latency per LLM call
            if self.llm_calls > 0:
                avg_latency_per_call = total_time / self.llm_calls
                
                # Update latency for each call in the list
                for call_detail in self.llm_calls_list:
                    call_detail["latency"] = round(avg_latency_per_call, 2)
            
            # Log final results banner
            logger.info(f"\n{'=' * 80}\nFINAL RESULTS\n{'=' * 80}")
            logger.info(f"\nStatus: SUCCESS")
            logger.info(f"\nOutput:\n{'-' * 80}\n{output}\n{'-' * 80}\n")
            
            # Log performance summary
            logger.info(f"\n{'=' * 80}\nPERFORMANCE SUMMARY\n{'=' * 80}")
            logger.info(f"Total Time: {total_time:.2f}s")
            logger.info(f"Total LLM Calls: {self.llm_calls}")
            logger.info(f"{'=' * 80}\n")
            
            # Log token usage summary
            logger.info(f"\n{'=' * 80}\nTOKEN USAGE SUMMARY\n{'=' * 80}")
            logger.info(f"\n{'-' * 80}\nTOTAL TOKENS CONSUMED\n{'-' * 80}")
            logger.info(f"Total Input Tokens: {self.total_tokens['input']}")
            logger.info(f"Total Output Tokens: {self.total_tokens['output']}")
            logger.info(f"Total Tokens: {self.total_tokens['total']}")
            logger.info(f"{'=' * 80}\n")
            
            # Return successful benchmark result
            return {
                "success": True,
                "output": output,
                "time": total_time,
                "llm_calls": self.llm_calls_list,
                "tokens": self.total_tokens
            }
            
        except Exception as e:
            # Log error details
            logger.error(f"\nError: {str(e)}")
            
            # Calculate total time even on failure
            total_time = time.time() - start_time
            
            # Return failed benchmark result with error details
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "time": total_time,
                "llm_calls": self.llm_calls_list,
                "tokens": self.total_tokens
            }

    def _get_system_prompt(self) -> str:
        """
        Get system prompt for the LangChain agent.
        
        Returns:
            System prompt string with tool usage instructions
        """
        # Return comprehensive system prompt with tool usage guidelines
        return """You are a data analysis assistant with access to filesystem tools.

## AVAILABLE TOOLS

You have three tools available. Choose the appropriate tool based on the file type and task:

1. **list_directory(path: str)**
   - Lists all files and directories in the specified path
   - Use this to discover available files when the exact filename is unknown

2. **inspect_csv(path: str)**
   - BEST CHOICE for CSV file analysis and data processing
   - Returns: Complete CSV file content as a formatted table with ALL rows
   - Use this when you need to analyze, filter, aggregate, or process CSV data
   - Example: Finding top products, calculating totals, filtering by region, etc.

3. **read_file(path: str)**
   - Reads complete file content (returns entire file)
   - Use this ONLY for non-CSV files like .txt, .py, .md, .json, etc.
   - Use when you need the exact full content of text-based files

## HOW TO CHOOSE THE RIGHT TOOL

**For CSV file analysis tasks** (calculations, filtering, aggregations):
→ Use `inspect_csv` - it provides full CSV data with structure information for analysis

**For reading text files** (.txt, .py, .md, .json):
→ Use `read_file` - get the full content

**For exploring directories**:
→ Use `list_directory` - discover available files

## IMPORTANT RULES

- Analyze what information you need before choosing a tool
- For CSV questions, inspect_csv usually provides sufficient information
- Use exact column names from inspection results
- Provide clear, formatted output with your final answer
- If user mentions a specific file name, use it directly - do not explore directories first
"""

