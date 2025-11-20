"""
Code Executor for safely running agent-generated Python code in-memory

This module executes code entirely in RAM using exec() - no temp files created or deleted.
Code runs in the same Python process, allowing access to existing MCP client connections.
Fast, clean, and efficient - everything stays in memory and is automatically garbage collected.
"""
import sys
import os
import asyncio
import io
import contextlib
import traceback
from typing import Dict, Any


class CodeExecutor:
    """Executes Python code in-process using exec() for MCP integration"""

    def __init__(self, timeout: int = 30):
        """
        Initialize code executor
        
        Args:
            timeout: Maximum execution time in seconds (currently not enforced for in-process execution)
        """
        self.timeout = timeout

    async def execute_async(self, code: str) -> Dict[str, Any]:
        """
        Execute async Python code in-process (for MCP code)
        This allows code to access existing MCP client connections
        We're running code in memory
        """
        # Capture stdout - Catch all output from the code so we can return it to the user
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            # Add the project root to sys.path so imports work
            project_root = os.path.dirname(os.path.abspath(__file__))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            
            # Create execution namespace with necessary imports
            # Use single namespace for both globals and locals so imports work correctly
            # This dictionary becomes the "environment" where the code runs
            exec_namespace = {
                '__builtins__': __builtins__,  # Built-in functions (print, len, etc.)
                'asyncio': asyncio,    # generated code is async, so we need to import asyncio
            }

            # Redirect stdout and stderr
            # Capture print() output and errors instead of showing in terminal.
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                # Execute the code to define functions and do imports
                # Use same namespace for both globals and locals
                exec(code, exec_namespace, exec_namespace)
                 #   code,   gloabl variable, local variable
                 # everyy improt, variavble, function goes to defined namespace

                # If there's a main() function, await it (we're already in async context)
                # AI generates code with a main() function that needs to be called.
                if 'main' in exec_namespace and asyncio.iscoroutinefunction(exec_namespace['main']):
                    await exec_namespace['main']()

            # Return successful result
            return {
                "success": True,
                "output": stdout_capture.getvalue(),
                "error": None,
                "return_code": 0
            }

        except Exception as e:
            # Get full traceback
            error_traceback = traceback.format_exc()
            
            # Return error result
            return {
                "success": False,
                "output": stdout_capture.getvalue(),
                "error": f"{error_traceback}\n{stderr_capture.getvalue()}",
                "return_code": -1
            }
