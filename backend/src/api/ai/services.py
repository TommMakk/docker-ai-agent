"""
AI Services Module

Provides high-level AI functions for generating structured outputs from LLMs.
Handles prompt engineering and output validation through LangChain.
"""

from api.ai.llms import get_openai_llm
from api.ai.schemas import EmailMessageSchema


def generate_email_message(query: str) -> EmailMessageSchema:
    """
    Generate a structured email message from a natural language query.
    
    Uses the configured LLM to generate email subject and content based
    on the provided query. Output is structured and validated using
    Pydantic schema.
    
    Args:
        query (str): Natural language request/topic for email generation
        
    Returns:
        EmailMessageSchema: Structured email with subject and plaintext content
        
    Note:
        - LLM is instructed to use plaintext only (no markdown)
        - Uses LangChain's structured_output for reliable parsing
        - System prompt emphasizes email best practices
        
    Example:
        result = generate_email_message("Create a latte recipe")
        print(result.subject)  # "Latte Recipe Guide"
        print(result.contents)  # "To make a latte..."
    """
    # Initialize LLM with structured output
    llm_base = get_openai_llm()
    llm_with_schema = llm_base.with_structured_output(EmailMessageSchema)

    # Define system and user prompts
    system_prompt = (
        "You are a helpful assistant specializing in research and composing "
        "professional plaintext emails. Generate clear, well-structured email "
        "content without any markdown formatting. "
        "Use only plaintext with basic formatting (line breaks, spaces)."
    )
    
    user_prompt = (
        f"{query}. "
        "Generate a professional email with subject and content. "
        "Do not use markdown or special formatting - plaintext only."
    )

    # Create message chain and invoke LLM
    messages = [
        ("system", system_prompt),
        ("human", user_prompt),
    ]

    return llm_with_schema.invoke(messages)