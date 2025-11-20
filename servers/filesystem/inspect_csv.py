"""
Smart CSV Inspection Tool

Uses pandas to analyze CSV structure and return top 5 rows with column information.
"""

from app.core.mcp_client import get_mcp_client
import pandas as pd
from io import StringIO


async def inspect_csv(path: str) -> str:
    """
    Inspect CSV file structure using pandas.
    
    Returns:
    - Top 5 rows
    - Column datatypes
    - Distinct count for object/string columns
    
    Args:
        path: Path to CSV file (e.g., "Sales_Records.csv")
        
    Returns:
        Formatted analysis string with structure and top 5 rows
        
    Example:
        structure = await inspect_csv("Sales_Records.csv")
        print(structure)
    """
    # Get singleton MCP client instance
    mcp_client = get_mcp_client()
    
    # Call official MCP filesystem server to read file
    result = await mcp_client.call_tool(
        server_name="filesystem",
        tool_name="read_file",
        arguments={"path": path}
    )
    
    # Extract file content and load into pandas
    content = result.content[0].text
    df = pd.read_csv(StringIO(content))
    
    # Handle empty file case
    if df.empty:
        return f"CSV file {path} is empty"
    
    # Build output with clear formatting for LLM
    output = [
        f"CSV File: {path}",
        "=" * 80,
        f"Total Rows: {len(df)}",
        f"Total Columns: {len(df.columns)}",
        "",
        "=" * 80,
        "COLUMN INFORMATION",
        "=" * 80
    ]
    
    # Analyze each column with clear formatting
    for idx, col in enumerate(df.columns, 1):
        dtype = str(df[col].dtype)
        output.append(f"\nColumn {idx}: {col}")
        output.append(f"  └─ Datatype: {dtype}")
        
        # For object/string columns, show distinct count
        if df[col].dtype == 'object':
            distinct_count = df[col].nunique()
            output.append(f"  └─ Distinct Values: {distinct_count}")
    
    # Show top 5 rows
    output.append("\n" + "=" * 80)
    output.append("FIRST 5 ROWS")
    output.append("=" * 80)
    output.append(df.head(5).to_string())
    
    return '\n'.join(output)

