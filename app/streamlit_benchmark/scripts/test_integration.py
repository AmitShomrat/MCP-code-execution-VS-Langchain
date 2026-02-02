"""
Test script to verify the benchmark system integration.

This script validates:
1. Task loading from JSON
2. Benchmark runner initialization
3. Component imports
4. File structure
"""
import sys
import os
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def print_test(test_name, status, message=""):
    """Print test result."""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {test_name}")
    if message:
        print(f"   {message}")


def test_file_structure():
    """Test that all required files exist."""
    print("\n" + "=" * 60)
    print("Testing File Structure")
    print("=" * 60)
    
    base_dir = project_root / "app" / "streamlit_benchmark"
    
    required_files = [
        base_dir / "__init__.py",
        base_dir / "ui.py",
        base_dir / "benchmark_tasks.json",
        base_dir / "README.md",
        base_dir / "scripts" / "start_ui.sh",
        base_dir / "scripts" / "test_integration.py",
        project_root / "launcher.py",
        project_root / "app" / "benchmarks" / "benchmark_runner.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        exists = file_path.exists()
        relative_path = file_path.relative_to(project_root)
        print_test(f"File exists: {relative_path}", exists)
        if not exists:
            all_exist = False
    
    return all_exist


def test_task_loading():
    """Test loading tasks from JSON."""
    print("\n" + "=" * 60)
    print("Testing Task Loading")
    print("=" * 60)
    
    task_file = project_root / "app" / "streamlit_benchmark" / "benchmark_tasks.json"
    
    try:
        with open(task_file, "r") as f:
            tasks = json.load(f)
        
        print_test("Load benchmark_tasks.json", True, f"Loaded {len(tasks)} tasks")
        
        # Validate task structure
        valid = True
        for task in tasks:
            required_fields = ["task_id", "user_query", "expected_behaviour", "expected_output"]
            for field in required_fields:
                if field not in task:
                    print_test(f"Task {task.get('task_id', '?')} has field '{field}'", False)
                    valid = False
        
        if valid:
            print_test("All tasks have required fields", True)
        
        return True
    except Exception as e:
        print_test("Load benchmark_tasks.json", False, str(e))
        return False


def test_imports():
    """Test that all modules can be imported."""
    print("\n" + "=" * 60)
    print("Testing Module Imports")
    print("=" * 60)
    
    imports_ok = True
    
    # Test benchmark runner import
    try:
        from app.benchmarks import BenchmarkRunner
        print_test("Import BenchmarkRunner", True)
    except Exception as e:
        print_test("Import BenchmarkRunner", False, str(e))
        imports_ok = False
    
    # Test code execution benchmark import
    try:
        from app.benchmarks import CodeExecutionBenchmark
        print_test("Import CodeExecutionBenchmark", True)
    except Exception as e:
        print_test("Import CodeExecutionBenchmark", False, str(e))
        imports_ok = False
    
    # Test traditional benchmark import
    try:
        from app.benchmarks import TraditionalMCPBenchmark
        print_test("Import TraditionalMCPBenchmark", True)
    except Exception as e:
        print_test("Import TraditionalMCPBenchmark", False, str(e))
        imports_ok = False
    
    return imports_ok


def test_benchmark_runner_methods():
    """Test that BenchmarkRunner has required methods."""
    print("\n" + "=" * 60)
    print("Testing BenchmarkRunner Methods")
    print("=" * 60)
    
    try:
        from app.benchmarks import BenchmarkRunner
        
        runner = BenchmarkRunner()
        
        required_methods = [
            "initialize_async",
            "run_task_on_both_benchmarks",
            "run_all_tasks",
            "load_tasks_from_file",
            "save_results",
            "cleanup_async"
        ]
        
        all_exist = True
        for method_name in required_methods:
            exists = hasattr(runner, method_name)
            print_test(f"Method: {method_name}", exists)
            if not exists:
                all_exist = False
        
        return all_exist
    except Exception as e:
        print_test("Create BenchmarkRunner instance", False, str(e))
        return False


def test_dependencies():
    """Test that required dependencies are installed."""
    print("\n" + "=" * 60)
    print("Testing Dependencies")
    print("=" * 60)
    
    dependencies = [
        "streamlit",
        "plotly",
        "pandas",
        "fastapi",
        "uvicorn"
    ]
    
    all_installed = True
    for dep in dependencies:
        try:
            __import__(dep)
            print_test(f"Dependency: {dep}", True)
        except ImportError:
            print_test(f"Dependency: {dep}", False, "Not installed")
            all_installed = False
    
    return all_installed


def test_task_file_structure():
    """Test that task JSON has proper structure."""
    print("\n" + "=" * 60)
    print("Testing Task File Structure")
    print("=" * 60)
    
    task_file = project_root / "app" / "streamlit_benchmark" / "benchmark_tasks.json"
    
    try:
        with open(task_file, "r") as f:
            tasks = json.load(f)
        
        if not isinstance(tasks, list):
            print_test("Tasks is a list", False, "Expected list, got " + type(tasks).__name__)
            return False
        
        print_test("Tasks is a list", True)
        
        if len(tasks) == 0:
            print_test("Tasks list not empty", False, "No tasks found")
            return False
        
        print_test("Tasks list not empty", True, f"{len(tasks)} tasks found")
        
        # Check first task structure
        first_task = tasks[0]
        print_test("First task has task_id", "task_id" in first_task)
        print_test("First task has user_query", "user_query" in first_task)
        print_test("First task has expected_behaviour", "expected_behaviour" in first_task)
        print_test("First task has expected_output", "expected_output" in first_task)
        
        return True
    except Exception as e:
        print_test("Parse task file", False, str(e))
        return False


def main():
    """Run all tests."""
    print("\n")
    print("=" * 60)
    print("MCP BENCHMARK SYSTEM - INTEGRATION TEST")
    print("=" * 60)
    
    results = {
        "File Structure": test_file_structure(),
        "Task Loading": test_task_loading(),
        "Module Imports": test_imports(),
        "BenchmarkRunner Methods": test_benchmark_runner_methods(),
        "Dependencies": test_dependencies(),
        "Task File Structure": test_task_file_structure(),
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} test suites passed")
    print("=" * 60 + "\n")
    
    if passed == total:
        print("🎉 All tests passed! The benchmark system is ready to use.")
        print("\nNext steps:")
        print("1. Run: python launcher.py")
        print("2. Choose option 1 for Streamlit UI or option 2 for API UI")
        print("3. Or run directly: streamlit run app/streamlit_benchmark/ui.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        print("\nTroubleshooting:")
        print("- Install missing dependencies: pip install streamlit plotly")
        print("- Or use uv: uv pip install streamlit plotly")
        return 1


if __name__ == "__main__":
    sys.exit(main())

