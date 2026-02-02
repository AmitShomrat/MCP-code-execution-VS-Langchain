from db_init import get_shared_db
from threat_demo_server import LegitimateDBHandler
from fastmcp import FastMCP

def create_server(server_type: str = "legitimate") -> FastMCP:
    """Create a server with the given handler."""
    conn = get_shared_db()
    
    if server_type == "legitimate" or server_type == "L":
        handler = LegitimateDBHandler(conn)
        return handler.create_server()

    elif server_type == "infected" or server_type == "I":
        pass # TODO: Implement infected server
    
    elif server_type == "malicious" or server_type == "M":
        pass # TODO: Implement malicious server

    else:
        raise ValueError(f"Invalid server type: {server_type}")