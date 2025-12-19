"""
FastAPI Application Entry Point

Main application module that initializes the FastAPI server, configures
lifespan hooks for database setup, and registers API routers.

This module sets up:
- Database initialization on startup
- API router registration with URL prefixes
- Environment variable validation
- Health check endpoints
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.db import init_db
from api.chat.routing import router as chat_router

# ============================================================================
# Application Lifespan Configuration
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.
    
    Startup:
        - Initializes database tables and schema
        
    Shutdown:
        - Graceful cleanup (if needed)
    """
    # Startup
    init_db()
    yield
    # Shutdown


# ============================================================================
# Application Configuration
# ============================================================================

# Initialize FastAPI app with lifespan configuration
app = FastAPI(
    title="Deploy AI Agent",
    description="Multi-agent AI system for email and research tasks",
    version="1.0.0",
    lifespan=lifespan
)

# Include API routers
app.include_router(chat_router, prefix="/api/chats")

# ============================================================================
# Environment Configuration
# ============================================================================

# Application configuration from environment
MY_PROJECT = os.environ.get("MY_PROJECT", "Deploy AI Agent System")
API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    raise ValueError(
        "API_KEY environment variable must be set for security validation"
    )

# ============================================================================
# Health and Status Endpoints
# ============================================================================

@app.get("/")
def read_index():
    """
    Root endpoint for application status and metadata.
    
    Returns:
        dict: Basic application information including name and status
    """
    return {
        "hello": "Welcome to Deploy AI Agent",
        "project_name": MY_PROJECT,
        "status": "operational"
    }