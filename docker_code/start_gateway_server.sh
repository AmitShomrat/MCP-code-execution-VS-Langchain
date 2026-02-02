#!/bin/bash

cd .. 

uvicorn docker_code.mcp_gateway_server:app --host 0.0.0.0 --port 8080 --reload
