# threat_demo_server.py - Main entry point
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from costume_mcp_servers.db_init import get_shared_db
from costume_mcp_servers.server_factory import create_server


server_choice = os.getenv('SERVER_CHOICE', 'I_1')
mcp, SERVER_GUIDE = create_server(server_choice)


if __name__ == "__main__":
    mcp.run()