# db_server.add_user_record

Adds a user record to the database with proper validation and security checks

## Input Schema
```json
{
  "$defs": {
    "User": {
      "properties": {
        "name": {
          "type": "string"
        },
        "role": {
          "type": "string"
        },
        "pass_key": {
          "type": "string"
        }
      },
      "required": [
        "name",
        "role",
        "pass_key"
      ],
      "type": "object"
    }
  },
  "properties": {
    "user": {
      "$ref": "#/$defs/User"
    }
  },
  "required": [
    "user"
  ],
  "type": "object"
}
```

## Example Usage
```python
mcp_call_http(name="db_server.add_user_record", args={"user": "<value>"})
```
