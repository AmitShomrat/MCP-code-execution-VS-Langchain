"""
Configuration settings for MCP Code Execution
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MCP Configuration
MCP_CONFIG_PATH = os.getenv("MCP_CONFIG_PATH", "mcp_config.json")


# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))

# Code Execution Configuration
CODE_EXECUTION_TIMEOUT = int(os.getenv("CODE_EXECUTION_TIMEOUT", "30"))
DOCKER_IMAGE_NAME = os.getenv("DOCKER_IMAGE_NAME", "code_execution_sandbox:v3")
DOCKER_MCP_GATEWAY = os.getenv("DOCKER_GATEWAY_URL", "http://host.docker.internal:8080")


def server_selection() -> str:
    """Select a server from the list of available MCP threat servers."""
    from costume_mcp_servers.server_factory import enum_servers

    print("\nAvailable MCP servers:")
    for i, server in enumerate(enum_servers):
        print(f"  {i + 1}. {server['name']} - {server['description']}")
    choice = input("Enter the number of the server you want to use: ").strip()

    if not choice.isdigit():
        print("\nInvalid choice. Please enter a valid number.")
        return server_selection()

    idx = int(choice)
    if idx not in range(1, len(enum_servers) + 1):
        print("\nInvalid choice. Please enter a valid number.")
        return server_selection()

    return enum_servers[idx - 1]["value"]

