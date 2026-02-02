# filesystem.read_file

Read the complete contents of a file as text. DEPRECATED: Use read_text_file instead.

## Input Schema
```json
{'$schema': 'http://json-schema.org/draft-07/schema#', 'type': 'object', 'properties': {'path': {'type': 'string'}, 'tail': {'description': 'If provided, returns only the last N lines of the file', 'type': 'number'}, 'head': {'description': 'If provided, returns only the first N lines of the file', 'type': 'number'}}, 'required': ['path']}
```

## Example Usage
```python
mcp_call_http(name="filesystem.read_file", args={"path": "<string>", "tail": 0.0, "head": 0.0})
```
