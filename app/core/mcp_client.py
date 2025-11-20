"""
Real MCP Client implementation using official MCP SDK
"""
import asyncio
import json
import os
from typing import Any, Dict, List
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from app.app_logging.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)


class MCPClient:
    """Client for interacting with real MCP servers using official protocol"""

    def __init__(self, config_path: str = "mcp_config.json"):
        # Load MCP server configurations from file
        self.config_path = config_path
        self.server_configs = self._load_config()
        
        # Store active sessions
        self.sessions = {}
        #  Create stack to hold all async resources - Add MCP server process to stack, Add JSON-RPC session to stack 
        self.exit_stack = AsyncExitStack()
        
        # Track if client is initialized
        self.initialized = False

    def _load_config(self) -> Dict[str, Any]:
        """Load MCP server configurations from JSON file"""
        if not os.path.exists(self.config_path):
            return {}
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        return config.get("mcpServers", {})

    async def initialize(self):
        """Initialize connections to all configured MCP servers"""
        if self.initialized:
            return
        
        # Connect to each configured server and creates communication channels
        for server_name, config in self.server_configs.items():
            await self._connect_server(server_name, config)
        
        self.initialized = True

    async def _connect_server(self, server_name: str, config: Dict[str, Any]):
        """Connect to a single MCP server"""
        try:
            # Extract server parameters
            command = config.get("command")
            args = config.get("args", [])
            
            # Step 1: Create server parameters
            # Packages the server launch configuration into an MCP SDK object.
            #Launch the MCP server by running this command
            server_params = StdioServerParameters(
                command=command,
                args=args,
            )
            
            # Step 2: Launch the MCP server process
            # Create stdio client and session
            stdio = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            
            # read: to read response from MCP server & write: write commands to MCP Server
            read, write = stdio   # Get input/output pipes
            
            # Step 3: Create JSON-RPC session for communication
            # Creates a session object that manages the JSON-RPC protocol communication with the server.
            # This session obj can send tool call request,receive tool response
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            
            # Initialize the session
            await session.initialize()
            
            # Store session
            self.sessions[server_name] = session
            
            logger.info(f"Connected to MCP server: {server_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to {server_name}: {str(e)}")

    async def list_tools(self, server_name: str) -> List[Dict[str, Any]]:
        """List all tools available on a specific MCP server"""
        if server_name not in self.sessions:
            raise ValueError(f"Server '{server_name}' is not connected")
        
        #store sessions
        session = self.sessions[server_name]
        
        # Call list_tools on the MCP server
        tools_result = await session.list_tools()
        
        return tools_result.tools

    async def call_tool(
        self, 
        server_name: str, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Any:
        """Call a tool on a connected MCP server using real protocol"""
        if server_name not in self.sessions:
            raise ValueError(f"Server '{server_name}' is not connected")
        
        session = self.sessions[server_name]
        
        logger.info(f"Calling {server_name}.{tool_name} with arguments: {arguments}")
        
        # Call the tool using MCP protocol
        result = await session.call_tool(tool_name, arguments)
        
        return result
        

    async def close(self):
        """Close all MCP server connections"""
        await self.exit_stack.aclose()
        self.sessions.clear()
        self.initialized = False
        logger.info("All MCP connections closed")

    def get_available_servers(self) -> List[str]:
        """Get list of all configured server names"""
        return list(self.server_configs.keys())

    def is_server_connected(self, server_name: str) -> bool:
        """Check if a server is connected"""
        return server_name in self.sessions


# Global MCP client instance
_mcp_client_instance = None


def get_mcp_client(config_path: str = "mcp_config.json") -> MCPClient:
    """Get or create the global MCP client instance"""
    global _mcp_client_instance
    
    if _mcp_client_instance is None:
        _mcp_client_instance = MCPClient(config_path)
    
    return _mcp_client_instance
