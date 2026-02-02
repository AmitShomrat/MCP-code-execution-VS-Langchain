# Tools Client

A modular Python client for the Tools Bridge API. Each tool has its own dedicated module for easy maintenance and usage.

## Structure

```
tools_client/
├── __init__.py              # Main package with all exports
├── _request.py              # Shared HTTP request helper
├── health_check.py          # Health check tool
├── list_available_tools.py  # List available tools
├── list_directory.py        # List directory contents
├── inspect_csv.py           # Inspect CSV files
├── read_file.py             # Read file contents
├── write_file.py            # Write file contents
├── example.py               # Usage examples
└── README.md                # This file
```

## Installation

No external dependencies required beyond `requests`:

```bash
pip install requests
```

## Usage

### Import all tools

```python
from tools_client import (
    health_check,
    list_available_tools,
    list_directory,
    inspect_csv,
    read_file,
    write_file
)
```

### Or import individual tools

```python
from tools_client import read_file, write_file

# Read a file
response = read_file("/data/config.txt")
if response['success']:
    print(response['result'])

# Write a file
response = write_file("/data/output.txt", "Hello World!")
```

## Available Tools

### health_check()
Check if the API is healthy and running.

```python
health = health_check()
print(health['status'])  # 'healthy'
```

### list_available_tools()
Get list of all available tools.

```python
tools = list_available_tools()
for tool in tools['tools']:
    print(f"{tool['name']}: {tool['description']}")
```

### list_directory(path)
List files and directories at a path.

```python
response = list_directory("/data")
if response['success']:
    for item in response['result']:
        print(item)
```

### inspect_csv(path)
Inspect a CSV file structure.

```python
response = inspect_csv("/data/sales.csv")
if response['success']:
    print(f"Columns: {response['result']['columns']}")
    print(f"Rows: {response['result']['row_count']}")
```

### read_file(path)
Read file contents.

```python
response = read_file("/data/config.txt")
if response['success']:
    print(response['result'])
```

### write_file(path, content)
Write content to a file.

```python
response = write_file("/data/output.txt", "Hello World!")
if response['success']:
    print("File written successfully!")
```

## Configuration

All tools accept optional `base_url` and `timeout` parameters:

```python
# Custom API endpoint
response = list_directory("/data", base_url="http://192.168.1.100:8080")

# Custom timeout
response = read_file("/large-file.txt", timeout=60)

# Both
response = write_file(
    "/data/output.txt",
    "content",
    base_url="http://custom-api:8080",
    timeout=45
)
```

Default values:
- `base_url`: `"http://localhost:8080"`
- `timeout`: `30` seconds

## Response Format

All tools return a dictionary with the following structure:

```python
{
    "success": bool,      # True if operation succeeded
    "result": Any,        # Result data (varies by tool)
    "message": str        # Success or error message
}
```

## Examples

Run the included examples:

```bash
python -m tools_client.example
```

Or see `example.py` for more usage patterns.

## Error Handling

```python
try:
    response = read_file("/some/file.txt")
    if response['success']:
        print(response['result'])
    else:
        print(f"Error: {response['message']}")
except Exception as e:
    print(f"Request failed: {e}")
```

