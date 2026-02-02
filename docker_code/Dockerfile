FROM python:3.14.2-slim

# Prevent buffering of stdout and stderr
ENV PYTHONUNBUFFERED=1

# ENV MCP_GATEWAY=http://host.docker.internal:8080 # Environment variable for the mcp client gateway
WORKDIR /workspace

# Passing abstract mcp_client gateway
COPY tools_client tools_client

# Install dependencies
RUN pip install --no-cache-dir -r tools_client/requirements.txt

# make it importable from everywhere
ENV PYTHONPATH=/workspace/tools_client

# Start the container
CMD ["python", "-u", "workspace/main.py"]