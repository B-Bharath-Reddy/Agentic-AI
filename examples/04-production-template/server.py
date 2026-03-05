"""
Production-Ready Agent Server
=============================
A FastAPI server with LangGraph agent, LangSmith tracing, and production features.

Features:
- FastAPI with async support
- LangGraph agent with memory
- LangSmith tracing for observability
- Health check endpoint
- Error handling and validation
- Rate limiting support
- Session management

Usage:
    uvicorn server:app --host 0.0.0.0 --port 8000
"""

import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configure LangSmith tracing (optional)
if os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "production-agents")
    logger.info("LangSmith tracing enabled")

# Import LangGraph components
try:
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.prebuilt import create_react_agent
    from langchain_openai import ChatOpenAI
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    logger.warning("LangGraph not installed. Running in demo mode.")


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class AgentRequest(BaseModel):
    """Request model for agent invocation."""
    message: str = Field(..., description="User message to process")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What time is it?",
                "session_id": "user-123-session"
            }
        }


class AgentResponse(BaseModel):
    """Response model for agent invocation."""
    response: str = Field(..., description="Agent response")
    session_id: str = Field(..., description="Session ID for future requests")
    timestamp: str = Field(..., description="Response timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: str
    version: str
    components: Dict[str, str]


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str
    detail: str
    timestamp: str


# ============================================================================
# TOOLS
# ============================================================================

def get_current_time() -> str:
    """
    Get the current time.
    
    Returns:
        Current time in HH:MM:SS format
    """
    return datetime.now().strftime("%H:%M:%S")


def get_current_date() -> str:
    """
    Get the current date.
    
    Returns:
        Current date in YYYY-MM-DD format
    """
    return datetime.now().strftime("%Y-%m-%d")


def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Result of the calculation
    """
    try:
        # Safe evaluation of simple math expressions
        allowed_chars = set("0123456789+-*/().% ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# List of available tools
TOOLS = [get_current_time, get_current_date, calculate]


# ============================================================================
# AGENT SETUP
# ============================================================================

# Global agent instance
agent = None
memory = None


def create_agent():
    """Create and configure the LangGraph agent."""
    if not LANGGRAPH_AVAILABLE:
        return None
    
    global agent, memory
    
    # Initialize memory for session persistence
    memory = MemorySaver()
    
    # Initialize LLM
    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        temperature=0.7
    )
    
    # Create ReAct agent
    agent = create_react_agent(
        model=llm,
        tools=TOOLS,
        checkpointer=memory,
        state_modifier="""You are a helpful AI assistant.

Available tools:
- get_current_time: Get the current time
- get_current_date: Get the current date  
- calculate: Evaluate mathematical expressions

Be helpful and concise in your responses."""
    )
    
    logger.info("Agent created successfully")
    return agent


# ============================================================================
# APPLICATION LIFESPAN
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    logger.info("Starting up agent server...")
    create_agent()
    yield
    # Shutdown
    logger.info("Shutting down agent server...")


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Agentic AI API",
    description="Production-ready agent API with LangGraph",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            detail=str(exc.detail),
            timestamp=datetime.now().isoformat()
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            detail="An unexpected error occurred",
            timestamp=datetime.now().isoformat()
        ).model_dump()
    )


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the API and its components.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        components={
            "agent": "ready" if agent else "not_initialized",
            "memory": "ready" if memory else "not_initialized",
            "langsmith": "enabled" if os.getenv("LANGSMITH_API_KEY") else "disabled"
        }
    )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Agentic AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.post("/agent/invoke", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest):
    """
    Invoke the agent with a message.
    
    This endpoint processes a user message through the agent and returns
    the response. Session ID is used to maintain conversation context.
    """
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="Agent not initialized. Check server logs."
        )
    
    # Generate session ID if not provided
    session_id = request.session_id or f"session-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    try:
        # Configure session for memory
        config = {"configurable": {"thread_id": session_id}}
        
        # Invoke agent
        result = await agent.ainvoke(
            {"messages": [("user", request.message)]},
            config=config
        )
        
        # Extract response
        response_content = result["messages"][-1].content
        
        logger.info(f"Processed request for session {session_id}")
        
        return AgentResponse(
            response=response_content,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            metadata={
                "message_count": len(result["messages"])
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.post("/agent/stream")
async def stream_agent(request: AgentRequest):
    """
    Stream agent responses.
    
    This endpoint streams the agent's response for real-time output.
    """
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="Agent not initialized"
        )
    
    session_id = request.session_id or f"session-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    config = {"configurable": {"thread_id": session_id}}
    
    async def generate():
        async for event in agent.astream(
            {"messages": [("user", request.message)]},
            config=config
        ):
            yield f"data: {event}\n\n"
    
    from fastapi.responses import StreamingResponse
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/tools")
async def list_tools():
    """List available tools."""
    return {
        "tools": [
            {
                "name": tool.__name__,
                "description": tool.__doc__.strip().split("\n")[0] if tool.__doc__ else "No description"
            }
            for tool in TOOLS
        ]
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )