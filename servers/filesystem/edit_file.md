# filesystem.edit_file

Make line-based edits to a text file. Each edit replaces exact line sequences with new content. Returns a git-style diff showing the changes made. Only works within allowed directories.

## Input Schema
```json
{'$schema': 'http://json-schema.org/draft-07/schema#', 'type': 'object', 'properties': {'path': {'type': 'string'}, 'edits': {'type': 'array', 'items': {'type': 'object', 'properties': {'oldText': {'description': 'Text to search for - must match exactly', 'type': 'string'}, 'newText': {'description': 'Text to replace with', 'type': 'string'}}, 'required': ['oldText', 'newText']}}, 'dryRun': {'description': 'Preview changes using git-style diff format', 'default': False, 'type': 'boolean'}}, 'required': ['path', 'edits']}
```

## Example Usage
```python
mcp_call_http(name="filesystem.edit_file", args={"path": "<string>", "edits": [], "dryRun": False})
```
