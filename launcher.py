"""
Application Launcher - Choose between UIs.

This module provides an interactive launcher to choose between:
1. Streamlit Benchmark UI - For running and comparing benchmarks
2. Single Query API UI - For running individual queries via API
"""
import sys
import subprocess
import multiprocessing
import uvicorn
import asyncio



def print_banner():
    """Print welcome banner."""
    print("=" * 80)
    print("MCP BENCHMARK SYSTEM")
    print("=" * 80)
    print()


def print_menu():
    """Print menu options."""
    print("Choose an interface:")
    print()
    print("  1. 📊 Streamlit Benchmark UI")
    print("     - Run multiple benchmark tasks")
    print("     - Compare Code Execution MCP vs Traditional MCP")
    print("     - Interactive visualizations and reports")
    print("     - Access at: http://localhost:8501")
    print()
    print("  2. 🚀 Single Query API UI")
    print("     - Run individual queries via REST API")
    print("     - Main API at: http://localhost:8000")
    print("     - API documentation at: http://localhost:8000/docs")
    print("     - MCP Gateway at: http://localhost:8080")
    print()
    print("  3. ❌ Exit")
    print()


async def start_gateway_server(host='localhost', port=8080):
    """
    Start the MCP Gateway server.
    
    Configuration:
    - Host: 0.0.0.0 (accessible from network)
    - Port: 8080
    - Reload: False (disabled for multiprocessing)
    - Log level: info
    """
    config = uvicorn.Config(
        "docker_code.mcp_gateway_server:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

def run_streamlit():
    """Run Streamlit benchmark UI."""
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "app/streamlit_benchmark/ui.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
    ])

async def start_streamlit_with_gateway():
    """Start Streamlit benchmark UI with MCP Gateway."""
    from app.core import get_mcp_client
    print("\n" + "=" * 80)
    print("Starting Streamlit Benchmark UI with MCP Gateway...")
    print("MCP Gateway: http://localhost:8080")
    print("Streamlit UI: http://localhost:8501")
    print("Press Ctrl+C to stop")
    print("=" * 80 + "\n")
    
    print("Initializing MCP client...")
    _mcp_client = await get_mcp_client()
    
    # Start gateway in async task
    gateway_task = asyncio.create_task(start_gateway_server(host='localhost', port=8080))

    await asyncio.sleep(2)


    # Start gateway server in background process
    from multiprocessing import Process
    
    streamlit_process = Process(target=run_streamlit, name="StreamlitUI")
    streamlit_process.start()

    try:
        await gateway_task
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
    finally:
        gateway_task.cancel()
        streamlit_process.terminate()
        streamlit_process.join()
        await _mcp_client.close()
        print("Streamlit UI and Gateway stopped")

def start_streamlit_ui():
    """Start the Streamlit benchmark UI."""
    asyncio.run(start_streamlit_with_gateway())

def start_api_ui():
    """Start the FastAPI servers (Main + Gateway)."""
    print("\n" + "=" * 80)
    print("Starting FastAPI Servers...")
    print("Main API: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("MCP Gateway: http://localhost:8085")
    print("Gateway Docs: http://localhost:8085/docs")
    print("Press Ctrl+C to stop")
    print("=" * 80 + "\n")
    
    # Import and run the existing main.py logic
    try:
        import main
        import asyncio
        asyncio.run(main.main())
    except KeyboardInterrupt:
        print("\n\nAPI servers stopped")


def main():
    """Main launcher function."""
    # Required for multiprocessing on Windows and macOS
    multiprocessing.set_start_method('spawn', force=True)
    
    while True:
        print_banner()
        print_menu()
        
        try:
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                start_streamlit_ui()
                break
            elif choice == "2":
                start_api_ui()
                break
            elif choice == "3":
                print("\nGoodbye! 👋\n")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice. Please enter 1, 2, or 3.\n")
                input("Press Enter to continue...")
                print("\n" * 2)
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()

