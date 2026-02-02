"""
Orchestrator for code execution with MCP.

This module handles the multi-turn conversation flow between the LLM and code executor,
managing the lifecycle of MCP connections and code execution.
"""
import asyncio
from typing import Dict, Any
import time
import json

# Application imports
from app.core import get_mcp_client, OpenAICodeAgent, DockerCodeExecutor, generate_mcp_tool_descriptions_and_catalog
from app.utils import ResultLogger
from app.app_logging.logger import setup_logger
from app.config import (CODE_EXECUTION_TIMEOUT,
                        MCP_CONFIG_PATH,
                        DOCKER_IMAGE_NAME,
                        DOCKER_MCP_GATEWAY)


# Initialize logger for tracking orchestration operations
logger = setup_logger(__name__)
class RealMCPOrchestrator:
    """
    Orchestrates code execution with real MCP servers.
    
    This class manages the entire workflow of:
    1. Initializing MCP connections
    2. Generating code through LLM
    3. Executing code in sandbox environment
    4. Managing multi-turn conversations
    5. Collecting and returning results
    """

    def __init__(self):
        """
        Initialize orchestrator with MCP configuration.
        
        Args:
            mcp_config_path: Path to MCP configuration file. If None, uses default from config.
        """
        
        # Initialize MCP client for connecting to MCP servers
        self.mcp_client = get_mcp_client(MCP_CONFIG_PATH)
        
        # Initialize code executor with timeout configuration
        # self.code_executor = CodeExecutor(timeout=CODE_EXECUTION_TIMEOUT)

        self.docker_executor = DockerCodeExecutor(image=DOCKER_IMAGE_NAME,
                                                  gateway_url=DOCKER_MCP_GATEWAY,
                                                  timeout_s=CODE_EXECUTION_TIMEOUT)
        
        # Initialize OpenAI agent for code generation
        self.agent = OpenAICodeAgent()

    async def initialize_async(self):
        """
        Initialize MCP connections asynchronously.
        
        This method:
        1. Initializes the MCP client
        2. Discovers available servers
        3. Lists available tools from each server
        """
        # Log initialization start banner
        logger.info("\n\n" + "=" * 80)
        logger.info("INITIALIZING MCP CLIENT CONNECTIONS")
        logger.info("=" * 80 + "\n")

        # Initialize MCP client and connect to all configured servers
        await self.mcp_client.initialize()

        # Get list of all connected servers
        servers = self.mcp_client.get_available_servers()
        logger.info(f"Available MCP servers: {servers}\n")

        # Log tool file description generation start banner
        logger.info("\n\n" + "=" * 80)
        logger.info("GENERATING TOOL DESCRIPTIONS FOR MCP CLIENT CONNECTIONS")
        logger.info("=" * 80 + "\n")
        await generate_mcp_tool_descriptions_and_catalog()


        # # Iterate through each server to discover available tools
        # for server_name in servers:
        #     # Check if server is successfully connected
        #     if self.mcp_client.is_server_connected(server_name):
        #         # List all tools available from this server
        #         tools = await self.mcp_client.list_tools(server_name)
        #         logger.info(f"Server '{server_name}' tools:")
                
        #         # Log each tool's name and description
        #         for tool in tools:
        #             logger.info(f"  - {tool.name}: {tool.description}")
                
        #         # Add blank line after each server's tools
        #         logger.info("")

        # Log initialization completion banner
        logger.info("=" * 80)
        logger.info("INITIALIZATION COMPLETE")
        logger.info("=" * 80 + "\n\n")

    async def run_multi_turn_async(self, user_query: str, max_turns: int = 3) -> Dict[str, Any]:
        """
        Run multi-turn conversation with status-based loop.
        
        Implements progressive discovery approach where agent decides
        if it needs exploration or can complete directly.
        
        Args:
            user_query: User's natural language request
            max_turns: Maximum number of turns to prevent infinite loops
            
        Returns:
            Dictionary containing:
                - success: Boolean indicating if execution was successful
                - output: Final output from code execution
                - error: Error message if any
                - time: Total execution time
                - llm_calls: List of LLM call details
                - tokens: Token usage information
        """
        # Start timer for total execution time tracking
        total_start = time.time()
        
        # Log the user query
        logger.info(f"\n\n{'=' * 80}\nUSER QUERY: {user_query}\n{'=' * 80}\n")
        
        # Initialize conversation with user query
        messages = [{"role": "user", "content": user_query}]
        
        # Initialize variables for tracking results and metrics
        final_result = None
        turn_times = []
        token_usage_list = []
        
        # Multi-turn loop: iterate up to max_turns times
        for llm_call_number in range(1, max_turns + 1):
            # Start timer for this turn
            turn_start = time.time()
            
            # Get LLM response with generated code
            response = await self._get_llm_response(llm_call_number, messages)
            
            # Handle case where code generation fails
            if response is None:
                return {"success": False, "output": "", "error": "Code generation failed"}
            
            # Execute the generated code and log results
            execution_result = await self._run_generated_code_and_log(llm_call_number, response)
            
            # Calculate turn execution time
            turn_time = time.time() - turn_start
            turn_times.append(turn_time)
            
            # Store token usage for this turn
            token_usage_list.append(response.get("token_usage", {}))
            
            # Log turn completion
            logger.info(f"\n{'=' * 80}\nLLM CALL {llm_call_number} COMPLETED in {turn_time:.2f}s\n{'=' * 80}")
            
            # Check if task is complete (status="complete" means agent finished)
            if response["status"] == "complete":
                logger.info("\nTask COMPLETE (status=complete)\n")
                final_result = execution_result
                break
            
            # Add results to conversation history for next turn (status="exploring")
            self._update_conversation_with_results(llm_call_number, response, execution_result, messages)
            
            # Log warning if execution failed but continue to next turn
            if not execution_result['success']:
                logger.warning(f"Execution failed in LLM call {llm_call_number}, but continuing...\n")
        
        # Handle case where max turns reached without completion
        if final_result is None:
            logger.warning(f"\nMax turns ({max_turns}) reached")
            final_result = execution_result
        
        # Calculate total execution time
        total_time = time.time() - total_start
        
        # Display final results summary
        ResultLogger.display_final_results(final_result, turn_times, total_time, token_usage_list)
        
        # Return formatted result dictionary
        return {
            "success": final_result.get("success", False),
            "output": final_result.get("output", ""),
            "error": final_result.get("error"),
            "time": total_time,
            "llm_calls": self._format_llm_calls(turn_times, token_usage_list),
            "tokens": self._calculate_total_tokens(token_usage_list)
        }
    
    async def _get_llm_response(self, llm_call_number: int, messages: list) -> Dict[str, str]:
        """
        Get code generation response from LLM with conversation history.
        
        Args:
            llm_call_number: Current LLM call number for logging
            messages: Conversation history messages
            
        Returns:
            Dictionary containing status, code, reasoning, and token usage
        """
        # Log LLM call start with conversation size
        logger.info(f"\n\n{'=' * 80}\nLLM CALL {llm_call_number}\n{'=' * 80}\n\nSending {len(messages)} messages to LLM...\n")
        
        # Call LLM agent to generate code based on conversation history
        try:
            response = await self.agent.generate_code_with_history(messages)
        except Exception as e:
            # Log error and return None if code generation fails
            logger.error(f"Error generating code: {e}")
            return None
        
        # Log LLM response details including token usage
        ResultLogger.log_llm_response_with_tokens(llm_call_number, response)
        
        # Return LLM response containing status, code, reasoning, and tokens
        return response
    
    async def _run_generated_code_and_log(self, llm_call_number: int, response: Dict) -> Dict:
        """
        Execute generated code in sandbox and log results.
        
        Args:
            llm_call_number: Current LLM call number for logging
            response: LLM response containing generated code
            
        Returns:
            Dictionary containing execution results (success, output, error)
        """
        # Log code execution start
        logger.info(f"\n{'=' * 80}\nEXECUTING CODE (Call {llm_call_number})\n{'=' * 80}")
        
        # Execute the generated code in sandbox environment
        # execution_result = await self.code_executor.execute_async(response["code"])
        execution_result = await self.docker_executor.execute_async(response["code"])
        
        # Log the execution output
        logger.info(f"\nExecution Result:\n{'-' * 80}\n{execution_result['output']}\n{'-' * 80}")
        
        # Log any errors that occurred during execution
        if execution_result['error']:
            logger.error(f"\nError: {execution_result['error']}")
        
        # Return execution result dictionary
        logger.info(f"Execution result: {execution_result}")
        return execution_result
    
    def _update_conversation_with_results(self, llm_call_number: int, response: Dict, 
                                           execution_result: Dict, messages: list):
        """
        Append assistant response and execution results to conversation history.
        
        Args:
            llm_call_number: Current LLM call number for logging
            response: LLM response containing status, code, and reasoning
            execution_result: Results from code execution
            messages: Conversation history to update
        """
        # Log continuation to next turn
        logger.info("\nContinuing to next LLM call (status=exploring)...")
        
        # Create JSON string of assistant's response for conversation history
        assistant_message_json = json.dumps({
            "status": response["status"],
            "code": response["code"],
            "reasoning": response.get("reasoning", "")
        })
        
        # Append assistant message to conversation history
        messages.append({
            "role": "assistant",
            "content": assistant_message_json
        })
        
        # Append execution result as user message to conversation history
        messages.append({
            "role": "user",
            "content": f"Execution result:\n{execution_result['output']}"
        })
        
        # Log what was added to conversation history
        logger.info(f"\n{'=' * 80}\nADDED TO CONVERSATION HISTORY (Call {llm_call_number})\n{'=' * 80}\n\nAssistant Message (JSON added to history):\n{assistant_message_json}\n\nUser Message: Execution result ({len(execution_result['output'])} chars)\nTotal history size: {len(messages)} messages\n")

    def _format_llm_calls(self, turn_times: list, token_usage_list: list) -> list:
        """
        Format LLM call details for result output.
        
        Args:
            turn_times: List of execution times for each turn
            token_usage_list: List of token usage for each turn
            
        Returns:
            List of formatted LLM call details
        """
        # Initialize empty list for formatted LLM call data
        llm_calls = []
        
        # Iterate through each turn and combine time + token data
        for i, (time_taken, tokens) in enumerate(zip(turn_times, token_usage_list), 1):
            # Append formatted call details to list
            llm_calls.append({
                "call_number": i,
                "latency": round(time_taken, 2),
                "tokens": tokens
            })
        
        # Return list of all LLM call details
        return llm_calls

    def _calculate_total_tokens(self, token_usage_list: list) -> Dict[str, int]:
        """
        Calculate total token usage across all LLM calls.
        
        Args:
            token_usage_list: List of token usage dictionaries
            
        Returns:
            Dictionary with total prompt_tokens, completion_tokens, and total_tokens
        """
        # Initialize total token counters
        total_tokens = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
        
        # Sum up tokens from all LLM calls
        for tokens in token_usage_list:
            total_tokens["prompt_tokens"] += tokens.get("prompt_tokens", 0)
            total_tokens["completion_tokens"] += tokens.get("completion_tokens", 0)
            total_tokens["total_tokens"] += tokens.get("total_tokens", 0)
        
        # Return aggregated token usage
        return total_tokens

    async def cleanup_async(self):
        """
        Cleanup MCP connections and resources.
        """
        # Close all MCP client connections
        await self.mcp_client.close()


   