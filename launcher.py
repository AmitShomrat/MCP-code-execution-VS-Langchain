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


def start_gateway_server():
    """
    Start the MCP Gateway server.
    
    Configuration:
    - Host: 0.0.0.0 (accessible from network)
    - Port: 8080
    - Reload: False (disabled for multiprocessing)
    - Log level: info
    """
    uvicorn.run(
        "docker_code.mcp_gateway_server:app",
        host="localhost",
        port=8080,
        reload=False,
        log_level="info"
    )


def start_streamlit_ui():
    """Start Streamlit benchmark UI with MCP Gateway."""
    print("\n" + "=" * 80)
    print("Starting Streamlit Benchmark UI with MCP Gateway...")
    print("MCP Gateway: http://localhost:8080")
    print("Streamlit UI: http://localhost:8501")
    print("Press Ctrl+C to stop")
    print("=" * 80 + "\n")
    
    # Start gateway server in background process
    from multiprocessing import Process
    
    gateway_process = Process(target=start_gateway_server, name="GatewayServer")
    gateway_process.start()
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "app/streamlit_benchmark/ui.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ])

        # sys.executable is the absolute path of python interpreter
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
    finally:
        gateway_process.terminate()
        gateway_process.join()
        print("Streamlit UI and Gateway stopped")


def start_api_ui():
    """Start the FastAPI servers (Main + Gateway)."""
    print("\n" + "=" * 80)
    print("Starting FastAPI Servers...")
    print("Main API: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("MCP Gateway: http://localhost:8080")
    print("Gateway Docs: http://localhost:8080/docs")
    print("Press Ctrl+C to stop")
    print("=" * 80 + "\n")
    
    # Import and run the existing main.py logic
    try:
        import main
        main.main()
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

