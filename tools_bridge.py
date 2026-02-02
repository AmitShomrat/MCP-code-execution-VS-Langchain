"""
Tools Bridge Server

FastAPI server that provides HTTP endpoints for filesystem tools.
This serves as a bridge to expose MCP filesystem server tools via REST API.
"""
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from servers.filesystem import (
    list_directory,
    inspect_csv,
    read_file,
    write_file
)


# Pydantic models for request/response validation
class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    version: str


class ListDirectoryRequest(BaseModel):
    """Request model for list_directory endpoint"""
    path: str


class InspectCsvRequest(BaseModel):
    """Request model for inspect_csv endpoint"""
    path: str


class ReadFileRequest(BaseModel):
    """Request model for read_file endpoint"""
    path: str


class WriteFileRequest(BaseModel):
    """Request model for write_file endpoint"""
    path: str
    content: str


class ToolResponse(BaseModel):
    """Generic response model for tool operations"""
    success: bool
    result: Any
    message: str = ""


# Initialize FastAPI application
app = FastAPI(
    title="Filesystem Tools Bridge API",
    description="HTTP API bridge for MCP filesystem server tools",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        HealthResponse with current status and timestamp
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/tools/list_directory", response_model=ToolResponse)
async def list_directory_endpoint(request: ListDirectoryRequest):
    """
    List files and directories at the specified path.
    
    Args:
        request: ListDirectoryRequest containing the path to list
        
    Returns:
        ToolResponse with list of files and directories
        
    Raises:
        HTTPException: If listing directory fails
    """
    try:
        result = await list_directory(request.path)
        return ToolResponse(
            success=True,
            result=result,
            message=f"Successfully listed directory: {request.path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list directory: {str(e)}"
        )


@app.post("/tools/inspect_csv", response_model=ToolResponse)
async def inspect_csv_endpoint(request: InspectCsvRequest):
    """
    Inspect a CSV file and return its structure and preview.
    
    Args:
        request: InspectCsvRequest containing the path to CSV file
        
    Returns:
        ToolResponse with CSV inspection results
        
    Raises:
        HTTPException: If inspecting CSV fails
    """
    try:
        result = await inspect_csv(request.path)
        return ToolResponse(
            success=True,
            result=result,
            message=f"Successfully inspected CSV: {request.path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to inspect CSV: {str(e)}"
        )


@app.post("/tools/read_file", response_model=ToolResponse)
async def read_file_endpoint(request: ReadFileRequest):
    """
    Read contents of a file at the specified path.
    
    Args:
        request: ReadFileRequest containing the path to read
        
    Returns:
        ToolResponse with file contents
        
    Raises:
        HTTPException: If reading file fails
    """
    try:
        result = await read_file(request.path)
        return ToolResponse(
            success=True,
            result=result,
            message=f"Successfully read file: {request.path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read file: {str(e)}"
        )


@app.post("/tools/write_file", response_model=ToolResponse)
async def write_file_endpoint(request: WriteFileRequest):
    """
    Write content to a file at the specified path.
    
    Args:
        request: WriteFileRequest containing path and content
        
    Returns:
        ToolResponse confirming write operation
        
    Raises:
        HTTPException: If writing file fails
    """
    try:
        result = await write_file(request.path, request.content)
        return ToolResponse(
            success=True,
            result=result,
            message=f"Successfully wrote to file: {request.path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to write file: {str(e)}"
        )


@app.get("/tools/available")
async def list_available_tools():
    """
    List all available filesystem tools.
    
    Returns:
        Dictionary with available tools and their descriptions
    """
    return {
        "tools": [
            {
                "name": "list_directory",
                "endpoint": "/tools/list_directory",
                "method": "POST",
                "description": "List files and directories at a specified path",
                "parameters": {"path": "string"}
            },
            {
                "name": "inspect_csv",
                "endpoint": "/tools/inspect_csv",
                "method": "POST",
                "description": "Inspect a CSV file structure and preview data",
                "parameters": {"path": "string"}
            },
            {
                "name": "read_file",
                "endpoint": "/tools/read_file",
                "method": "POST",
                "description": "Read contents of a file",
                "parameters": {"path": "string"}
            },
            {
                "name": "write_file",
                "endpoint": "/tools/write_file",
                "method": "POST",
                "description": "Write content to a file",
                "parameters": {"path": "string", "content": "string"}
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)