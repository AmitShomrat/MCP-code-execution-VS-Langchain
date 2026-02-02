# Unified MCP Benchmark Dashboard

## Overview

The system has been refactored into a **single unified FastAPI application** that replaces the previous dual-UI approach (Streamlit + FastAPI). This eliminates the multiprocessing complexity and MCP client singleton duplication issues.

## Key Features

### ✅ Single Application
- One FastAPI app serving both dashboard and gateway
- Shared MCP client singleton across all operations
- No duplicate connections to MCP servers
- Simplified deployment

### ✅ Two Modes in One UI

#### **Single Task Mode** 🎯
- Run individual queries
- Compare Traditional MCP vs Code Execution MCP in real-time
- View detailed metrics and outputs
- Export results

#### **Multiple Tasks Mode** 📋
- Add multiple benchmark tasks dynamically
- Run batch comparisons
- View aggregate statistics
- Interactive charts for time and token comparisons
- Detailed results for each task

## Architecture

```
┌─────────────────────────────────────────────┐
│         MCP Benchmark Dashboard             │
│         (FastAPI + JavaScript UI)           │
├──────────────────┬──────────────────────────┤
│  Single Task     │   Multiple Tasks         │
│  - Run one query │   - Batch benchmarks     │
│  - Quick compare │   - Analytics            │
└──────────────────┴──────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │   Shared MCP Client   │
        │     (Singleton)       │
        └───────────┬───────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌───▼────┐    ┌────▼────┐    ┌────▼────┐
│FS MCP  │    │Sequential│   │Code Exec│
│Server  │    │Thinking  │   │  MCP    │
└────────┘    └─────────┘    └─────────┘
```

## What Changed

### 1. **Removed Streamlit**
- No more separate Streamlit app
- All functionality moved to FastAPI + JavaScript

### 2. **New API Endpoints**
Added to `/app/api/routes.py`:
- `POST /api/benchmarks/run-multiple` - Run multiple benchmark tasks
- Returns aggregate statistics and per-task results

### 3. **New Models**
Added to `/app/api/models.py`:
- `TaskDefinition` - Define a benchmark task
- `MultiTaskRequest` - Request for multiple tasks
- `MultiTaskResponse` - Results with summary statistics
- `TaskResult` - Individual task result with comparison

### 4. **Enhanced UI**
Updated `/static/index.html`:
- Mode toggle buttons (Single/Multiple)
- Multi-task section with dynamic task management
- Summary cards showing aggregate metrics
- Interactive charts for batch results
- Detailed results view

### 5. **New JavaScript Features**
Added to `/static/js/app.js`:
- `initializeMultiTaskMode()` - Set up multi-task functionality
- `addTaskItem()` - Dynamically add tasks
- `runAllTasks()` - Execute batch benchmarks
- `displayMultiTaskResults()` - Show results with charts
- Chart.js integration for visual comparisons

### 6. **Simplified Launcher**
Updated `/launcher.py`:
- Single menu option to start dashboard
- Uses `main.py` which already shares MCP client correctly
- No more multiprocessing/threading complexity

## How to Use

### Starting the Dashboard

```bash
python launcher.py
```

Choose option 1 to start the dashboard.

The dashboard will be available at:
- **Main UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Gateway**: http://localhost:8080
- **Gateway Docs**: http://localhost:8080/docs

### Single Task Mode

1. Enter your query in the text area
2. Click "Traditional MCP" or "Code Execution MCP"
3. View real-time results and comparisons
4. Export results if needed

### Multiple Tasks Mode

1. Click the "Multiple Tasks" toggle button
2. Click "+ Add Task" to add tasks
3. Fill in:
   - Task ID (e.g., task_1)
   - Query (e.g., "Calculate total revenue in Sales_Records.csv")
4. Set max LLM turns (default: 3)
5. Click "Run All Tasks"
6. View:
   - Summary statistics
   - Time comparison chart
   - Token usage chart
   - Detailed results for each task

## Benefits

### ✅ **No Singleton Issues**
- Single process, single MCP client
- No duplicate connections
- Reduced resource usage

### ✅ **Better Performance**
- Less overhead from multiprocessing
- Shared resources
- Faster startup

### ✅ **Simpler Deployment**
- One application to deploy
- Fewer moving parts
- Easier to maintain

### ✅ **Consistent UX**
- Same look and feel across modes
- Smooth transitions
- Unified navigation

### ✅ **Enhanced Features**
- Batch benchmark execution
- Aggregate analytics
- Interactive visualizations
- Export capabilities

## API Examples

### Run Multiple Tasks

```bash
curl -X POST "http://localhost:8000/api/benchmarks/run-multiple" \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      {
        "task_id": "task_1",
        "user_query": "Calculate total revenue in Sales_Records.csv"
      },
      {
        "task_id": "task_2",
        "user_query": "Find the top 5 customers by total purchases"
      }
    ],
    "max_turns": 3
  }'
```

### Response

```json
{
  "success": true,
  "results": [
    {
      "task_id": "task_1",
      "user_query": "Calculate total revenue...",
      "timestamp": "2026-01-05T12:00:00",
      "code_execution_mcp": { "success": true, "time": 5.2, ... },
      "traditional_mcp": { "success": true, "time": 8.1, ... },
      "comparison": { "time_diff": -2.9, ... }
    }
  ],
  "summary": {
    "total_tasks": 2,
    "code_exec_successes": 2,
    "traditional_successes": 2,
    "avg_code_exec_time": 5.2,
    "avg_traditional_time": 8.1,
    "time_improvement": 35.8,
    "token_reduction": 42.3
  }
}
```

## Technical Details

### Shared MCP Client

The `main.py` implementation uses `asyncio.gather()` to run both servers:

```python
async def main():
    global _mcp_client
    _mcp_client = await get_mcp_client()  # Initialize once
    await asyncio.gather(
        serve("app.api.routes:app", "0.0.0.0", 8000),
        serve("docker_code.mcp_gateway_server:app", "localhost", 8080)
    )
```

Both servers share the same MCP client singleton, eliminating duplicate connections.

### Frontend Architecture

- **Pure JavaScript** (no frameworks) for fast performance
- **Chart.js** for interactive visualizations
- **CSS Grid/Flexbox** for responsive layouts
- **Fetch API** for async backend communication

## Migration from Streamlit

If you were using the Streamlit UI:

**Before:**
```bash
python launcher.py  # Choose option 1 for Streamlit
# Streamlit at :8501, Gateway at :8080
```

**Now:**
```bash
python launcher.py  # Choose option 1 for Dashboard
# Everything at :8000, Gateway at :8080
```

All Streamlit functionality is now in the "Multiple Tasks" mode of the unified dashboard.

## Future Enhancements

Potential additions:
- Save/load task templates
- Task scheduling
- Historical trend analysis
- Custom metric thresholds
- Team collaboration features
- Report generation

## Troubleshooting

### Port Already in Use

```bash
# Kill existing processes
lsof -ti:8000 | xargs kill -9
lsof -ti:8080 | xargs kill -9
```

### MCP Client Not Initializing

Check that MCP servers are configured in `mcp_config.json`.

### Charts Not Displaying

Ensure Chart.js is loading correctly. Check browser console for errors.

## Support

For issues or questions, check:
1. Browser console for JavaScript errors
2. Terminal output for backend errors
3. API docs at http://localhost:8000/docs

