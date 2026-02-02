"""
Application Launcher for MCP Benchmark Dashboard.

This module provides an interactive launcher for the unified MCP Benchmark Dashboard
which includes both single-task and multi-task modes in one FastAPI application.
"""
import sys
import asyncio



def print_banner():
    """Print welcome banner."""
    print("=" * 80)
    print("MCP BENCHMARK SYSTEM")
    print("=" * 80)
    print()


def print_menu():
    """Print menu options."""
    print("Choose an option:")
    print()
    print("  1. 🚀 Start MCP Benchmark Dashboard")
    print("     - Unified web interface at: http://localhost:8000")
    print("     - Single Task Mode: Run individual queries")
    print("     - Multiple Tasks Mode: Run batch benchmarks")
    print("     - Real-time comparison charts and analytics")
    print("     - API documentation at: http://localhost:8000/docs")
    print("     - MCP Gateway at: http://localhost:8080")
    print()
    print("  2. ❌ Exit")
    print()


def start_dashboard():
    """Start the unified FastAPI Dashboard (Main + Gateway with single/multiple task modes)."""
    print("\n" + "=" * 80)
    print("Starting MCP Benchmark Dashboard...")
    print("Dashboard: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("MCP Gateway: http://localhost:8080")
    print("Gateway Docs: http://localhost:8080/docs")
    print("\nFeatures:")
    print("  • Single Task Mode - Run individual queries")
    print("  • Multiple Tasks Mode - Run batch benchmarks")
    print("  • Real-time comparison charts")
    print("Press Ctrl+C to stop")
    print("=" * 80 + "\n")
    
    # Import and run the existing main.py logic (already uses shared MCP client)
    try:
        import main
        asyncio.run(main.main())
    except KeyboardInterrupt:
        print("\n\nDashboard stopped")


def main():
    """Main launcher function."""
    while True:
        print_banner()
        print_menu()
        
        try:
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == "1":
                start_dashboard()
                break
            elif choice == "2":
                print("\nGoodbye! 👋\n")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice. Please enter 1 or 2.\n")
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

