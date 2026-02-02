# FROM python:3.14.2-slim

# # Prevent buffering of stdout and stderr
# ENV PYTHONUNBUFFERED=1

# # Passing abstract mcp_client gateway
# COPY tools_client /opt/tools_client

# # Install dependencies
# RUN pip install --no-cache-dir -r /opt/tools_client/requirements.txt

# # make it importable from everywhere
# ENV PYTHONPATH=/opt/tools_client

# WORKDIR /workspace

# # Start the container
# CMD ["python", "-u", "workspace/main.py"]


FROM python:3.14.2-slim

ENV PYTHONUNBUFFERED=1

# Copy tools and execution server
COPY tools_client /opt/tools_client
COPY execution_server.py /opt/execution_server.py

# Install dependencies
RUN pip install --no-cache-dir -r /opt/tools_client/requirements.txt

ENV PYTHONPATH=/opt/tools_client

WORKDIR /workspace

COPY test.py /workspace/test.py

# Start execution server (not main.py anymore)
CMD ["python", "-u", "/opt/execution_server.py"]