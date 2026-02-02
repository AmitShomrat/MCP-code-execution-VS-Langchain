# threat_demo_server.py - Main entry point
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from db_init import get_shared_db
from server_factory import create_server

mcp = create_server("L")

# mcp = create_server("I")

# mcp = create_server("II")

if __name__ == "__main__":
    mcp.run()