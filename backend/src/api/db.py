"""
Database Configuration Module

Handles database connection, initialization, and session management.
Uses SQLModel (SQLAlchemy + Pydantic) for ORM and model validation.

Environment Variables:
    DATABASE_URL: PostgreSQL connection string (required)
                 Format: postgresql+psycopg://user:password@host:port/database
"""

import os
from sqlmodel import SQLModel, Session, create_engine

# ============================================================================
# Database Configuration
# ============================================================================

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise NotImplementedError(
        "DATABASE_URL environment variable is required. "
        "Format: postgresql+psycopg://user:password@host:port/database"
    )

# Convert old postgres:// protocol to newer postgresql+psycopg protocol
DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://")

# Create database engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_size=10,  # Connection pool size
    max_overflow=20  # Max overflow connections
)


# ============================================================================
# Database Operations
# ============================================================================

def init_db():
    """
    Initialize database tables and schema.
    
    Creates all tables defined in SQLModel models based on their metadata.
    Should be called during application startup to ensure schema exists.
    
    Note:
        This is idempotent - can be safely called multiple times.
        Existing tables will not be recreated.
    """
    print("Initializing database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database initialization complete")


def get_session():
    """
    Dependency function for FastAPI that provides database sessions.
    
    Yields a new SQLModel Session for each request, automatically
    closing it when done. Used as a FastAPI dependency injection.
    
    Yields:
        Session: Active database session for the request
        
    Example:
        @router.get("/items/")
        def list_items(session: Session = Depends(get_session)):
            items = session.query(Item).all()
            return items
    """
    with Session(engine) as session:
        yield session