"""
Email Assistant Module

Experimental assistant implementation using tool binding pattern.

This module demonstrates an alternative approach to agent creation using
LangChain's bind_tools pattern. It creates a simple email assistant
that can:
- Accept natural language queries
- Automatically detect and invoke email tools
- Handle tool results and generate responses

WARNING: This is an experimental module not currently used in production.
The main application uses the multi-agent supervisor pattern (api.ai.agents).
This serves as a reference implementation for tool binding approaches.
"""

from api.ai.llms import get_openai_llm
from api.ai.tools import send_me_email, get_unread_emails

# ============================================================================
# Tool Registry
# ============================================================================

# Dictionary mapping tool names to tool functions
EMAIL_TOOLS = {
    "send_me_email": send_me_email,
    "get_unread_emails": get_unread_emails,
}


# ============================================================================
# Email Assistant
# ============================================================================

def email_assistant(query: str):
    """
    Simple email assistant using tool binding pattern.
    
    This function demonstrates an alternative to the React agent pattern.
    Instead of create_react_agent, it uses LLM.bind_tools() to enable
    tool calling, then manually handles tool invocation and response chaining.
    
    Workflow:
    1. Initialize LLM and bind available tools
    2. Send user query with tool definitions
    3. Check if LLM wants to call tools
    4. If tools requested: invoke them and get results
    5. Send results back to LLM for final response
    6. Return final response or initial response if no tools used
    
    Args:
        query (str): Natural language query from user
                    Example: "Send me an email about Python"
    
    Returns:
        dict or str: LLM response (either tool result or direct response)
        
    Example:
        response = email_assistant("Get my unread emails from the last 24 hours")
        print(response)
    
    Note:
        This is a simplified tool binding pattern. The production system
        uses create_react_agent which is more robust for complex workflows.
    """
    # Initialize LLM
    llm_base = get_openai_llm()
    
    # Bind tools to LLM (tells LLM what tools are available)
    # This enables the LLM to generate tool_calls in its response
    llm = llm_base.bind_tools(list(EMAIL_TOOLS.values()))

    # Create system and user messages
    system_prompt = "You are a helpful assistant for managing my email inbox."
    
    messages = [
        ("system", system_prompt),
        ("human", f"{query}.")
    ]
    
    # Initial LLM invocation - LLM may decide to call tools
    response = llm.invoke(messages)
    messages.append(response)
    
    # Check if LLM generated tool calls
    if hasattr(response, "tool_calls") and response.tool_calls:
        # Process each tool call
        for tool_call in response.tool_calls:
            tool_name = tool_call.get("name")
            tool_func = EMAIL_TOOLS.get(tool_name)
            tool_args = tool_call.get('args', {})
            
            # Skip if tool not found
            if not tool_func:
                print(f"Warning: Tool '{tool_name}' not found in EMAIL_TOOLS")
                continue
            
            # Invoke the tool with provided arguments
            tool_result = tool_func.invoke(tool_args)
            messages.append(tool_result)
        
        # Send tool results back to LLM for final response synthesis
        final_response = llm.invoke(messages)
        return final_response
    
    # Return initial response if no tools were used
    return response