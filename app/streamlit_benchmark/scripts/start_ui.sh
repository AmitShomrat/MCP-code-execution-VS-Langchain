#!/bin/bash
# Start Streamlit Benchmark UI

# Get the script's directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../../.." && pwd )"

echo "=================================================="
echo "Starting MCP Benchmark UI"
echo "=================================================="
echo ""
echo "Access the UI at: http://localhost:8501"
echo "Press Ctrl+C to stop"
echo ""

cd "$PROJECT_ROOT"

streamlit run app/streamlit_benchmark/ui.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --browser.gatherUsageStats=false

