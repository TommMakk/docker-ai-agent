"""
Chat Message Data Models

Defines Pydantic and SQLModel models for chat messages:
- ChatMessagePayload: Request validation for incoming messages
- ChatMessage: Database model for message persistence
- ChatMessageListItem: Response model for message listings
"""

from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, DateTime


# ============================================================================
# Utilities
# ============================================================================

def get_utc_now() -> datetime:
    """
    Get current UTC timestamp with timezone info.
    
    Returns:
        datetime: Current time in UTC timezone
    """
    return datetime.now(timezone.utc)


# ============================================================================
# Request Models
# ============================================================================

class ChatMessagePayload(SQLModel):
    """
    Request model for creating a new chat message.
    
    Used for request validation and schema documentation in FastAPI.
    
    Attributes:
        message (str): The content of the chat message from the user
    """
    message: str


# ============================================================================
# Database Models
# ============================================================================

class ChatMessage(SQLModel, table=True):
    """
    Database model for persisting chat messages.
    
    Represents a message stored in the database with automatic
    timestamp tracking.
    
    Attributes:
        id (int): Primary key, auto-generated
        message (str): Message content
        created_at (datetime): Timestamp when message was created (UTC)
    """
    id: int | None = Field(default=None, primary_key=True)
    message: str = Field(description="Message content")
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        description="Timestamp when message was created"
    )


# ============================================================================
# Response Models
# ============================================================================

class ChatMessageListItem(SQLModel):
    """
    Response model for listing recent chat messages.
    
    Used when returning message lists to clients. Includes message
    content and creation timestamp.
    
    Attributes:
        id (int): Message identifier
        message (str): Message content
        created_at (datetime): When the message was created
    """
    id: int | None = Field(default=None, description="Message ID")
    message: str = Field(description="Message content")
    created_at: datetime = Field(description="Message creation timestamp")