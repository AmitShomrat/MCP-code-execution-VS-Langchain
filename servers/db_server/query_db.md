# db_server.query_db

Executes safe SQL queries on the database. Only SELECT queries are allowed. 
            IMPORTANT: You have to understand data base schemas and tables to generate correct queeries.

## Input Schema
```json
{'properties': {'query': {'type': 'string'}}, 'required': ['query'], 'type': 'object'}
```

## Example Usage
```python
mcp_call_http(name="db_server.query_db", args={"query": "<string>"})
```
