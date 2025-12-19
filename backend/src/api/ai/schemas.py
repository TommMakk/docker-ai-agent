"""
AI System Schema Models

Defines Pydantic models for agent responses and structured outputs.
Used for response validation and serialization.
"""

from pydantic import BaseModel, Field


class EmailMessageSchema(BaseModel):
    """
    Structured schema for AI-generated email messages.
    
    This schema ensures that LLM outputs conform to a specific structure
    with subject and content fields. Used with LangChain's
    structured_output feature for reliable parsing.
    
    Attributes:
        subject (str): Email subject line
        contents (str): Email body content in plaintext (no markdown)
        invalid_request (bool): Flag indicating if request was invalid
    """
    subject: str = Field(description="Email subject line")
    contents: str = Field(description="Email body content (plaintext only)")
    invalid_request: bool | None = Field(
        default=False,
        description="Indicates if the request was invalid or malformed"
    )


class SupervisorMessageSchema(BaseModel):
    """
    Response schema for supervisor agent outputs.
    
    Represents the final message response from the multi-agent supervisor
    system. Contains the synthesized result after agent coordination.
    
    Attributes:
        content (str): The text content of the supervisor's response
    """
    content: str = Field(description="Response content from the supervisor agent")