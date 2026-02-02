# db_server.query_db

Executes safe SQL queries on the database. Only SELECT queries are allowed.

## Input Schema
```json
{'$defs': {'QueryRequest': {'properties': {'query': {'type': 'string'}, 'inverse': {'default': False, 'type': 'boolean'}}, 'required': ['query'], 'type': 'object'}}, 'properties': {'request': {'$ref': '#/$defs/QueryRequest'}}, 'required': ['request'], 'type': 'object'}
```

## Example Usage
```python
mcp_call_http(name="db_server.query_db", args={"request": "<value>"})
```
