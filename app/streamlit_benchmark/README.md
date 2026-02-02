# MCP Benchmark Streamlit UI

A clean, intuitive Streamlit-based UI for running and visualizing benchmark comparisons between **Code Execution MCP** and **Traditional MCP** approaches.

## 🚀 Quick Start

### Launch the UI

From the project root:

```bash
# Option 1: Use the launcher
python launcher.py
# Choose option 1

# Option 2: Direct launch
streamlit run app/streamlit_benchmark/ui.py --server.port=8501

# Option 3: Use shell script
./app/streamlit_benchmark/scripts/start_ui.sh
```

Access at: **http://localhost:8501**

### First Run (3 Steps)

1. Click **"📋 Load Default Tasks"** in the sidebar
2. Click **"🚀 Run Benchmarks"**
3. Explore results with interactive visualizations!

## 📋 Features

### Core Functionality
- **One-Click Default Tasks**: Pre-configured 10 example tasks ready to run
- **Custom Task Upload**: Drag & drop your own task JSON files
- **Automated Benchmarking**: Run both approaches on all tasks automatically
- **Results Management**: Save/load benchmark results with timestamps

### Interactive Visualizations
- **Time Comparison**: Execution time per task (bar charts)
- **LLM Calls**: Number of LLM invocations per task
- **Token Usage**: Total tokens consumed per task
- **Aggregate Metrics**: Overall totals across all tasks

### Enhanced UI
- **Glowing Difference Metrics**: Color-coded gradient boxes with text glow
  - Pink: Code Execution is faster/better (negative diff)
  - Purple: Traditional is faster/better (positive diff)
  - Blue: Tie (zero diff)
- **Collapsible Task Details**: Side-by-side comparison for each task
- **Data Export**: View results as interactive tables

## 📁 File Structure

```
app/streamlit_benchmark/
├── __init__.py              # Package initialization
├── ui.py                    # Main Streamlit application
├── benchmark_tasks.json     # Default example tasks (10 tasks)
├── README.md                # This file
├── benchmark_results/       # Saved benchmark results (auto-created)
│   └── .gitignore          # Ignore result files in git
└── scripts/
    ├── start_ui.sh          # Launch script
    └── test_integration.py  # Integration tests
```

## 📊 How to Use

### Configuration

**Max LLM Turns**: Set the maximum number of LLM turns (1-10, default: 3)

### Loading Tasks

**Option 1 - Default Tasks** (recommended for first-time users):
```
Click "📋 Load Default Tasks" button
→ Loads app/streamlit_benchmark/benchmark_tasks.json
→ 10 pre-configured filesystem tasks ready to run
```

**Option 2 - Upload Custom Tasks**:
```
Use the file uploader widget
→ Browse to your JSON file or drag & drop
→ Only .json files accepted
```

### Running Benchmarks

1. Ensure tasks are loaded (you'll see "📋 Loaded Tasks (N)")
2. Click **"🚀 Run Benchmarks"**
3. Wait for completion (5-30 seconds per task)
4. Results auto-save to `app/streamlit_benchmark/benchmark_results/results_YYYYMMDD_HHMMSS.json`

### Viewing Results

Results are organized in sections:

1. **Summary Metrics**
   - Success rates for both approaches
   - Average time/LLM calls/token differences

2. **Visualizations** (4 tabs)
   - Time comparison bar chart
   - LLM calls comparison bar chart
   - Token usage comparison bar chart
   - Aggregate metrics

3. **Results Table**
   - Sortable dataframe with all metrics

4. **Detailed Task Results**
   - Expandable sections per task
   - Glowing difference metrics (time, calls, tokens)
   - Side-by-side comparison of both approaches
   - Full output and error messages

### Loading Previous Results

Use the **"📥 Load Previous Results"** file uploader:
- Browse to `app/streamlit_benchmark/benchmark_results/` folder
- Select any previous results JSON file
- View historical comparisons

## 📝 Task JSON Format

Create custom tasks with this structure:

```json
[
  {
    "task_id": 1,
    "user_query": "List all files in the current directory",
    "expected_behaviour": "Agent calls filesystem.list_directory with path='.'",
    "expected_output": "List of files and directories"
  },
  {
    "task_id": 2,
    "user_query": "What is the size of main.py?",
    "expected_behaviour": "Agent calls filesystem.get_file_info",
    "expected_output": "File size and metadata"
  }
]
```

### Required Fields
- `task_id` (int): Unique identifier
- `user_query` (str): Query to send to both benchmarks
- `expected_behaviour` (str): Description of expected agent behavior
- `expected_output` (str): Description of expected output

## 🎨 Visual Features

### Difference Metrics (Glowing Design)

Each task detail shows three prominent gradient boxes:

**Time Difference**
```
┌─────────────────────┐
│  TIME DIFFERENCE    │  ← White uppercase label
│     -2.35s         │  ← Large glowing white number
└─────────────────────┘
   Pink gradient = Code Execution faster
```

**Color Meanings**:
- **Pink gradient** (#f093fb → #f5576c): Negative diff = Code Execution wins
- **Purple gradient** (#667eea → #764ba2): Positive diff = Traditional wins  
- **Blue gradient** (#4facfe → #00f2fe): Zero diff = Tie

### Text Effects
- Font size: 32px
- Font weight: 800
- Double glow: Inner (20px) + Outer (40px)
- High contrast white on vibrant backgrounds

## 🔧 Configuration & Tips

### Environment Setup

Required:
```bash
export OPENAI_API_KEY="your-key-here"
```

Recommended dependencies:
```bash
pip install streamlit plotly pandas
```

### Performance Tips

1. **Start Small**: Test with 2-3 tasks first
2. **Use Lower Max Turns**: Set to 2 for faster results
3. **Docker Ready**: Ensure Docker is running before benchmarks
4. **MCP Config**: Verify `mcp_config.json` in project root

### Task Design Best Practices

1. **Clear queries**: Be specific about what you want
2. **Achievable scope**: Keep tasks simple and focused
3. **Realistic expectations**: Align with MCP tool capabilities
4. **Test incrementally**: Add tasks one by one

## 🐛 Troubleshooting

### UI Won't Start
```bash
pip install streamlit plotly pandas
```

### MCP Servers Not Connecting
- Check `mcp_config.json` in project root
- Verify OpenAI API key is set
- Check logs in `logs/app.log`

### Docker Issues
```bash
docker ps                    # Check if Docker is running
docker logs <container_id>   # View container logs
```

### Benchmarks Running Slowly
This is **normal**! Each task involves:
- MCP server connections
- Multiple LLM calls (typically 2-8 per task)
- Docker code execution
- Network latency

**Expected**: 5-30 seconds per task

### File Upload Issues
- Ensure file is valid JSON
- Check file has `.json` extension
- Verify task structure matches format above

## 📚 Integration

This UI integrates with:
- `app/benchmarks/benchmark_runner.py` - Core benchmark execution
- `app/benchmarks/code_execution_mcp.py` - Code execution approach
- `app/benchmarks/traditional_mcp.py` - Traditional approach
- `app/core/mcp_client.py` - MCP server connections
- `app/core/orchestrator.py` - Multi-turn orchestration

## 🧪 Testing

Run integration tests:
```bash
python app/streamlit_benchmark/scripts/test_integration.py
```

Expected output:
- ✅ File Structure
- ✅ Task Loading
- ✅ Task File Structure

## 📊 Example Results

After running the default 10 tasks, expect to see:

**Summary Metrics**:
- Success rates: ~90% for both approaches
- Avg time diff: Code Execution typically 2-5s faster
- Avg LLM calls diff: Code Execution uses 3-6 fewer calls
- Avg token diff: Code Execution uses 1000-2000 fewer tokens

**Performance Characteristics**:
- **Code Execution MCP**: Faster, fewer LLM calls, more efficient
- **Traditional MCP**: More LLM calls, higher latency, higher token usage

## 🎯 Use Cases

1. **Feature Development**: Test how code changes affect performance
2. **Approach Comparison**: Validate which approach works better for your use case
3. **Regression Testing**: Ensure performance doesn't degrade over time
4. **Documentation**: Generate visual reports for stakeholders
5. **Optimization**: Identify bottlenecks and optimization opportunities

## 🔐 Security

- Never commit API keys to version control
- Use environment variables for sensitive data
- Keep benchmark results in secure location
- Review generated code before production use

## 💡 Pro Tips

1. **Save Results**: Always save results for historical comparison
2. **Name Tasks Well**: Use descriptive task_ids and queries
3. **Iterate**: Start with simple tasks, add complexity gradually
4. **Document Expectations**: Clear expected_behaviour helps debugging
5. **Compare Across Runs**: Load multiple result files to see trends

## 📖 Additional Resources

- **Project README**: See root `README.md` for overall system documentation
- **API Documentation**: http://localhost:8000/docs (when API servers running)
- **Test Cases**: See `test_case.txt` in project root
- **Integration Tests**: Run `python app/streamlit_benchmark/scripts/test_integration.py`

## 🤝 Contributing

When adding new features:
1. Keep the UI simple and intuitive
2. Use file uploaders instead of text inputs
3. Provide clear error messages
4. Add loading spinners for long operations
5. Test with both default and custom tasks

---

**Ready to benchmark!** Click "Load Default Tasks" and get started in seconds! 🚀
