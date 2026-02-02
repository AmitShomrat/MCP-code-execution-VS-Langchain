from fastmcp import FastMCP
from costume_mcp_servers.db_init import get_shared_db
from costume_mcp_servers.threat_demo_server import (LegitimateDBHandler,
                                PhaseI_1DBHandler,
                                PhaseII_1DBHandler,
                                PhaseII_2DBHandler,
                                PhaseIII_1DBHandler,
                                PhaseIII_2DBHandler)


def create_server(server_type: str = "L") -> FastMCP:
    """Create a server with the given handler."""
    conn = get_shared_db()
    
    if server_type == "L":
        handler = LegitimateDBHandler(conn)
        handler.create_server()

    elif server_type == "I_1":
        handler = PhaseI_1DBHandler(conn)
        handler.create_server()

    elif server_type == "II_1":
        handler = PhaseII_1DBHandler(conn)
        handler.create_server()

    elif server_type == "II_2":
        handler = PhaseII_2DBHandler(conn)
        handler.create_server()

    elif server_type == "III_1":
        handler = PhaseIII_1DBHandler(conn)
        handler.create_server()

    elif server_type == "III_2":
        handler = PhaseIII_2DBHandler(conn)
        handler.create_server()

    else:
        raise ValueError(f"Invalid server type: {server_type}")
    
    SERVER_GUIDE = handler.server_guide
    
    return handler.mcp, SERVER_GUIDE

