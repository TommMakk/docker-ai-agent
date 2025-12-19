"""
Chat AI Services Module

Experimental module for testing LLM configurations and structured outputs.

WARNING: This module is primarily for development/testing purposes. The main
application uses api.ai.services instead. Functions here demonstrate:
- Direct LLM initialization
- Structured output patterns
- Email generation with prompt engineering

This module is not used in production and serves as a reference implementation.
"""

import os
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# ============================================================================
# Structured Output Schema
# ============================================================================

class EmailMessage(BaseModel):
    """
    Email message structure for LLM output validation.
    
    This schema ensures LLM outputs are properly structured when generating
    email messages. The same schema is defined in api.ai.schemas for 
    production use.
    
    Attributes:
        subject (str): Email subject line
        contents (str): Email body content
        invalid_request (bool): Flag if request was invalid
    """
    subject: str = Field(description="Email subject")
    contents: str = Field(description="Email body content (plaintext)")
    invalid_request: bool | None = Field(
        default=False,
        description="Whether the request was invalid"
    )


# ============================================================================
# LLM Configuration (Development/Testing)
# ============================================================================

# Load LLM configuration from environment
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL')
OPENAI_MODEL_NAME = os.environ.get('OPENAI_MODEL_NAME', 'gpt-4o-mini')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY must be set. "
        "For local LLM testing, a dummy value is acceptable."
    )

# Prepare LLM configuration parameters
openai_params = {
    "model": OPENAI_MODEL_NAME,
    "api_key": OPENAI_API_KEY,
}

# Add custom base URL if using local LLM
if OPENAI_BASE_URL:
    openai_params["base_url"] = OPENAI_BASE_URL

# ============================================================================
# Example Usage (Development Testing)
# ============================================================================

# Initialize LLM with structured output schema
llm_base = ChatOpenAI(**openai_params)
llm = llm_base.with_structured_output(EmailMessage)

# Example message chain for testing
example_messages = [
    (
        "system",
        "You are a helpful assistant for research and composing plaintext emails. "
        "Do not use markdown in your response - use plaintext only.",
    ),
    (
        "human",
        "Create an email about the benefits of coffee. "
        "Do not use markdown and only use plaintext."
    ),
]

# Test LLM invocation (runs when module is imported/executed)
if __name__ == "__main__":
    print("Testing LLM structured output...")
    response = llm.invoke(example_messages)
    print(response)