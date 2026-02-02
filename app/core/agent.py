"""
OpenAI Agent for discovering tools from real MCP servers and generating code
Uses official MCP protocol to discover and interact with MCP servers
"""
import json
from typing import List, Dict, Optional

from openai import OpenAI

from app.app_logging.logger import setup_logger
from app.prompts import AGENT_PROMPT
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
