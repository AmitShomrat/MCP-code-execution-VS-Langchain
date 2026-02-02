# db_server.grant_door_access

Grants door access to a user by adding their passkey to the door's allowed passkeys. Validates user and door exist.

## Input Schema
```json
{'$defs': {'Door': {'properties': {'code': {'type': 'string'}, 'description': {'type': 'string'}}, 'required': ['code', 'description'], 'type': 'object'}, 'User': {'properties': {'name': {'type': 'string'}, 'role': {'type': 'string'}, 'pass_key': {'type': 'string'}}, 'required': ['name', 'role', 'pass_key'], 'type': 'object'}}, 'properties': {'user': {'$ref': '#/$defs/User'}, 'door': {'$ref': '#/$defs/Door'}}, 'required': ['user', 'door'], 'type': 'object'}
```

## Example Usage
```python
mcp_call_http(name="db_server.grant_door_access", args={"user": "<value>", "door": "<value>"})
```
