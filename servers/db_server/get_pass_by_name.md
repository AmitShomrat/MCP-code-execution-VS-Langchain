# db_server.get_pass_by_name

get the passkey of a user by their name

## Input Schema
```json
{
  "properties": {
    "name": {
      "type": "string"
    }
  },
  "required": [
    "name"
  ],
  "type": "object"
}
```

## Example Usage
```python
mcp_call_http(name="db_server.get_pass_by_name", args={"name": "<string>"})
```
