"""
Pydantic models for FastAPI request and response validation.

This module defines all data models used in the API endpoints,
ensuring proper validation and documentation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class QueryRequest(BaseModel):
    """
    Request model for benchmark execution.
    
    Attributes:
        query: User query string to be processed by the benchmark
    """
    query: str = Field(
        ...,
        description="User query to process",
        min_length=1,
        max_length=2000,
        examples=["Calculate total revenue in Sales_Records.csv"]
    )


class TokenUsage(BaseModel):
    """
    Model for token usage information.
    
    Attributes:
        prompt_tokens: Number of tokens in the prompt
        completion_tokens: Number of tokens in the completion
        total_tokens: Total number of tokens used
    """
    prompt_tokens: int = Field(..., description="Number of input tokens", ge=0)
    completion_tokens: int = Field(..., description="Number of output tokens", ge=0)
    total_tokens: int = Field(..., description="Total tokens used", ge=0)


class LLMCallDetail(BaseModel):
    """
    Model for individual LLM call details.
    
    Attributes:
        call_number: Sequential number of the LLM call
        latency: Time taken for this call in seconds
        tokens: Token usage for this call
    """
    call_number: int = Field(..., description="LLM call sequence number", ge=1)
    latency: float = Field(..., description="Call latency in seconds", ge=0)
    tokens: TokenUsage = Field(..., description="Token usage details")


class BenchmarkResult(BaseModel):
    """
    Model for benchmark execution result.
    
    Attributes:
        success: Whether the benchmark completed successfully
        final_output: Final output from the benchmark execution
        error: Error message if any
        time: Total execution time in seconds
        llm_calls: List of individual LLM call details
        total_tokens: Total token usage across all calls
    """
    success: bool = Field(..., description="Execution success status")
    final_output: str = Field(..., description="Final output text")
    error: Optional[str] = Field(None, description="Error message if failed")
    time: float = Field(..., description="Total execution time in seconds", ge=0)
    llm_calls: List[LLMCallDetail] = Field(..., description="List of LLM call details")
    total_tokens: TokenUsage = Field(..., description="Total token usage")


class BenchmarkResponse(BaseModel):
    """
    Response model for benchmark execution endpoint.
    
    Attributes:
        success: Whether the API call was successful
        approach: Name of the benchmark approach used
        result: Detailed benchmark results
        message: Optional message for additional information
    """
    success: bool = Field(..., description="API call success status")
    approach: str = Field(..., description="Benchmark approach name")
    result: BenchmarkResult = Field(..., description="Benchmark execution results")
    message: Optional[str] = Field(None, description="Additional information")


class BenchmarkHistoryItem(BaseModel):
    """
    Model for a single benchmark history entry.
    
    Attributes:
        timestamp: ISO format timestamp of execution
        query: Query that was executed
        result: Benchmark results
    """
    timestamp: str = Field(..., description="Execution timestamp (ISO format)")
    query: str = Field(..., description="Executed query")
    result: Dict[str, Any] = Field(..., description="Benchmark results")


class ComparisonResponse(BaseModel):
    """
    Response model for benchmark comparison endpoint.
    
    Attributes:
        success: Whether the comparison was successful
        traditional_mcp: List of traditional MCP benchmark results
        code_execution_mcp: List of code execution MCP benchmark results
        total_count: Total number of benchmark results
    """
    success: bool = Field(..., description="Comparison success status")
    traditional_mcp: List[BenchmarkHistoryItem] = Field(
        ...,
        description="Traditional MCP benchmark history"
    )
    code_execution_mcp: List[BenchmarkHistoryItem] = Field(
        ...,
        description="Code execution MCP benchmark history"
    )
    total_count: Dict[str, int] = Field(
        ...,
        description="Count of results per approach"
    )


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint.
    
    Attributes:
        status: Service status
        timestamp: Current server timestamp
        version: API version
    """
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current server timestamp")
    version: str = Field(..., description="API version")

