"""
Example usage of the tools_client package.
"""
from tools_client import (
    health_check,
    list_available_tools,
    list_directory,
    inspect_csv,
    read_file,
    write_file
)


def main():
    """Run examples of all available tools."""
    print("=== Tools Client Examples ===\n")
    
    try:
        # Example 1: Check API health
        print("1. Checking API health...")
        health = health_check()
        print(f"   Status: {health['status']}")
        print(f"   Version: {health['version']}\n")
        
        # Example 2: List available tools
        print("2. Listing available tools...")
        tools = list_available_tools()
        print(f"   Available tools: {len(tools['tools'])}")
        for tool in tools['tools']:
            print(f"   - {tool['name']}: {tool['description']}")
        print()
        
        # Example 3: List directory
        print("3. Listing directory '/'...")
        response = list_directory("/")
        if response['success']:
            print(f"   ✓ {response['message']}")
            items = response['result']
            if isinstance(items, list):
                print(f"   Items found: {len(items)}")
        else:
            print(f"   ✗ Failed: {response['message']}")
        print()
        
        # Example 4: Read a file
        print("4. Reading file '/etc/hostname'...")
        response = read_file("/etc/hostname")
        if response['success']:
            print(f"   ✓ Content: {response['result']}")
        else:
            print(f"   ✗ Failed: {response['message']}")
        print()
        
        # Example 5: Write a file
        print("5. Writing to file '/tmp/test_output.txt'...")
        response = write_file("/tmp/test_output.txt", "Hello from tools_client!")
        if response['success']:
            print(f"   ✓ {response['message']}")
        else:
            print(f"   ✗ Failed: {response['message']}")
        print()
        
        # Example 6: Inspect CSV (if available)
        print("6. Inspecting CSV file '/data/Sales_Records.csv'...")
        response = inspect_csv("/data/Sales_Records.csv")
        if response['success']:
            print(f"   ✓ {response['message']}")
            result = response['result']
            if isinstance(result, dict):
                print(f"   Columns: {result.get('columns', [])}")
                print(f"   Row count: {result.get('row_count', 0)}")
        else:
            print(f"   ✗ Failed: {response['message']}")
        print()
            
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
    
    print("=== Done ===")


if __name__ == "__main__":
    main()

