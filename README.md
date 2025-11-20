# MCP Benchmark Comparison Dashboard

Python implementation of Code Execution with Model Context Protocol (MCP) using OpenAI and real MCP servers, featuring a web-based benchmark comparison dashboard.

Based on [Anthropic's blog post](https://www.anthropic.com/engineering/code-execution-with-mcp) about building more efficient agents.

## 🎯 Overview

This project provides an interactive web dashboard to compare two approaches for MCP-based agents:

1. **Traditional MCP** - Direct tool calls through LangChain agents
2. **Code Execution MCP** - Generate and execute code using MCP tools

The dashboard allows you to run queries against both approaches and compare performance metrics including execution time, token usage, and LLM call efficiency.

## ✨ Features

- 🎨 **Modern Web Dashboard** - Interactive UI with real-time benchmark results
- 📊 **Performance Comparison** - Compare execution time, token usage, and LLM calls
- 📈 **Visual Analytics** - Chart.js visualizations for metric comparison
- 🚀 **FastAPI Backend** - RESTful API for benchmark execution
- 🐳 **Docker Support** - Containerized deployment for GCP
- 💾 **Result Storage** - JSON-based storage for benchmark history
- 🎯 **Winner Detection** - Automatic performance winner calculation

## 🏗️ Architecture

```
User Query (Web UI)
    |
    ├─── Traditional MCP Path
    |    └── LangChain Agent → Direct Tool Calls → LLM Invocation per Tool
    |
    └─── Code Execution Path
         └── OpenAI Agent → Code Generation → MCP Tool Execution → Final Result
```

## 📁 Project Structure

```
Code_Execution_MCP_17_Nov/
├── main.py                      # FastAPI application runner
├── mcp_config.json              # MCP server configurations
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Project metadata
├── .env.example                 # Environment variables template
├── .dockerignore                # Docker build exclusions
│
├── app/                         # Main application package
│   ├── api/                     # FastAPI routes and models
│   │   ├── routes.py           # API endpoints
│   │   └── models.py           # Pydantic request/response models
│   │
│   ├── benchmarks/              # Benchmark implementations
│   │   ├── traditional_mcp.py  # LangChain-based benchmark
│   │   └── code_execution_mcp.py # Code execution benchmark
│   │
│   ├── core/                    # Core functionality
│   │   ├── mcp_client.py       # MCP client using official SDK
│   │   ├── agent.py            # OpenAI agent for code generation
│   │   ├── orchestrator.py     # Multi-turn conversation orchestrator
│   │   └── code_executor.py    # Secure code execution engine
│   │
│   ├── config/                  # Configuration management
│   │   ├── settings.py         # Application settings
│   │   └── __init__.py
│   │
│   ├── app_logging/             # Logging utilities
│   │   ├── logger.py           # Logger setup
│   │   └── __init__.py
│   │
│   ├── utils/                   # Utility functions
│   │   ├── result_logger.py    # Result formatting and display
│   │   ├── benchmark_storage.py # Benchmark result storage
│   │   └── __init__.py
│   │
│   └── prompts/                 # LLM prompts
│       └── agent_prompt.py     # Code generation prompts
│
├── static/                      # Web dashboard assets
│   ├── index.html              # Main dashboard page
│   ├── css/
│   │   └── style.css          # Dashboard styles
│   └── js/
│       ├── app.js             # Main application logic
│       └── charts.js          # Chart.js visualizations
│
├── servers/                     # MCP tool wrappers
│   └── filesystem/             # Filesystem operations
│       ├── read_file.py
│       ├── write_file.py
│       ├── list_directory.py
│       └── inspect_csv.py
│
├── docker/                      # Docker deployment files
│   ├── dockerfile              # Container definition
│   └── docker-compose.yml      # Service orchestration
│
├── data/                        # Benchmark results storage
│   ├── traditional_mcp_results.json
│   └── code_execution_results.json
│
└── logs/                        # Application logs
    └── app.log
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or using uv:

```bash
uv sync
```

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=4096
OPENAI_TEMPERATURE=0.2

# Code Execution Configuration
CODE_EXECUTION_TIMEOUT=30

# MCP Configuration
MCP_CONFIG_PATH=mcp_config.json
```

### 3. Configure MCP Servers

Edit `mcp_config.json` to configure your MCP servers:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/your/directory"
      ],
      "description": "Filesystem operations"
    }
  }
}
```

**Note for Windows/WSL**: Use WSL-compatible paths (e.g., `/mnt/c/...`) or relative paths (`.`)

### 4. Run the Dashboard

```bash
python main.py
```

The dashboard will be available at:
- **Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 📊 Using the Dashboard

### Web Interface

1. **Enter Your Query**
   - Type a natural language query in the text area
   - Example: "Calculate total revenue in Sales_Records.csv"

2. **Run Benchmarks**
   - Click "Traditional MCP" to run LangChain-based benchmark
   - Click "Code Execution MCP" to run code generation benchmark
   - Or run both to see comparison

3. **View Results**
   - See execution time, token usage, and LLM calls
   - View token breakdown (prompt vs completion)
   - Read the output/answer

4. **Compare Performance**
   - Automatic winner detection based on time + token efficiency
   - Visual comparison with Chart.js
   - Detailed comparison table
   - Export results as CSV

### API Endpoints

The dashboard uses the following REST API endpoints:

#### Health Check
```bash
GET /health
```

#### Run Traditional MCP Benchmark
```bash
POST /traditional-mcp
Content-Type: application/json

{
  "query": "Your query here"
}
```

#### Run Code Execution MCP Benchmark
```bash
POST /code-execution-mcp
Content-Type: application/json

{
  "query": "Your query here"
}
```

#### Get Comparison Data
```bash
GET /compare
```

## 🔄 How It Works

### Traditional MCP Approach

1. **Tool Loading**: All MCP tools loaded into LangChain agent context
2. **LLM Invocation**: Agent selects appropriate tool for each step
3. **Direct Calls**: Each tool call goes through LLM for decision
4. **High Token Usage**: All tool definitions + intermediate results consume tokens

```python
# Traditional approach with LangChain
tools = create_mcp_tools()  # All tools loaded upfront
agent = create_agent(model=llm, tools=tools)
result = await agent.ainvoke({"messages": [query]})
```

### Code Execution MCP Approach

1. **Tool Discovery**: Agent discovers only needed tools via MCP protocol
2. **Code Generation**: LLM generates Python code to accomplish task
3. **Code Execution**: Code runs in isolated environment with MCP access
4. **Low Token Usage**: Only final results return to LLM

```python
# Code execution approach
orchestrator = RealMCPOrchestrator()
await orchestrator.initialize_async()
result = await orchestrator.run_multi_turn_async(query)
```

### Multi-Turn Conversation Flow

The Code Execution approach uses a progressive discovery pattern:

```
Turn 1: Explore
├─ Generate code to inspect CSV structure
├─ Execute: Get column names and types
└─ Status: "exploring"

Turn 2: Complete
├─ Generate code using discovered structure
├─ Execute: Calculate revenue total
└─ Status: "complete" (task done)
```

## 📈 Performance Comparison

### Typical Results

| Metric | Traditional MCP | Code Execution MCP | Improvement |
|--------|----------------|-------------------|-------------|
| **Execution Time** | 10-15s | 5-10s | 40-50% faster |
| **Total Tokens** | 8,000-10,000 | 1,500-3,000 | 70-80% fewer |
| **LLM Calls** | 5-8 calls | 1-2 calls | 60-80% fewer |
| **Cost per Query** | $0.10-$0.15 | $0.02-$0.04 | 75-85% cheaper |

### Why Code Execution Wins

1. **Progressive Disclosure**: Load only needed tools
2. **Context Efficiency**: Process large datasets in code, not LLM
3. **Complex Control Flow**: Loops/conditions in code, not chained tool calls
4. **Reduced Overhead**: Fewer LLM invocations = less latency

## 🐳 Docker Deployment

### Local Development

```bash
# Build and run with docker-compose
docker-compose -f docker/docker-compose.yml up --build

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### Google Cloud Platform (GCP)

#### Option 1: Cloud Run (Recommended)

```bash
# Build image
docker build -f docker/dockerfile -t mcp-benchmark-dashboard .

# Tag for GCR
docker tag mcp-benchmark-dashboard gcr.io/YOUR_PROJECT_ID/mcp-benchmark-dashboard

# Push to GCR
docker push gcr.io/YOUR_PROJECT_ID/mcp-benchmark-dashboard

# Deploy to Cloud Run
gcloud run deploy mcp-benchmark-dashboard \
  --image gcr.io/YOUR_PROJECT_ID/mcp-benchmark-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key_here
```

#### Option 2: Artifact Registry + Cloud Run

```bash
# Tag for Artifact Registry
docker tag mcp-benchmark-dashboard \
  us-central1-docker.pkg.dev/PROJECT_ID/REPO_NAME/mcp-benchmark-dashboard

# Push
docker push us-central1-docker.pkg.dev/PROJECT_ID/REPO_NAME/mcp-benchmark-dashboard

# Deploy
gcloud run deploy mcp-benchmark-dashboard \
  --image us-central1-docker.pkg.dev/PROJECT_ID/REPO_NAME/mcp-benchmark-dashboard \
  --platform managed
```

#### Option 3: Compute Engine with Docker Compose

```bash
# SSH into GCP VM
gcloud compute ssh your-vm-name

# Clone repository
git clone your-repo-url
cd Code_Execution_MCP_17_Nov

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run with docker-compose
docker-compose -f docker/docker-compose.yml up -d
```

## 🔒 Security

The code executor implements security measures:

- **Subprocess Isolation**: Code runs in separate process
- **Timeout Limits**: 30-second execution timeout
- **Restricted Imports**: Limited to safe Python modules
- **Output Capture**: All stdout/stderr captured and sanitized
- **Error Handling**: Try/except blocks for all MCP operations
- **Non-Root User**: Docker container runs as unprivileged user

## 🛠️ Adding New MCP Servers

To add a new MCP server, update `mcp_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "description": "Filesystem operations"
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      },
      "description": "GitHub API operations"
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://user:password@localhost/dbname"
      ],
      "description": "PostgreSQL database operations"
    }
  }
}
```

The agent will automatically discover tools from all configured servers.

### Finding MCP Servers

- **Official servers**: https://github.com/modelcontextprotocol/servers
- **Community servers**: https://github.com/topics/mcp-server
- **MCP directory**: https://mcp.run

## 📝 Development

### Project Structure Principles

- **Clean Architecture**: Separation of concerns (API, Core, Utils)
- **Type Safety**: Pydantic models for all API requests/responses
- **Logging**: Comprehensive logging throughout application
- **Documentation**: Docstrings and inline comments
- **Error Handling**: Try/except blocks with proper error messages

### Code Organization

```
app/
├── api/          # Web layer (routes, models)
├── benchmarks/   # Business logic (benchmark implementations)
├── core/         # Core functionality (MCP, agent, execution)
├── config/       # Configuration management
├── app_logging/  # Logging utilities
├── utils/        # Helper functions
└── prompts/      # LLM prompts
```

### Running Tests

```bash
# Run benchmarks from command line
python main.py

# Test specific query
# Use the web interface at http://localhost:8000

# View API documentation
# Open http://localhost:8000/docs
```

## 🎨 UI Customization

The dashboard uses a modern black theme with:

- **Glassmorphism**: Frosted glass card effects
- **Responsive Design**: Works on desktop and mobile
- **Interactive Charts**: Chart.js for visualizations
- **Real-time Updates**: Dynamic result rendering
- **Export Feature**: Download results as CSV

To customize:
- Edit `static/css/style.css` for styling
- Modify `static/js/app.js` for functionality
- Update `static/index.html` for structure

## 🐛 Troubleshooting

### Common Issues

**Issue**: MCP server initialization hangs
- **Solution**: Check MCP server paths in `mcp_config.json`
- For Windows/WSL, use WSL-compatible paths or relative paths

**Issue**: "OPENAI_API_KEY not found"
- **Solution**: Ensure `.env` file exists with valid API key

**Issue**: "Module not found" errors
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Port 8000 already in use
- **Solution**: Change port in `main.py` or kill existing process

**Issue**: Docker build fails
- **Solution**: Ensure Docker daemon is running and you have internet access

## 📊 Benchmark Results Storage

Results are stored in JSON format:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "query": "Calculate total revenue",
  "result": {
    "success": true,
    "time": 5.2,
    "llm_calls": 2,
    "tokens": {
      "prompt_tokens": 1200,
      "completion_tokens": 150,
      "total_tokens": 1350
    },
    "output": "Total revenue: $384,949.43"
  }
}
```

Files:
- `data/traditional_mcp_results.json` - Traditional approach results
- `data/code_execution_results.json` - Code execution approach results

## 🔗 API Response Format

### Benchmark Response
```json
{
  "success": true,
  "approach": "code_execution_mcp",
  "result": {
    "success": true,
    "final_output": "Total revenue: $384,949.43",
    "error": null,
    "time": 5.06,
    "llm_calls": [
      {
        "call_number": 1,
        "latency": 2.53,
        "tokens": {
          "prompt_tokens": 1154,
          "completion_tokens": 139,
          "total_tokens": 1293
        }
      }
    ],
    "total_tokens": {
      "prompt_tokens": 1154,
      "completion_tokens": 139,
      "total_tokens": 1293
    }
  },
  "message": "Benchmark completed successfully"
}
```

## 🎯 Use Cases

1. **Data Analysis**: Query CSV files, calculate statistics
2. **File Operations**: Read, write, list, search files
3. **Multi-step Tasks**: Complex workflows requiring multiple tools
4. **Performance Testing**: Compare different agent approaches
5. **Educational**: Learn about MCP and agentic workflows

## 📚 References

- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Chart.js Documentation](https://www.chartjs.org)

## 🤝 Contributing

This is a demonstration project. For production use, consider:

- ✅ Enhanced security sandboxing (containers, VMs)
- ✅ Rate limiting and request throttling
- ✅ User authentication and authorization
- ✅ Database for result persistence
- ✅ Caching layer for repeated queries
- ✅ Monitoring and alerting
- ✅ Comprehensive test suite
- ✅ CI/CD pipeline

## 📄 License

This is a demonstration project for educational purposes.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework
- [OpenAI API](https://openai.com) - LLM for code generation
- [MCP SDK](https://modelcontextprotocol.io) - Model Context Protocol
- [LangChain](https://langchain.com) - Agent framework
- [Chart.js](https://www.chartjs.org) - Data visualization
- [Uvicorn](https://www.uvicorn.org) - ASGI server

---

**Made with ❤️ for efficient AI agents**
