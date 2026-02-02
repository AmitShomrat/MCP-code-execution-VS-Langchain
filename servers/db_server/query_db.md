# db_server.query_db

Executes SQL queries on the database

## Input Schema
```json
{'properties': {'query': {'type': 'string'}}, 'required': ['query'], 'type': 'object'}
```

## Example Usage
```python
mcp_call_http(name="db_server.query_db", args={"query": "<string>"})
```
