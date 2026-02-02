# app/sandbox/docker_executor.py
import asyncio
import os
import tempfile
from typing import Dict, Any

class DockerCodeExecutor:
    def __init__(
        self,
        image: str,
        gateway_url: str,
        timeout_s: int = 30,
    ):
        self.image = image
        self.gateway_url = gateway_url
        self.timeout_s = timeout_s

    async def execute_async(self, code: str) -> Dict[str, Any]:
        # 1) Write code to a temp file in a mounted workspace
        run_dir = tempfile.mkdtemp(prefix="sandbox_run_")
        script_path = os.path.join(run_dir, "main.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        # 2) Build docker command
        cmd = [
            "docker", "run", "--rm",
            "-e", f"MCP_GATEWAY={self.gateway_url}",
            "-v", f"{run_dir}:/workspace",
            self.image,
            "python", "-u", "/workspace/main.py",
        ]

        # 3) Run and capture stdout/stderr
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(), timeout=self.timeout_s)
            stdout = stdout_b.decode("utf-8", errors="replace")
            stderr = stderr_b.decode("utf-8", errors="replace")
            rc = proc.returncode

            return {
                "success": rc == 0,
                "output": stdout,
                "error": stderr if rc != 0 else None,
                "return_code": rc,
            }

        except asyncio.TimeoutError:
            # Kill the container process
            proc.kill()
            try:
                await proc.communicate()
            except Exception:
                pass

            return {
                "success": False,
                "output": "",
                "error": f"Timeout after {self.timeout_s}s",
                "return_code": -1,
            }
