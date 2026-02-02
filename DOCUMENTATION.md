# AI Code Execution with MCP - Complete Documentation

> Comprehensive guide to the MCP Benchmark Dashboard, including architecture, technical concepts, and usage instructions.

---

## 📚 Table of Contents

1. [Unified Dashboard](#unified-dashboard)
   - [Overview](#overview)
   - [Key Features](#key-features)
   - [Architecture](#architecture)
   - [Getting Started](#getting-started)
   - [API Reference](#api-reference)

2. [LLM Trace & Conversation History](#llm-trace--conversation-history)
   - [Overview](#trace-overview)
   - [Implementation Details](#implementation-details)
   - [UI Structure](#ui-structure)
   - [Usage Tips](#usage-tips)

3. [Technical Deep Dive](#technical-deep-dive)
   - [STDIO, Pipes, and IPC](#stdio-pipes-and-ipc)
   - [Dynamic Code Execution](#dynamic-code-execution)
   - [Output Capture & Redirection](#output-capture--redirection)
   - [Docker Container Communication](#docker-container-communication)

---

# Unified Dashboard

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
- Upload tasks from JSON files
- Run batch comparisons
- View aggregate statistics
- Interactive charts for time and token comparisons
- Detailed results with LLM trace history for each task
- Download results as JSON

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
- Detailed results view with collapsible LLM traces

### 5. **New JavaScript Features**
Added to `/static/js/app.js`:
- `initializeMultiTaskMode()` - Set up multi-task functionality
- `addTaskItem()` - Dynamically add tasks
- `runAllTasks()` - Execute batch benchmarks
- `displayMultiTaskResults()` - Show results with charts
- `handleFileUpload()` - Upload tasks from JSON
- `downloadResults()` - Export results as JSON
- Chart.js integration for visual comparisons

### 6. **Simplified Launcher**
Updated `/launcher.py`:
- Single menu option to start dashboard
- Uses `main.py` which already shares MCP client correctly
- No more multiprocessing/threading complexity

## Getting Started

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
2. **Option A: Manual Entry**
   - Click "+ Add Task" to add tasks
   - Fill in:
     - Task ID (e.g., task_1)
     - Query (e.g., "Calculate total revenue in Sales_Records.csv")
3. **Option B: Upload JSON**
   - Click "Upload Tasks JSON"
   - Select a JSON file with this format:
     ```json
     {
       "tasks": [
         {
           "task_id": "task_1",
           "user_query": "Your query here"
         }
       ]
     }
     ```
4. Set max LLM turns (default: 3)
5. Click "Run All Tasks"
6. View:
   - Summary statistics
   - Time comparison chart
   - Token usage chart
   - Detailed results for each task
   - LLM trace history (expand to see turn-by-turn details)
7. Download results as JSON

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
- Full LLM trace history

## API Reference

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
      "code_execution_mcp": {
        "success": true,
        "time": 5.2,
        "output": "...",
        "llm_calls": 3,
        "total_tokens": 5590,
        "turn_details": [...]
      },
      "traditional_mcp": {
        "success": true,
        "time": 8.1,
        "output": "...",
        "llm_calls": 3,
        "total_tokens": 8234,
        "turn_details": [...]
      },
      "comparison": {
        "time_diff": -2.9,
        "time_improvement_pct": 35.8,
        "token_diff": -2644,
        "token_reduction_pct": 32.1
      }
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

### Technical Details

#### Shared MCP Client

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

#### Frontend Architecture

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

---

# LLM Trace & Conversation History

## Trace Overview

The dashboard provides detailed trace messages and conversation history for each LLM call, showing the agent's thinking process and execution results with an intuitive collapsible UI.

## Implementation Details

### Backend Components

#### 1. **Orchestrator (Code Execution MCP)**
Located in `app/core/orchestrator.py`:
- Returns `conversation_history` - Full message history
- Returns `turn_details` - Formatted turn information
- `_format_turn_details()` method extracts:
  - Turn number
  - LLM request (prompt)
  - LLM response (generated code + reasoning)
  - Execution result
  - Latency and token usage

#### 2. **Traditional MCP Benchmark**
Located in `app/benchmarks/traditional_mcp.py`:
- Returns `conversation_history` - Captured from agent
- Returns `turn_details` - Formatted turn information
- `_format_turn_details()` method extracts similar data

### Frontend Components

#### JavaScript Changes (`static/js/app.js`)

**Updated `formatLLMCalls` Function:**
```javascript
const formatLLMCalls = (calls, turnDetails) => {
    // Accepts turnDetails parameter
    // Creates collapsible <details> elements for each call
    // Shows request, response, and execution results
}
```

**Features:**
- ▶ Collapsible sections for each turn
- 📤 Request to LLM (full prompt)
- 🤖 LLM Response (code + reasoning)
- ⚙️ Execution Result (what happened)
- Token and latency info in summary
- Proper JSON formatting with HTML escaping

#### CSS Styles (`static/css/style.css`)

**New Styles:**
- `.llm-call-details` - Collapsible container
- `.llm-call-summary` - Clickable header with arrow
- `.summary-arrow` - Rotates on expand
- `.llm-call-content` - Expanded content area
- `.llm-message` - Individual message boxes
- `.llm-request` - Orange accent for requests
- `.llm-response` - Green accent for responses
- `.llm-execution` - Cyan accent for execution results
- `.message-content` - Styled code blocks with scrolling

## UI Structure

### Collapsed View:
```
▶ Turn 1    2.82s    1608 tokens (1469 prompt + 139 completion)
▶ Turn 2    2.70s    1848 tokens (1714 prompt + 134 completion)
▶ Turn 3    2.21s    2134 tokens (1995 prompt + 139 completion)
```

### Expanded View (Turn 1):
```
▼ Turn 1    2.82s    1608 tokens (1469 prompt + 139 completion)
  
  ┌─────────────────────────────────────────────┐
  │ 📤 REQUEST TO LLM:                          │
  │ {                                           │
  │   "role": "user",                           │
  │   "content": "List all files..."           │
  │ }                                           │
  └─────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────┐
  │ 🤖 LLM RESPONSE:                            │
  │ {                                           │
  │   "status": "exploring",                    │
  │   "code": "import mcp_call...",            │
  │   "reasoning": "I'll use filesystem..."    │
  │ }                                           │
  └─────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────┐
  │ ⚙️ EXECUTION RESULT:                        │
  │ Execution result:                           │
  │ [FILE] main.py                             │
  │ [DIR] app                                  │
  │ ...                                        │
  └─────────────────────────────────────────────┘
```

### Information Hierarchy:
```
Task Result
├─ Quick Metrics (always visible)
│  ├─ Success badges
│  ├─ Time comparison
│  └─ Token comparison
│
└─ Full Results (collapsible)
   ├─ Code Execution MCP
   │  ├─ Final Output
   │  └─ LLM Calls (collapsible)
   │     ├─ Turn 1 (collapsible)
   │     │  ├─ Request
   │     │  ├─ Response
   │     │  └─ Execution Result
   │     ├─ Turn 2 (collapsible)
   │     └─ Turn 3 (collapsible)
   │
   └─ Traditional MCP
      ├─ Final Output
      └─ LLM Calls (collapsible)
         └─ Similar structure
```

## Visual Design

### Color Coding:
- **Orange/Yellow** (`--warning-color`) - Requests to LLM
- **Green** (`--code-exec-color`) - LLM Responses
- **Cyan** (`--success-color`) - Execution Results

### Animations:
- Arrow rotation on expand (0.3s ease)
- Background transitions on hover (0.2s ease)
- Smooth border color transitions

### Accessibility:
- Proper semantic HTML (`<details>`, `<summary>`)
- Keyboard navigable (native details support)
- Clear visual hierarchy
- Scrollable content with custom scrollbars

## Data Flow

```
Backend → Frontend → UI Display

1. run_multi_turn_async() / run_benchmark_async()
   └─> Captures conversation_history
   └─> Calls _format_turn_details()
   └─> Returns in API response

2. displayDetailedResults(results)
   └─> Calls formatLLMCalls(calls, turnDetails)
   └─> Generates HTML with <details> elements
   └─> Displays with proper formatting

3. User Interaction
   └─> Click to expand/collapse
   └─> Smooth animations
   └─> View complete trace
```

## Usage Tips

### Navigation:
1. Run multiple tasks
2. View results summary
3. Expand task details
4. See "View Full Results & Outputs"
5. Expand individual LLM calls (turns)
6. See complete conversation flow

### Best Practices:
- **Start Collapsed** - Overview first, details on demand
- **Expand Interesting Turns** - Focus on specific calls
- **Compare Side-by-Side** - Code Exec vs Traditional
- **Export Results** - Download JSON with full traces
- **Study Patterns** - Learn from successful approaches

## Benefits

1. **Full Transparency** - See exactly what the LLM is thinking
2. **Debugging** - Understand why certain decisions were made
3. **Learning** - Study how agents solve problems
4. **Comparison** - Compare approaches turn-by-turn
5. **Troubleshooting** - Identify where things went wrong
6. **Documentation** - Export complete traces for analysis

---

# Technical Deep Dive

## STDIO, Pipes, and IPC

A comprehensive guide to understanding streams, pipes, and binary communication protocols.

### What are Streams?

**A stream is a sequence of data elements made available over time.**

Think of it like a water pipe:
- Data flows in one direction
- You can't see all the data at once
- You read what's available or wait for more

```
Source → [Stream] → Destination
         ^^^^^^^^
         Flows over time
```

#### Key Properties

- **Sequential**: Data arrives in order
- **Unidirectional**: Data flows one way (unless you have two pipes)
- **Buffered**: OS may hold data temporarily
- **Blocking**: Operations wait if no data is available

### The Three Standard Streams

Every program has three default streams:

#### 1. **stdin** (Standard Input)
- **File Descriptor**: 0
- **Direction**: INTO the program
- **Purpose**: Receive input data

```python
import sys
data = sys.stdin.read()  # Read from stdin
```

#### 2. **stdout** (Standard Output)
- **File Descriptor**: 1
- **Direction**: OUT of the program
- **Purpose**: Send normal output

```python
import sys
sys.stdout.write("Hello\n")  # Write to stdout
print("Hello")                # Also writes to stdout
```

#### 3. **stderr** (Standard Error)
- **File Descriptor**: 2
- **Direction**: OUT of the program
- **Purpose**: Send error messages and diagnostics

```python
import sys
sys.stderr.write("Error!\n")  # Write to stderr
print("Error!", file=sys.stderr)  # Alternative
```

#### Why Three Streams?

```
Program Flow:
┌─────────────────────┐
│      Program        │
│                     │
stdin  →  0 ────────→│
                     │
        stdout ←─── 1 │  ← Normal output
                     │
        stderr ←─── 2 │  ← Errors/diagnostics
└─────────────────────┘
```

**Benefits:**
- Can redirect output and errors separately
- Errors don't pollute normal output
- Can pipe stdout to another program while still seeing errors

### Pipes: Connecting Processes

**A pipe connects the output of one process to the input of another.**

#### Creating Pipes in Python

```python
import asyncio

process = await asyncio.create_subprocess_exec(
    'python', 'script.py',
    stdin=asyncio.subprocess.PIPE,   # Create pipe for input
    stdout=asyncio.subprocess.PIPE,  # Create pipe for output
    stderr=asyncio.subprocess.PIPE   # Create pipe for errors
)
```

#### Visual Diagram

```
┌─────────────────┐                    ┌─────────────────┐
│   Parent        │                    │   Child         │
│   Process       │                    │   Process       │
│                 │                    │                 │
│  stdin.write()  │──── PIPE ────────→│  stdin.read()   │
│                 │     [Data flows]   │                 │
│  stdout.read()  │←─── PIPE ─────────│  stdout.write() │
│                 │     [Data flows]   │                 │
│  stderr.read()  │←─── PIPE ─────────│  stderr.write() │
│                 │     [Data flows]   │                 │
└─────────────────┘                    └─────────────────┘
```

#### Pipe Properties

- **Bidirectional setup**: Can create pipes in both directions
- **Buffered**: OS buffers data between processes
- **Byte-oriented**: Pipes transfer binary data (bytes)
- **No random access**: Can't seek backwards, only forward

### Strings vs Bytes

#### The Fundamental Difference

**Strings (str)**: Abstract text representation
```python
text = "Hello 世界 🐍"
type(text)  # <class 'str'>
len(text)   # 10 characters
```

**Bytes (bytes)**: Binary data, what computers actually transmit
```python
data = text.encode('utf-8')
type(data)  # <class 'bytes'>
len(data)   # 16 bytes (emoji and Chinese take multiple bytes)
# b'Hello \xe4\xb8\x96\xe7\x95\x8c \xf0\x9f\x90\x8d'
```

#### Why the Distinction Matters

**Pipes only understand BYTES!**

```python
# ❌ This FAILS:
process.stdin.write("Hello")  
# TypeError: a bytes-like object is required, not 'str'

# ✅ This WORKS:
process.stdin.write("Hello".encode('utf-8'))
# or
process.stdin.write(b"Hello")
```

#### Encoding and Decoding

```python
# String → Bytes (Encoding)
text = "Hello"
data = text.encode('utf-8')  # b'Hello'

# Bytes → String (Decoding)
data = b'Hello'
text = data.decode('utf-8')  # 'Hello'
```

#### UTF-8: The Universal Standard

**Why UTF-8?**
- ✅ Supports ALL Unicode characters (every language, emoji, symbols)
- ✅ Backward compatible with ASCII
- ✅ Variable length (efficient for English, works for everything)
- ✅ Default for Python 3 and most systems

```python
# Examples of UTF-8 efficiency:
"A".encode('utf-8')      # b'A'              (1 byte)
"ñ".encode('utf-8')      # b'\xc3\xb1'      (2 bytes)
"世".encode('utf-8')      # b'\xe4\xb8\x96'  (3 bytes)
"🐍".encode('utf-8')     # b'\xf0\x9f\x90\x8d' (4 bytes)
```

### Reading from Streams

#### `read()` - Read Until EOF

```python
data = stream.read()  # Read ALL data until stream closes
```

**Behavior:**
- Blocks until EOF (End of File) signal
- Returns all accumulated data
- Only returns when stream closes

**Use cases:**
- Reading entire files
- One-shot commands that exit
- When you want everything

#### `read(size)` - Read Exact Amount

```python
data = stream.read(100)  # Read exactly 100 bytes
```

**Behavior:**
- Blocks until `size` bytes are available (or EOF)
- Returns as soon as `size` bytes are read
- Doesn't wait for EOF

**Use cases:**
- Known data sizes
- Protocol with length prefix
- Persistent connections

#### `readline()` - Read Until Newline

```python
line = stream.readline()  # Read until '\n'
```

**Behavior:**
- Reads until it finds `\n` character
- Returns the line including the `\n`
- Good for line-based protocols

**Use cases:**
- Text-based protocols
- Reading log files
- Line-oriented data

#### Comparison Table

| Method | Stops When | Best For |
|--------|-----------|----------|
| `read()` | EOF (stream closes) | Files, one-shot commands |
| `read(size)` | Got `size` bytes | Binary protocols, known sizes |
| `readline()` | Found `\n` | Text lines, logs |

### EOF (End of File)

**EOF is a signal that means "no more data will ever come from this stream."**

#### What EOF Really Means

EOF is **NOT a character** - it's a **state** of the stream:
- The stream is closed
- No more data will arrive
- Reading will return empty bytes

```python
data = stream.read()
if len(data) == 0:  # This is EOF!
    print("Stream closed (EOF)")
```

#### When EOF Happens

**1. File Reading**
```python
with open('file.txt', 'rb') as f:
    data = f.read()  # Reads until end of file (EOF)
# File has natural end → EOF exists
```

**2. Process Exits**
```python
process = subprocess.Popen(['ls', '-la'], stdout=PIPE)
output = process.stdout.read()  # Waits for 'ls' to finish
# When 'ls' exits → stdout closes → EOF → read() returns
```

**3. Explicit Close**
```python
# Sender side:
pipe.close()  # Explicitly close the pipe

# Receiver side:
data = pipe.read()  # Gets EOF (empty bytes)
```

#### When EOF Does NOT Happen

**Persistent Connections:**
```python
# Server keeps running
process = await create_subprocess_exec(
    'python', 'server.py',
    stdin=PIPE, stdout=PIPE
)

# stdin is OPEN but may be empty
data = process.stdin.read()  # ⏳ HANGS FOREVER!
# Process is alive, stdin is open → no EOF → waits forever
```

#### The EOF Problem in Persistent Connections

```
Timeline of read() with persistent connection:

[T=0]  Start: data = stream.read()
       Stream state: OPEN, empty
       Action: Block, waiting for data or EOF

[T=1]  Data arrives: "hello"
       Stream state: OPEN, has data
       Action: Read "hello", but keep waiting (no EOF yet)

[T=2]  More data? Maybe?
       Stream state: OPEN, empty
       Action: Keep blocking, waiting for EOF

[T=∞]  Still waiting...
       Stream state: OPEN (never closes)
       Result: ⏳ HANGS FOREVER
```

### Writing and Flushing

#### The Buffer Problem

When you write to a stream, data doesn't go immediately - it's **buffered**:

```
Your code → [Buffer in memory] → [Pipe/Network]
            ^^^^^^^^^^^^^^^^^^
            Data sits here until flushed!
```

#### Why Buffering Exists

**Performance optimization:**
- Writing to OS/network is expensive
- Buffer many small writes into one big write
- Reduces system calls

**But causes problems:**
- Data might not be sent immediately
- Receiver waits for data that's stuck in buffer
- Interactive protocols need immediate transmission

#### Flushing: Force Data to Send

```python
# Write data
stream.write(data)  # Goes to buffer (not sent yet!)

# Flush the buffer
await stream.drain()  # Force send now!
# or
stream.flush()  # Synchronous version
```

#### When to Flush

**✅ Always flush when:**
1. Interactive protocols (expecting immediate response)
2. End of a message in a protocol
3. Before waiting for a response
4. Sending status/ready signals

**❌ Don't need to flush when:**
1. Writing large amounts of data continuously
2. About to close the stream anyway
3. Performance is critical and you have many small writes

### The Length-Prefix Protocol

#### The Problem: Message Boundaries

In a persistent connection, how do you know where one message ends and the next begins?

```
Pipe contains: [message1message2message3]
                       ↑        ↑
               Where do messages split?
```

#### Solution: Length Prefix

**Send the length FIRST, then the data:**

```
Format: [4-byte length][actual data]

Example:
[0x00][0x00][0x01][0xA4][... 420 bytes of data ...]
 \________length_______/\________payload________/
     (420 in binary)
```

#### Implementation

**Sending Side:**
```python
# 1. Prepare data
message = "Hello, World!"
message_bytes = message.encode('utf-8')  # Convert to bytes

# 2. Calculate length
length = len(message_bytes)  # 13 bytes

# 3. Convert length to 4-byte integer (big-endian)
length_bytes = length.to_bytes(4, 'big')
# 13 → [0x00, 0x00, 0x00, 0x0D]

# 4. Send length first
stream.write(length_bytes)

# 5. Send actual data
stream.write(message_bytes)

# 6. Flush to ensure it's sent
await stream.drain()
```

**Receiving Side:**
```python
# 1. Read length (always 4 bytes)
length_bytes = stream.read(4)

# 2. Convert bytes to integer
length = int.from_bytes(length_bytes, 'big')
# [0x00, 0x00, 0x00, 0x0D] → 13

# 3. Read exact amount of data
message_bytes = stream.read(length)  # Read exactly 13 bytes

# 4. Convert bytes to string
message = message_bytes.decode('utf-8')
# Result: "Hello, World!"
```

#### Why 4 Bytes?

```
1 byte  = 0 to 255              (256 bytes max)        ❌ Too small
2 bytes = 0 to 65,535           (64 KB max)           ❌ Still limiting
4 bytes = 0 to 4,294,967,295    (4 GB max)            ✅ Perfect!
8 bytes = 0 to huge             (16 exabytes max)     ⚠️  Overkill
```

4 bytes (32 bits) can represent up to 4GB - plenty for any message!

#### Big-Endian Byte Order

The number 420 (0x1A4) in different byte orders:

**Big-endian (network standard):**
```
[0x00][0x00][0x01][0xA4]
  MSB ────────────→ LSB
  Most significant first
```

**Little-endian (Intel CPUs):**
```
[0xA4][0x01][0x00][0x00]
  LSB ←──────────── MSB
  Least significant first
```

**Always use 'big' for network protocols** - it's the standard!

#### Advantages of Length-Prefix Protocol

| Feature | Benefit |
|---------|---------|
| **No EOF needed** | Works with persistent connections |
| **Binary safe** | Can send any data, including delimiters |
| **Efficient** | No escaping or scanning for delimiters |
| **Simple** | Easy to implement correctly |
| **Standard** | Used by many protocols |

### Persistent vs One-Shot Communication

#### One-Shot Communication

**Pattern:** Connect → Send → Receive → Close

```python
# Example: Running a command
process = subprocess.run(
    ['python', 'script.py'],
    input=b"some data",
    capture_output=True
)
# Process runs, gets input, produces output, exits
# stdout closes → EOF → we get the output
```

**Lifecycle:**
```
[Start] → [Send Data] → [Process] → [Exit/EOF] → [Get Result]
  └────────── One execution, then done ──────────┘
```

**Characteristics:**
- ✅ EOF naturally occurs (process exits)
- ✅ Simple: `read()` until EOF works
- ❌ Overhead: New process per request
- ❌ Slow: Startup time every time

#### Persistent Communication

**Pattern:** Connect once → Send/Receive many times → Close when done

```python
# Example: Long-running server
process = await create_subprocess_exec(
    'python', 'server.py',
    stdin=PIPE, stdout=PIPE, stderr=PIPE
)

# Send multiple requests over same connection
for i in range(10):
    await send_request(process, f"request {i}")
    response = await read_response(process)

# Finally close when done
await process.terminate()
```

**Lifecycle:**
```
[Start] → [Req1] → [Resp1] → [Req2] → [Resp2] → ... → [Close]
  └─────── Multiple requests on same connection ─────────┘
```

**Characteristics:**
- ✅ Fast: No startup overhead per request
- ✅ Efficient: Reuse same process
- ❌ Need protocol: Can't use EOF for message boundaries
- ✅ Solution: Length-prefix or other protocol

#### Comparison

| Aspect | One-Shot | Persistent |
|--------|----------|-----------|
| **Process lifecycle** | Start/stop per request | Long-running |
| **EOF signal** | Yes (process exits) | No (during operation) |
| **Message boundaries** | EOF marks the end | Need protocol (length-prefix) |
| **Performance** | Slower (startup overhead) | Faster (reuse connection) |
| **Complexity** | Simple | Need protocol |
| **Best for** | Occasional tasks | High-frequency communication |

## Docker Container Communication

### The Architecture

```
┌─────────────────────────┐         ┌──────────────────────────┐
│  Host Process           │         │  Docker Container        │
│  (Python)               │         │  (Python)                │
│                         │         │                          │
│  DockerCodeExecutor     │         │  execution_server.py     │
│                         │         │                          │
│  stdin.write() ────────→│─ PIPE ─→│  stdin.read()           │
│                         │         │  [Execute code]          │
│  stdout.read() ←────────│← PIPE ──│  stdout.write()         │
│                         │         │                          │
└─────────────────────────┘         └──────────────────────────┘
```

### Why Persistent Connection?

**Goal:** Execute multiple Python code snippets without restarting container

**Benefits:**
- 🚀 10-15x faster (no container startup per request)
- 💰 Lower resource usage
- 🔄 Keep state between executions (if needed)

### The Protocol Implementation

#### Host Side (docker_executor.py)

```python
async def execute_async(self, code: str):
    # 1. Encode code to bytes
    code_bytes = code.encode('utf-8')
    
    # 2. Create 4-byte length prefix
    length_bytes = len(code_bytes).to_bytes(4, 'big')
    
    # 3. Send length + code
    self.process.stdin.write(length_bytes)
    self.process.stdin.write(code_bytes)
    await self.process.stdin.drain()  # Flush!
    
    # 4. Read response length (4 bytes)
    response_length_bytes = await self.process.stdout.readexactly(4)
    response_length = int.from_bytes(response_length_bytes, 'big')
    
    # 5. Read exact response
    response_bytes = await self.process.stdout.readexactly(response_length)
    response = json.loads(response_bytes.decode('utf-8'))
    
    return response
```

#### Container Side (execution_server.py)

```python
async def main_loop():
    # Signal ready
    print("READY", file=sys.stderr, flush=True)
    
    while True:
        # 1. Read 4-byte length
        length_bytes = sys.stdin.buffer.read(4)
        if not length_bytes:  # EOF = connection closed
            break
        
        # 2. Convert to integer
        length = int.from_bytes(length_bytes, 'big')
        
        # 3. Read exact amount of code
        code_bytes = sys.stdin.buffer.read(length)
        code = code_bytes.decode('utf-8')
        
        # 4. Execute code
        result = await execute_code(code)
        
        # 5. Encode result
        result_json = json.dumps(result).encode('utf-8')
        
        # 6. Send length + result
        sys.stdout.buffer.write(len(result_json).to_bytes(4, 'big'))
        sys.stdout.buffer.write(result_json)
        sys.stdout.buffer.flush()  # Important!
        
        # Ready for next message!
```

### Message Flow Example

```
Host                           Container
  |                               |
  |-- [Length: 420 bytes] ------->|
  |-- [420 bytes of code] ------->|
  |                               |
  |                               |-- Executing code...
  |                               |
  |<------ [Length: 156 bytes] ---|
  |<------ [156 bytes JSON] ------|
  |                               |
  |-- [Length: 523 bytes] ------->|  (Next request!)
  |-- [523 bytes of code] ------->|
  |                               |
  ...continues indefinitely...
```

### Key Design Decisions

1. **READY signal on stderr** - Separates startup signal from data channel
2. **Binary protocol** - Can send any data (including non-UTF-8)
3. **4-byte length** - Up to 4GB messages (way more than needed)
4. **Big-endian** - Network standard byte order
5. **Flush after write** - Immediate delivery (interactive protocol)
6. **EOF check** - Gracefully handle connection closure

## Dynamic Code Execution

**`exec()` is Python's way to execute code dynamically from a string.**

### Basic Usage

```python
code = """
x = 10
y = 20
result = x + y
print(f"Result: {result}")
"""

exec(code)
# Prints: Result: 30
```

### The Critical Truth: `exec()` Returns `None`

```python
code = """
def calculate():
    return 42

result = calculate()
"""

return_value = exec(code)
print(return_value)  # None (always!)
```

**`exec()` ALWAYS returns `None`, regardless of what the code does!**

This is why we need alternative ways to get results (print, namespace inspection, etc.)

### How `exec()` Works

**Signature:**
```python
exec(code, globals=None, locals=None)
```

**Parameters:**
1. **code** - String of Python code to execute
2. **globals** - Dictionary for global variables
3. **locals** - Dictionary for local variables (usually same as globals)

### The Three Ways to Call `exec()`

#### 1. No namespace (dangerous!)
```python
exec("x = 10")
print(x)  # 10 - variable is in current scope!
# ⚠️ Pollutes your namespace!
```

#### 2. With globals only
```python
namespace = {}
exec("x = 10", namespace)
print(namespace['x'])  # 10 ✅
# x is NOT in your scope, only in namespace
```

#### 3. With globals and locals (recommended)
```python
namespace = {}
exec("x = 10", namespace, namespace)
#              ^^^^^^^^^ ^^^^^^^^^
#              globals   locals (same dict)
print(namespace['x'])  # 10 ✅
```

**Best practice:** Use same dict for both globals and locals so imports work correctly.

### What Can You Execute?

#### ✅ Works: Statements
```python
exec("x = 10")              # Assignment
exec("print('hello')")      # Function call
exec("if True: x = 1")      # Conditionals
exec("for i in range(5): print(i)")  # Loops
exec("def f(): pass")       # Function definition
exec("class C: pass")       # Class definition
```

#### ❌ Doesn't Work: Top-level return
```python
exec("return 42")  # SyntaxError: 'return' outside function
```

#### ⚠️ Works but useless: Expressions
```python
exec("42")  # Valid, but result is lost!
exec("10 + 32")  # Calculates but returns None
```

**Use `eval()` for expressions:**
```python
result = eval("10 + 32")  # 42 ✅
```

### Security Warning ⚠️

**`exec()` executes ARBITRARY code with full privileges!**

```python
# Malicious code:
exec("import os; os.system('rm -rf /')")  # 💀 DANGER!
exec("open('/etc/passwd').read()")        # 💀 Data theft!
```

**Always run in isolated environment:**
- ✅ Docker container (your approach)
- ✅ Virtual machine
- ✅ Sandboxed interpreter
- ❌ NEVER directly on host with untrusted code

### Namespaces and Variable Scope

**A namespace is a dictionary that holds variables and their values.**

Think of it as a **separate universe** where code runs:

```python
# Your Python code (Universe A)
my_var = "host"

# Executed code (Universe B)
namespace = {}
exec("my_var = 'exec'", namespace)

print(my_var)              # "host" (Universe A)
print(namespace['my_var']) # "exec" (Universe B)

# They're separate! No collision!
```

#### Creating a Clean Namespace

```python
# Minimal namespace
namespace = {
    '__builtins__': __builtins__,  # Built-in functions (print, len, etc.)
}

exec("x = 10", namespace)
print(namespace['x'])  # 10
```

#### What's in `__builtins__`?

```python
# Without __builtins__:
namespace = {}
exec("print('hello')", namespace)
# NameError: name 'print' is not defined

# With __builtins__:
namespace = {'__builtins__': __builtins__}
exec("print('hello')", namespace)
# 'hello' ✅ Works!
```

**`__builtins__` provides:**
- `print()`, `len()`, `range()`, `str()`, etc.
- Basic exceptions: `ValueError`, `TypeError`, etc.
- Type constructors: `list()`, `dict()`, `int()`, etc.

#### Setting `__name__` for Main Guard

```python
code = """
def main():
    print("Hello from main!")

if __name__ == '__main__':
    main()
"""

# ❌ Without __name__:
namespace = {'__builtins__': __builtins__}
exec(code, namespace)
# Nothing prints! __name__ is not '__main__'

# ✅ With __name__:
namespace = {
    '__builtins__': __builtins__,
    '__name__': '__main__',  # ← This is key!
}
exec(code, namespace)
# "Hello from main!" ✅ main() is called!
```

#### Pre-loading Modules

```python
import asyncio

namespace = {
    '__builtins__': __builtins__,
    '__name__': '__main__',
    'asyncio': asyncio,  # Pre-import modules
}

code = """
async def fetch():
    await asyncio.sleep(1)  # asyncio is available!
    return "done"
"""

exec(code, namespace)
```

#### Namespace After Execution

```python
namespace = {
    '__builtins__': __builtins__,
    '__name__': '__main__',
}

code = """
x = 10
y = 20
result = x + y

def calculate(a, b):
    return a * b

answer = calculate(5, 6)
"""

exec(code, namespace)

# Namespace now contains:
print(namespace.keys())
# dict_keys(['__builtins__', '__name__', 'x', 'y', 'result', 'calculate', 'answer'])

# Access variables:
print(namespace['x'])        # 10
print(namespace['result'])   # 30
print(namespace['answer'])   # 30
print(namespace['calculate']) # <function calculate>
```

## Output Capture & Redirection

**How to capture `print()` output from dynamically executed code.**

### The Problem

```python
code = """
print("Hello")
print("World")
"""

exec(code)
# Prints to terminal:
# Hello
# World
# But we can't capture it! 😞
```

### The Solution: `io.StringIO()` + `contextlib.redirect_stdout()`

#### Step 1: Create In-Memory Buffer

```python
import io

capture = io.StringIO()
# This creates a "fake file" in memory
# Like a bucket that collects text
```

**What is StringIO?**
- Acts like a file object
- But exists entirely in RAM (no disk)
- Has methods: `write()`, `read()`, `getvalue()`

```python
# Using StringIO like a file:
buffer = io.StringIO()
buffer.write("Hello\n")
buffer.write("World\n")

# Get all the content:
content = buffer.getvalue()  # "Hello\nWorld\n"
```

#### Step 2: Redirect stdout

```python
import contextlib

with contextlib.redirect_stdout(capture):
    # Inside this block, print() goes to 'capture'
    print("Hello")
    print("World")

# Outside the block, print() goes back to normal
print("Back to terminal")
```

**What `redirect_stdout()` does:**
```
Normal:
  print() → sys.stdout → Terminal

With redirect_stdout(capture):
  print() → sys.stdout → capture (StringIO) → Memory buffer
```

#### Step 3: Execute Code with Redirection

```python
import io
import contextlib

# Create buffer
capture = io.StringIO()

# Code to execute
code = """
print("Line 1")
print("Line 2")
result = 10 + 32
print(f"Result: {result}")
"""

# Execute with redirection
with contextlib.redirect_stdout(capture):
    exec(code)

# Get captured output
output = capture.getvalue()
print(output)
# Line 1
# Line 2
# Result: 42
```

### Capturing Both stdout and stderr

```python
import io
import contextlib

stdout_capture = io.StringIO()
stderr_capture = io.StringIO()

code = """
print("Normal output")
print("Error message!", file=sys.stderr)
print("More output")
"""

# Redirect both streams
with contextlib.redirect_stdout(stdout_capture), \
     contextlib.redirect_stderr(stderr_capture):
    exec(code, {'__builtins__': __builtins__})

# Extract both
stdout_output = stdout_capture.getvalue()
stderr_output = stderr_capture.getvalue()

print("STDOUT:", stdout_output)
# STDOUT: Normal output
# More output

print("STDERR:", stderr_output)
# STDERR: Error message!
```

### How Redirection Works Internally

```python
# What redirect_stdout() does (simplified):
class redirect_stdout:
    def __init__(self, new_target):
        self.new_target = new_target
        self.old_target = None
    
    def __enter__(self):
        self.old_target = sys.stdout  # Save original
        sys.stdout = self.new_target  # Replace with buffer
        return self.new_target
    
    def __exit__(self, *args):
        sys.stdout = self.old_target  # Restore original
```

**Context manager pattern:**
1. Enter: Save old stdout, set new stdout
2. Execute: Code uses new stdout
3. Exit: Restore old stdout

### Extracting Results from Executed Code

**The Big Question: How do we get results from `exec()`?**

Since `exec()` returns `None`, we have **four main strategies:**

#### Strategy 1: Require `print()` (Simplest)

```python
# Code MUST print results
code = """
result = 10 + 32
print(result)  # ← Required!
"""

capture = io.StringIO()
with contextlib.redirect_stdout(capture):
    exec(code)

output = capture.getvalue()  # "42\n"
```

**Pros:**
- ✅ Simple and explicit
- ✅ Works for any output type
- ✅ Can print multiple times
- ✅ Good for streaming/progressive output

**Cons:**
- ❌ User must remember to print
- ❌ Not "natural" for functions that return

#### Strategy 2: Inspect Namespace (Extract Variables)

```python
# Code assigns to variables (no print needed)
code = """
x = 10
y = 32
result = x + y
"""

namespace = {'__builtins__': __builtins__}
exec(code, namespace)

# Extract the 'result' variable
output = namespace.get('result')  # 42
```

**Pros:**
- ✅ No print required
- ✅ Can access multiple variables
- ✅ Natural for assignments

**Cons:**
- ❌ Need to know variable name
- ❌ Not obvious which variable is "the result"
- ❌ Need to serialize objects

#### Strategy 3: Eval Last Expression (Jupyter-style)

```python
import ast

code = """
x = 10
y = 32
x + y  # ← Last line is an expression
"""

# Parse code to AST
tree = ast.parse(code)
last_stmt = tree.body[-1]

namespace = {'__builtins__': __builtins__}

if isinstance(last_stmt, ast.Expr):  # Last line is expression
    # Execute everything except last line
    for stmt in tree.body[:-1]:
        exec(compile(ast.Module([stmt], []), '<string>', 'exec'), namespace)
    
    # Evaluate last expression
    result = eval(compile(ast.Expression(last_stmt.value), '<string>', 'eval'), namespace)
    output = str(result)  # "42"
else:
    # Normal exec
    exec(code, namespace)
```

**Pros:**
- ✅ Like Python REPL / Jupyter
- ✅ Natural for calculations
- ✅ No explicit print needed

**Cons:**
- ❌ Complex implementation
- ❌ Magic behavior
- ❌ Only works for expressions

#### Strategy 4: Hybrid (Auto-Print Result Variable)

```python
code = """
result = 10 + 32
# Can print OR just assign to 'result'
"""

namespace = {'__builtins__': __builtins__}
capture = io.StringIO()

with contextlib.redirect_stdout(capture):
    exec(code, namespace)
    
    # If no output and 'result' exists, auto-print it
    if not capture.getvalue() and 'result' in namespace:
        print(namespace['result'])

output = capture.getvalue()  # "42\n"
```

**Pros:**
- ✅ Flexible: print OR assign to 'result'
- ✅ Explicit variable name ('result')
- ✅ Falls back to manual print

**Cons:**
- ⚠️ Convention-based (must use 'result')
- ⚠️ Slightly magical

#### Strategy Comparison

| Strategy | User Code | Pros | Cons | Best For |
|----------|-----------|------|------|----------|
| **Print** | `print(result)` | Simple, explicit | Must remember | Current system ✅ |
| **Namespace** | `result = 42` | Natural | Which var? | Known variable name |
| **Eval last** | `x + y` | REPL-like | Complex | Interactive shells |
| **Hybrid** | `result = 42` or `print(...)` | Flexible | Convention | LLM-generated code |

### Complete Example: Execution with Capture

Here's how your `execution_server.py` works:

```python
import io
import sys
import contextlib
import traceback
import inspect

async def execute_code(code: str) -> dict:
    """Execute code and return results"""
    
    # STEP 1: Create capture buffers
    stdout_capture = io.StringIO()  # Catch print() output
    stderr_capture = io.StringIO()  # Catch errors/warnings
    
    try:
        # STEP 2: Setup execution namespace
        exec_namespace = {
            '__builtins__': __builtins__,  # Built-in functions
            '__name__': '__main__',        # So if __name__ == '__main__' works
            'asyncio': asyncio,            # Pre-import asyncio
        }
        
        # Remember initial keys (to find new variables later)
        initial_keys = set(exec_namespace.keys())
        
        # STEP 3: Execute with output redirection
        with contextlib.redirect_stdout(stdout_capture), \
             contextlib.redirect_stderr(stderr_capture):
            
            # Execute the code string
            exec(code, exec_namespace, exec_namespace)
            
            # STEP 4: Handle async main() if exists
            if 'main' in exec_namespace and \
               inspect.iscoroutinefunction(exec_namespace['main']):
                await exec_namespace['main']()
        
        # STEP 5: Extract captured output
        stdout_output = stdout_capture.getvalue()
        stderr_output = stderr_capture.getvalue()
        
        # STEP 6: Find user-created variables
        user_vars = {
            key: exec_namespace[key]
            for key in exec_namespace.keys()
            if key not in initial_keys and not key.startswith('_')
        }
        
        # STEP 7: Fallback - if no output but 'result' exists, use it
        if not stdout_output and 'result' in user_vars:
            stdout_output = str(user_vars['result'])
        
        # STEP 8: Return results
        return {
            "success": True,
            "output": stdout_output,
            "error": stderr_output if stderr_output else None,
            "variables": user_vars,  # Optional: return all variables
            "return_code": 0
        }
    
    except Exception as e:
        # STEP 9: Handle errors
        return {
            "success": False,
            "output": stdout_capture.getvalue(),
            "error": f"{traceback.format_exc()}\n{stderr_capture.getvalue()}",
            "return_code": -1
        }
```

### Key Insights

#### 1. Return Values from Functions are LOST

```python
code = """
def main():
    return 42  # ← This goes nowhere!

main()
"""

exec(code, namespace)
# The return value is discarded
# No way to retrieve it!
```

**Solution:** Use `print()` instead of `return` in the executed code.

#### 2. Top-Level Variables ARE Accessible

```python
code = """
x = 10
y = 20
result = x + y  # ← This IS in namespace
"""

namespace = {}
exec(code, namespace)
print(namespace['result'])  # 42 ✅
```

#### 3. Local Variables Inside Functions are NOT Accessible

```python
code = """
def calculate():
    x = 10  # ← Local to function
    y = 20  # ← Local to function
    return x + y

result = calculate()  # ← This IS accessible
"""

namespace = {}
exec(code, namespace)

print(namespace['result'])  # 42 ✅
print(namespace.get('x'))   # None ❌ (local to function)
print(namespace.get('y'))   # None ❌ (local to function)
```

### Design Recommendations

**For Your LLM-Generated Code:**

**Option A: Enforce print() (Current)**
```python
# LLM generates:
def main():
    result = mcp_call_http(...)
    print(result)  # ← Required

if __name__ == '__main__':
    main()
```

**Option B: Use result variable + auto-print**
```python
# LLM generates:
def main():
    result = mcp_call_http(...)
    # Don't need to print if we return it

if __name__ == '__main__':
    result = main()  # ← Assign to top-level 'result'

# System auto-prints if result exists and no output
```

**Option C: Hybrid (Recommended)**
```python
# System accepts either:
# 1. Code that prints
# 2. Code that assigns to 'result'
# 3. Code that does both

# Your execute_code checks:
if not stdout_output and 'result' in namespace:
    stdout_output = str(namespace['result'])
```

---

## Quick Reference

### Encoding / Decoding
```python
text.encode('utf-8')              # str → bytes
bytes_data.decode('utf-8')        # bytes → str
```

### Reading
```python
stream.read()                     # Read until EOF
stream.read(n)                    # Read exactly n bytes
stream.readline()                 # Read until \n
```

### Writing
```python
stream.write(data_bytes)          # Write bytes to buffer
await stream.drain()              # Flush buffer (send now!)
stream.flush()                    # Flush (sync version)
```

### Length Prefix Protocol
```python
# Send:
length_bytes = len(data).to_bytes(4, 'big')
stream.write(length_bytes + data)
await stream.drain()

# Receive:
length = int.from_bytes(stream.read(4), 'big')
data = stream.read(length)
```

### EOF Check
```python
data = stream.read(n)
if len(data) == 0:  # EOF!
    break
```

---

## Support

For issues or questions, check:
1. Browser console for JavaScript errors
2. Terminal output for backend errors
3. API docs at http://localhost:8000/docs

---

**Last Updated:** January 5, 2026

**Version:** 2.0

