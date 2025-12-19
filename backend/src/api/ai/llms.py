"""
Language Model Configuration Module

This module manages the initialization and configuration of LLM instances used
throughout the application. It supports both local and cloud-based LLM backends
via environment variable configuration.

Environment Variables:
    OPENAI_BASE_URL: Optional URL for local/custom LLM endpoint (e.g., Ollama)
    OPENAI_MODEL_NAME: Name of the model to use (default: 'gpt-4o-mini')
    OPENAI_API_KEY: API key for the LLM service (required)
"""

import os
from langchain_openai import ChatOpenAI

# Configuration from environment variables
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL')
OPENAI_MODEL_NAME = os.environ.get('OPENAI_MODEL_NAME', 'gpt-4o-mini')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Validate required configuration
if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY environment variable must be set. "
        "For local LLM testing, a dummy value is acceptable."
    )


def get_openai_llm() -> ChatOpenAI:
    """
    Initialize and return a ChatOpenAI language model instance.
    
    Supports both cloud-based OpenAI models and local LLM backends
    (e.g., Ollama, LM Studio) by allowing custom base URLs.
    
    Returns:
        ChatOpenAI: Configured language model instance ready for use.
        
    Raises:
        RuntimeError: If required environment variables are not set.
    """
    llm_config = {
        "model": OPENAI_MODEL_NAME,
        "api_key": OPENAI_API_KEY,
    }
    
    # Add custom base URL if configured (for local LLM endpoints)
    if OPENAI_BASE_URL:
        llm_config["base_url"] = OPENAI_BASE_URL

    return ChatOpenAI(**llm_config)