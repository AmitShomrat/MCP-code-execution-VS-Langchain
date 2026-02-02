from fastmcp import FastMCP
from db_init import get_shared_db
from threat_demo_server import (LegitimateDBHandler,
                                PhaseIDBHandler,
                                PhaseIIDBHandler,
                                PhaseIIIDBHandler)


def create_server(server_type: str = "L") -> FastMCP:
    """Create a server with the given handler."""
    conn = get_shared_db()
    
    if server_type == "L":
        handler = LegitimateDBHandler(conn)
        return handler.create_server()

    elif server_type == "I":
        handler = PhaseIDBHandler(conn)
        return handler.create_server()
        
    elif server_type == "II":
        handler = PhaseIIDBHandler(conn)
        return handler.create_server()

    elif server_type == "III":
        handler = PhaseIIIDBHandler(conn)
        return handler.create_server()

    else:
        raise ValueError(f"Invalid server type: {server_type}")