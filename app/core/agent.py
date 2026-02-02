"""
OpenAI Agent for discovering tools from real MCP servers and generating code
Uses official MCP protocol to discover and interact with MCP servers
"""
import json
from typing import List, Dict, Optional, Any

from openai import OpenAI

from app.app_logging.logger import setup_logger
from app.prompts import AGENT_PROMPT, SUMMARIZATION_PROMPT
from app.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_MAX_TOKENS,
    OPENAI_TEMPERATURE
)


# Setup logger
logger = setup_logger(__name__)


class OpenAICodeAgent:
    """Agent that discovers MCP tools from real MCP servers and generates Python code using OpenAI"""

    def __init__(self, api_key: Optional[str] = None):
        # Initialize OpenAI client for code generation
        self.client = OpenAI(api_key=api_key or OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.max_tokens = OPENAI_MAX_TOKENS

    async def generate_code_with_history(
        self, 
        messages: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Generate code with conversation history and status indicator.
        
        Uses progressive discovery approach where agent explores tools
        and data structures across multiple turns. Returns structured
        JSON response with status to determine if more turns are needed.
        
        Args:
            messages: Conversation history with role and content
                Example: [
                    {"role": "user", "content": "query"},
                    {"role": "assistant", "content": "code1"},
                    {"role": "user", "content": "result1"},
                    ...
                ]
        
        Returns:
            Dictionary with:
                - status: "exploring" or "complete"
                - code: Generated Python code
                - reasoning: Explanation of status choice
        
        Raises:
            ValueError: If LLM response is invalid JSON or missing fields
        """
        # Build messages array with system prompt and conversation history
        openai_messages = [{"role": "system", "content": AGENT_PROMPT}] # The AGENT_PROMPT used while Maintenance a messeges list
        openai_messages.extend(messages)
        logger.info(f"\n\nOpenAI Messages:\n\n{json.dumps(openai_messages, indent=2)}\n")
        
        # Call OpenAI API with JSON mode to ensure structured response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            response_format={"type": "json_object"},
            max_tokens=self.max_tokens,
            temperature=OPENAI_TEMPERATURE
        )
        
        # Parse JSON response from LLM
        raw_response = response.choices[0].message.content
        result = json.loads(raw_response)
        
        # Validate required fields are present
        if "status" not in result or "code" not in result:
            raise ValueError(f"Invalid LLM response format: {result}")
        
        # Validate status value
        if result["status"] not in ["exploring", "complete"]:
            raise ValueError(f"Invalid status value: {result['status']}")
        
        # Add token usage information
        result["token_usage"] = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        
        return result

    async def generate_final_answer(
        self,
        user_query: str,
        execution_results: List[str],
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Generate a clean, well-formatted final answer from code execution results.
        
        This method analyzes all execution results and provides a final answer
        that is clean, well-formatted, and directly addresses the user's query.
        
        Args:
            user_query: The original user query
            execution_results: List of execution output strings from all turns
            conversation_history: Full conversation history for context
            
        Returns:
            Dictionary with:
                - answer: Clean, formatted final answer
                - token_usage: Token usage information
        """
        # Compile all execution results into a single context
        results_text = "\n\n---\n\n".join([
            f"Execution Result {i+1}:\n{result}" 
            for i, result in enumerate(execution_results)
        ])
        
        # Create messages for summarization
        messages = [
            {
                "role": "system",
                "content": SUMMARIZATION_PROMPT
            },
            {
                "role": "user",
                "content": f"""Original User Query:
{user_query}

Code Execution Results:
{results_text}

Please provide a clean, well-formatted final answer to the user's query based on the execution results above."""
            }
        ]
        
        logger.info(f"\n\n{'=' * 80}\nFINAL ANSWER GENERATION\n{'=' * 80}\n")
        logger.info(f"Generating final answer for query: {user_query}")
        logger.info(f"Analyzing {len(execution_results)} execution results\n")
        
        # Call OpenAI API (no JSON mode - we want natural text)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=OPENAI_TEMPERATURE
        )
        
        # Get the final answer
        final_answer = response.choices[0].message.content
        
        # Extract token usage
        token_usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        
        logger.info(f"\n{'=' * 80}\nFINAL ANSWER GENERATED\n{'=' * 80}\n")
        logger.info(f"Answer length: {len(final_answer)} characters\n")
        logger.info(f"Token usage: {token_usage['total_tokens']} tokens\n")
        
        return {
            "answer": final_answer,
            "token_usage": token_usage
        }
