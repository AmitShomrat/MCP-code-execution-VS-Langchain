# threat_demo_server.py - Main entry point
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from costume_mcp_servers.db_init import get_shared_db
from costume_mcp_servers.server_factory import create_server

# mcp, SERVER_GUIDE = create_server("L")

# mcp, SERVER_GUIDE = create_server("I_1")

# mcp, SERVER_GUIDE = create_server("II_1")

# mcp, SERVER_GUIDE = create_server("II_2")

# mcp, SERVER_GUIDE = create_server("III_1")

# mcp, SERVER_GUIDE = create_server("III_2")

mcp, SERVER_GUIDE = create_server("IV_1")

if __name__ == "__main__":
    mcp.run()