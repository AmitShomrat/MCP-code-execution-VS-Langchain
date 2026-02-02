"""
Streamlit Benchmark UI for MCP Approaches Comparison.

This module provides an interactive UI for running and visualizing
benchmark comparisons between Code Execution MCP and Traditional MCP approaches.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import asyncio
import os
import atexit
from datetime import datetime

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.benchmarks.benchmark_runner import BenchmarkRunner
from app.app_logging.logger import setup_logger

logger = setup_logger(__name__)


# Global cleanup function
def cleanup_on_exit():
    """Cleanup function called when Streamlit app exits."""
    if 'benchmark_runner' in st.session_state and st.session_state.benchmark_runner is not None:
        logger.info("Streamlit app shutting down - cleaning up resources...")
        try:
            runner = st.session_state.benchmark_runner
            st.session_state.event_loop.run_until_complete(runner.cleanup_async())
            st.session_state.event_loop.close()
            logger.info("Cleanup completed successfully")
            print("UI Cleanup completed successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")


# Register cleanup handler
atexit.register(cleanup_on_exit)


# Page configuration - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="MCP Benchmark Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .stMetric label {
        color: #1f1f1f !important;
        font-weight: 600 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #0e1117 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #1f1f1f !important;
        font-weight: 600 !important;
    }
    .diff-metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        margin: 10px 0;
    }
    .diff-metric-label {
        color: #ffffff;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .diff-metric-value {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.8),
                     0 0 40px rgba(255, 255, 255, 0.4);
        margin: 0;
        line-height: 1;
    }
    .diff-metric-positive {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .diff-metric-negative {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .diff-metric-neutral {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .centered-icon {
        text-align: center;
        font-size: 32px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize BenchmarkRunner on app startup (stored in session state)
def ensure_runner_initialized():
    """Ensure the benchmark runner is initialized with Docker and MCP connections."""
    
    if "event_loop" not in st.session_state:
        st.session_state.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(st.session_state.event_loop)
    
    # Initialize session state keys if not present
    if 'benchmark_runner' not in st.session_state:
        st.session_state.benchmark_runner = None
    
    if 'initialization_attempted' not in st.session_state:
        st.session_state.initialization_attempted = False
    
    # Only initialize once
    if st.session_state.benchmark_runner is None and not st.session_state.initialization_attempted:
        st.session_state.initialization_attempted = True
        
        # Debug: Print to console as well
        print("=" * 80)
        print("Streamlit Benchmark UI Starting Up")
        print("=" * 80)
        logger.info("=" * 80)
        logger.info("Streamlit Benchmark UI Starting Up")
        logger.info("=" * 80)
        
        with st.spinner("🚀 Starting Docker and MCP servers..."):
            try:
                runner = BenchmarkRunner()
                st.session_state.event_loop.run_until_complete(runner.initialize_async())
                st.session_state.benchmark_runner = runner
            except Exception as e:
                st.error(f"❌ Failed to initialize benchmark system: {str(e)}")
                logger.error(f"Initialization error: {str(e)}")
                st.stop()
    
    return st.session_state.benchmark_runner


# Initialization is now called inside main() function


def load_tasks_from_file(file_path: str):
    """Load tasks from JSON file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []


def save_results(results, output_dir=None):
    """Save results to JSON file with timestamp."""
    if output_dir is None:
        # Save in app/streamlit_benchmark/benchmark_results/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(current_dir, "benchmark_results")
    
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"results_{timestamp}.json")
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    return output_path


def create_comparison_dataframe(results):
    """Create a DataFrame from benchmark results for visualization."""
    data = []
    for result in results:
        if "comparison" in result:
            comp = result["comparison"]
            data.append({
                "Task ID": result["task_id"],
                "Query": result["user_query"][:50] + "..." if len(result["user_query"]) > 50 else result["user_query"],
                "CE Success": "✅" if comp["code_exec_success"] else "❌",
                "Trad Success": "✅" if comp["traditional_success"] else "❌",
                "CE Time (s)": comp["code_exec_time"],
                "Trad Time (s)": comp["traditional_time"],
                "CE LLM Calls": comp["code_exec_llm_calls"],
                "Trad LLM Calls": comp["traditional_llm_calls"],
                "CE Tokens": comp["code_exec_total_tokens"],
                "Trad Tokens": comp["traditional_total_tokens"],
                "Time Diff (s)": comp["time_diff"],
                "LLM Calls Diff": comp["llm_calls_diff"],
                "Tokens Diff": comp["tokens_diff"]
            })
    
    return pd.DataFrame(data)


def plot_time_comparison(df):
    """Create time comparison bar chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Code Execution MCP',
        x=df['Task ID'],
        y=df['CE Time (s)'],
        marker_color='#3366CC'
    ))
    
    fig.add_trace(go.Bar(
        name='Traditional MCP',
        x=df['Task ID'],
        y=df['Trad Time (s)'],
        marker_color='#DC3912'
    ))
    
    fig.update_layout(
        title='Execution Time Comparison',
        xaxis_title='Task ID',
        yaxis_title='Time (seconds)',
        barmode='group',
        height=400
    )
    
    return fig


def plot_llm_calls_comparison(df):
    """Create LLM calls comparison bar chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Code Execution MCP',
        x=df['Task ID'],
        y=df['CE LLM Calls'],
        marker_color='#109618'
    ))
    
    fig.add_trace(go.Bar(
        name='Traditional MCP',
        x=df['Task ID'],
        y=df['Trad LLM Calls'],
        marker_color='#FF9900'
    ))
    
    fig.update_layout(
        title='LLM Calls Comparison',
        xaxis_title='Task ID',
        yaxis_title='Number of LLM Calls',
        barmode='group',
        height=400
    )
    
    return fig


def plot_tokens_comparison(df):
    """Create tokens comparison bar chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Code Execution MCP',
        x=df['Task ID'],
        y=df['CE Tokens'],
        marker_color='#990099'
    ))
    
    fig.add_trace(go.Bar(
        name='Traditional MCP',
        x=df['Task ID'],
        y=df['Trad Tokens'],
        marker_color='#0099C6'
    ))
    
    fig.update_layout(
        title='Token Usage Comparison',
        xaxis_title='Task ID',
        yaxis_title='Total Tokens',
        barmode='group',
        height=400
    )
    
    return fig


def plot_aggregate_metrics(results):
    """Create aggregate metrics visualization."""
    if not results or not any("comparison" in r for r in results):
        return None
    
    # Calculate aggregates
    total_ce_time = sum(r["comparison"]["code_exec_time"] for r in results if "comparison" in r)
    total_trad_time = sum(r["comparison"]["traditional_time"] for r in results if "comparison" in r)
    total_ce_calls = sum(r["comparison"]["code_exec_llm_calls"] for r in results if "comparison" in r)
    total_trad_calls = sum(r["comparison"]["traditional_llm_calls"] for r in results if "comparison" in r)
    total_ce_tokens = sum(r["comparison"]["code_exec_total_tokens"] for r in results if "comparison" in r)
    total_trad_tokens = sum(r["comparison"]["traditional_total_tokens"] for r in results if "comparison" in r)
    
    # Create subplots
    fig = go.Figure()
    
    categories = ['Time (s)', 'LLM Calls', 'Tokens']
    ce_values = [total_ce_time, total_ce_calls, total_ce_tokens]
    trad_values = [total_trad_time, total_trad_calls, total_trad_tokens]
    
    fig.add_trace(go.Bar(
        name='Code Execution MCP',
        x=categories,
        y=ce_values,
        marker_color='#3366CC',
        text=ce_values,
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Traditional MCP',
        x=categories,
        y=trad_values,
        marker_color='#DC3912',
        text=trad_values,
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Aggregate Metrics Comparison',
        barmode='group',
        height=400,
        yaxis_title='Total Count'
    )
    
    return fig


def display_task_details(result):
    """Display detailed results for a single task."""
    st.markdown(f"### Task {result['task_id']}: {result['user_query']}")
    
    # Expected behavior and output
    with st.expander("📋 Expected Behavior & Output", expanded=False):
        st.markdown(f"**Expected Behavior:** {result.get('expected_behaviour', 'N/A')}")
        st.markdown(f"**Expected Output:** {result.get('expected_output', 'N/A')}")
    
    if "comparison" not in result:
        st.error("No comparison data available for this task")
        return
    
    comp = result["comparison"]
    
    # Comparison metrics with enhanced styling
    col1, col2, col3 = st.columns(3)
    
    # Determine CSS classes based on differences (negative is better for Code Execution)
    time_class = "diff-metric-negative" if comp['time_diff'] < 0 else "diff-metric-positive" if comp['time_diff'] > 0 else "diff-metric-neutral"
    calls_class = "diff-metric-negative" if comp['llm_calls_diff'] < 0 else "diff-metric-positive" if comp['llm_calls_diff'] > 0 else "diff-metric-neutral"
    tokens_class = "diff-metric-negative" if comp['tokens_diff'] < 0 else "diff-metric-positive" if comp['tokens_diff'] > 0 else "diff-metric-neutral"
    
    with col1:
        st.markdown(f"""
            <div class="diff-metric-box {time_class}">
                <div class="diff-metric-label">Time Difference</div>
                <div class="diff-metric-value">{comp['time_diff']:.2f}s</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="diff-metric-box {calls_class}">
                <div class="diff-metric-label">LLM Calls Diff</div>
                <div class="diff-metric-value">{comp['llm_calls_diff']:+d}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="diff-metric-box {tokens_class}">
                <div class="diff-metric-label">Tokens Diff</div>
                <div class="diff-metric-value">{comp['tokens_diff']:+d}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Code Execution MCP Results
    with st.expander("🚀 Code Execution MCP Results", expanded=True):
        ce_result = result.get("code_execution_mcp", {})
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status = "✅ Success" if ce_result.get("success") else "❌ Failed"
            st.markdown(f"**Status:** {status}")
        with col2:
            st.markdown(f"**Time:** {ce_result.get('time', 0):.2f}s")
        with col3:
            st.markdown(f"**LLM Calls:** {len(ce_result.get('llm_calls', []))}")
        with col4:
            st.markdown(f"**Total Tokens:** {ce_result.get('tokens', {}).get('total_tokens', 0)}")
        
        st.markdown("**Output:**")
        st.code(ce_result.get("output", "No output"), language="text")
        
        if ce_result.get("error") is not None:
            st.error(f"Error: {ce_result['error']}")
    
    # Traditional MCP Results
    with st.expander("🔧 Traditional MCP Results", expanded=True):
        trad_result = result.get("traditional_mcp", {})
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status = "✅ Success" if trad_result.get("success") else "❌ Failed"
            st.markdown(f"**Status:** {status}")
        with col2:
            st.markdown(f"**Time:** {trad_result.get('time', 0):.2f}s")
        with col3:
            st.markdown(f"**LLM Calls:** {len(trad_result.get('llm_calls', []))}")
        with col4:
            st.markdown(f"**Total Tokens:** {trad_result.get('tokens', {}).get('total_tokens', 0)}")
        
        st.markdown("**Output:**")
        st.code(trad_result.get("output", "No output"), language="text")
        
        if trad_result.get("error") is not None:
            st.error(f"Error: {trad_result['error']}")
    
    st.markdown("---")


def main():
    """Main Streamlit application."""
    # Initialize benchmark runner on first load
    ensure_runner_initialized()
    
    st.title("📊 MCP Benchmark Dashboard")
    st.markdown("Compare **Code Execution MCP** vs **Traditional MCP** approaches")
    
    # Sidebar
    with st.sidebar:
        # Configuration section icon
        st.markdown('<div class="centered-icon">⚙️</div>', unsafe_allow_html=True)
        
        # Max turns configuration
        max_turns = st.number_input(
            "Max LLM Turns:",
            min_value=1,
            max_value=10,
            value=3,
            help="Maximum number of LLM turns for code execution approach"
        )
        
        st.markdown("---")
        
        # Tasks section icon
        st.markdown('<div class="centered-icon">📂</div>', unsafe_allow_html=True)
        
        # Option 1: Load default tasks
        if st.button("📋 Load Default Tasks", type="secondary", use_container_width=True):
            default_path = "app/streamlit_benchmark/benchmark_tasks.json"
            tasks = load_tasks_from_file(default_path)
            if tasks:
                st.session_state.tasks = tasks
                st.session_state.tasks_source = default_path
                st.success(f"✅ Loaded {len(tasks)} tasks from default file")
            else:
                st.error("❌ Default tasks file not found")
        
        # Option 2: Upload custom file
        uploaded_file = st.file_uploader(
            "Or upload a custom tasks JSON file:",
            type=['json'],
            help="Upload a JSON file containing benchmark tasks"
        )
        
        if uploaded_file is not None:
            try:
                tasks = json.load(uploaded_file)
                if tasks:
                    st.session_state.tasks = tasks
                    st.session_state.tasks_source = uploaded_file.name
                    st.success(f"✅ Loaded {len(tasks)} tasks from {uploaded_file.name}")
                else:
                    st.error("❌ No tasks found in uploaded file")
            except json.JSONDecodeError:
                st.error("❌ Invalid JSON file")
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
        
        # Add spacing before Run button
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Run benchmarks button - centered
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        with col2:
            run_button = st.button("🚀 Run Benchmarks", type="primary", disabled="tasks" not in st.session_state, use_container_width=True)
        
        if run_button:
            with st.spinner("Running benchmarks... This may take several minutes..."):
                # Use the pre-initialized runner from session state
                runner = st.session_state.benchmark_runner
                
                try:
                    results = st.session_state.event_loop.run_until_complete(
                        runner.run_all_tasks(st.session_state.tasks, max_turns)
                    )
                    st.session_state.results = results
                    
                    # Save results
                    output_path = save_results(results)
                    st.session_state.output_path = output_path
                    st.session_state.benchmark_completed = True
                    
                    # Success - will auto-show results below
                    st.success("✅ Benchmarks completed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error running benchmarks: {str(e)}")
                
        
        # Load existing results
        st.markdown("---")
        
        # Results section icon
        st.markdown('<div class="centered-icon">📥</div>', unsafe_allow_html=True)
        
        results_file_uploader = st.file_uploader(
            "Upload a previous results JSON file:",
            type=['json'],
            key="results_uploader",
            help="Upload a benchmark results file to view previous comparisons"
        )
        
        if results_file_uploader is not None:
            try:
                results = json.load(results_file_uploader)
                st.session_state.results = results
                st.success(f"✅ Loaded results from {results_file_uploader.name}")
            except json.JSONDecodeError:
                st.error("❌ Invalid JSON file")
            except Exception as e:
                st.error(f"❌ Error loading results: {str(e)}")
    
    # Main content
    if "tasks" in st.session_state:
        tasks_source = st.session_state.get('tasks_source', 'unknown')
        st.subheader(f"📋 Loaded Tasks ({len(st.session_state.tasks)})")
        st.caption(f"Source: {tasks_source}")
        
        # Display tasks in expandable sections
        for task in st.session_state.tasks:
            with st.expander(f"Task {task['task_id']}: {task['user_query'][:60]}..."):
                st.markdown(f"**Query:** {task['user_query']}")
                st.markdown(f"**Expected Behavior:** {task.get('expected_behaviour', 'N/A')}")
                st.markdown(f"**Expected Output:** {task.get('expected_output', 'N/A')}")
    
    # Display results
    if "results" in st.session_state:
        results = st.session_state.results
        
        st.markdown("---")
        st.header("📈 Benchmark Results")
        
        # Show completion banner if just completed
        if st.session_state.get("benchmark_completed", False):
            st.success(f"🎉 Benchmarks completed successfully! Analyzed {len(results)} tasks.")
            if "output_path" in st.session_state:
                # Extract just the filename for display
                filename = os.path.basename(st.session_state.output_path)
                st.caption(f"💾 Saved as: {filename}")
            # Clear the flag
            st.session_state.benchmark_completed = False
        
        # Create DataFrame
        df = create_comparison_dataframe(results)
        
        if not df.empty:
            # Summary metrics
            st.subheader("📊 Summary Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                ce_success_rate = (df['CE Success'] == '✅').sum() / len(df) * 100
                st.metric("CE Success Rate", f"{ce_success_rate:.0f}%")
            
            with col2:
                trad_success_rate = (df['Trad Success'] == '✅').sum() / len(df) * 100
                st.metric("Trad Success Rate", f"{trad_success_rate:.0f}%")
            
            with col3:
                avg_time_diff = df['Time Diff (s)'].mean()
                st.metric(
                    "Avg Time Difference",
                    f"{avg_time_diff:.2f}s",
                    delta=f"{avg_time_diff:.2f}s",
                    delta_color="inverse"
                )
            
            with col4:
                avg_tokens_diff = df['Tokens Diff'].mean()
                st.metric(
                    "Avg Token Difference",
                    f"{avg_tokens_diff:.0f}",
                    delta=f"{avg_tokens_diff:.0f}",
                    delta_color="inverse"
                )
            
            # Visualizations
            st.markdown("---")
            st.subheader("📊 Visualizations")
            
            tab1, tab2, tab3, tab4 = st.tabs(["Time", "LLM Calls", "Tokens", "Aggregate"])
            
            with tab1:
                st.plotly_chart(plot_time_comparison(df), use_container_width=True)
            
            with tab2:
                st.plotly_chart(plot_llm_calls_comparison(df), use_container_width=True)
            
            with tab3:
                st.plotly_chart(plot_tokens_comparison(df), use_container_width=True)
            
            with tab4:
                agg_fig = plot_aggregate_metrics(results)
                if agg_fig:
                    st.plotly_chart(agg_fig, use_container_width=True)
            
            # Data table
            st.markdown("---")
            st.subheader("📋 Results Table")
            st.dataframe(df, use_container_width=True)
            
            # Detailed task results
            st.markdown("---")
            st.subheader("🔍 Detailed Task Results")
            
            for result in results:
                display_task_details(result)
        else:
            st.warning("No comparison data available in results")
    else:
        # Welcome message
        st.info("👈 Load tasks from the sidebar to get started!")
        
        st.markdown("""
        ### How to use:
        1. **Set Max Turns**: Configure the maximum LLM turns (default: 3)
        2. **Load Tasks**: 
           - Click "📋 Load Default Tasks" for the pre-configured examples
           - Or upload your own tasks JSON file using the file uploader
        3. **Run Benchmarks**: Click the "🚀 Run Benchmarks" button to execute both approaches
        4. **View Results**: Explore visualizations and detailed results for each task
        5. **Load Previous Results**: Upload a previous results file to review past benchmarks
        
        ### Task JSON Format:
        ```json
        [
          {
            "task_id": 1,
            "user_query": "Your query here",
            "expected_behaviour": "What the agent should do",
            "expected_output": "What output is expected"
          }
        ]
        ```
        
        ### Quick Start:
        1. Click "📋 Load Default Tasks" in the sidebar
        2. Click "🚀 Run Benchmarks"
        3. Wait for completion and explore results!
        """)


if __name__ == "__main__":
    main()

