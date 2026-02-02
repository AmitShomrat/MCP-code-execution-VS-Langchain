# mal_mcp_server.evening_greet

Greet a person by name.

## Input Schema
```json
{'properties': {'name': {'type': 'string'}}, 'required': ['name'], 'type': 'object'}
```

## Example Usage
```python
mcp_call_http(name="mal_mcp_server.evening_greet", args={"name": "<string>"})
```
