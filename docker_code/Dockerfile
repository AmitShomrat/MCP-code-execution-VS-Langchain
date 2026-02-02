FROM python:3.14.2-slim

WORKDIR /app

COPY tools_client tools_client

RUN pip install -r tools_client/requirements.txt
ENV MCP_GATEWAY=http://host.docker.internal:8080
CMD ["python", "-u", "-c", "import sys; code = sys.stdin.read(); exec(code)"]