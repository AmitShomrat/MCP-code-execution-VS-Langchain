"""
Configuration settings for MCP Code Execution
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))

# Code Execution Configuration
CODE_EXECUTION_TIMEOUT = int(os.getenv("CODE_EXECUTION_TIMEOUT", "30"))

# MCP Configuration
MCP_CONFIG_PATH = os.getenv("MCP_CONFIG_PATH", "mcp_config.json")

