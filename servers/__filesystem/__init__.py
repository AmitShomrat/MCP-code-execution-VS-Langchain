"""
Filesystem MCP Tool Wrappers

Exports all filesystem tool wrappers for the official MCP filesystem server.

This module provides two versions of each tool:
1. Regular async functions (with _func suffix) - for direct calls in REST APIs, etc.
2. LangChain StructuredTool objects (without suffix) - for use with LangChain agents
"""

# Import regular callable functions
from .read_file import read_file
from .write_file import write_file
from .list_directory import list_directory
from .inspect_csv import inspect_csv

# Import LangChain tool versions
from .read_file import read_file_decorated
from .write_file import write_file_decorated    
from .list_directory import list_directory_decorated
from .inspect_csv import inspect_csv_decorated


__all__ = [
    # Regular functions - for direct calls
    'read_file',
    'write_file', 
    'list_directory',
    'inspect_csv',
    # LangChain tools - for agents
    'read_file_decorated',
    'write_file_decorated',
    'list_directory_decorated',
    'inspect_csv_decorated'
]

