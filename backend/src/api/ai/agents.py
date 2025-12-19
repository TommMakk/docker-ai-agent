"""
AI Agent Factory Module

This module defines specialized AI agents that perform distinct tasks within
the multi-agent system:

- Email Agent: Manages email inbox operations (send, retrieve, manage emails)
- Research Agent: Conducts research on topics and generates summaries
- Supervisor Agent: Orchestrates task delegation between specialized agents

The module uses LangGraph's ReAct pattern for agent reasoning and tool usage.

Note: Currently uses langgraph_supervisor which requires a strong LLM for
reliable tool calling. Open source models may struggle with complex routing.
"""

from langgraph.prebuilt import create_react_agent

from api.ai.llms import get_openai_llm
from api.ai.tools import send_me_email, get_unread_emails

# Import supervisor - will raise ImportError if not available
try:
    from langgraph_supervisor import create_supervisor
except ImportError as e:
    raise ImportError(
        "langgraph_supervisor package is required but not installed. "
        "Install it or implement a custom supervisor pattern."
    ) from e


# Tools available to the email agent
EMAIL_AGENT_TOOLS = [send_me_email, get_unread_emails]

# System prompts for agent behavior
EMAIL_AGENT_SYSTEM_PROMPT = (
    "You are an intelligent email management assistant. Your responsibilities include:\n"
    "1. Composing and sending emails based on user requests\n"
    "2. Retrieving and summarizing unread emails from the inbox\n"
    "3. Helping organize and manage email communications\n"
    "\nAlways be professional and clear in email composition."
)

RESEARCH_AGENT_SYSTEM_PROMPT = (
    "You are a thorough research assistant specialized in gathering and "
    "synthesizing information. Your workflow:\n"
    "1. Conduct comprehensive research on the given topic\n"
    "2. Compile findings into a clear, structured summary\n"
    "3. Format results for email delivery using the send_me_email tool\n"
    "\nAlways cite sources when available and provide actionable insights."
)

SUPERVISOR_SYSTEM_PROMPT = (
    "You are a task orchestrator managing specialized agents:\n"
    "- Email Agent: Handles email operations\n"
    "- Research Agent: Conducts research and analysis\n"
    "\nYour role:\n"
    "1. Analyze incoming requests to determine which agent(s) should handle them\n"
    "2. Delegate tasks to the appropriate agent(s)\n"
    "3. Ensure tasks are completed in the correct sequence\n"
    "4. Synthesize results for the end user\n"
    "\nMake intelligent routing decisions based on task requirements."
)


def get_email_agent():
    """
    Create and configure the Email Management Agent.
    
    The email agent specializes in email operations including composition,
    sending, and retrieval. It has access to email-specific tools.
    
    Returns:
        Configured email agent ready for use in multi-agent workflows
    """
    model = get_openai_llm()
    
    email_agent = create_react_agent(
        model=model,
        tools=EMAIL_AGENT_TOOLS,
        prompt=EMAIL_AGENT_SYSTEM_PROMPT,
        name="email_agent"
    )
    
    return email_agent


def get_research_agent():
    """
    Create and configure the Research Agent.
    
    The research agent conducts research on topics and formats findings
    for email delivery. It includes email sending capability to deliver
    research results directly.
    
    Returns:
        Configured research agent ready for use in multi-agent workflows
    """
    model = get_openai_llm()
    
    research_agent = create_react_agent(
        model=model,
        tools=[send_me_email],
        prompt=RESEARCH_AGENT_SYSTEM_PROMPT,
        name='research_agent'
    )
    
    return research_agent


def get_supervisor(checkpointer=None):
    """
    Create and compile the Multi-Agent Supervisor.
    
    The supervisor orchestrates between specialized agents, routing tasks
    to the appropriate agent and managing multi-step workflows.
    
    Args:
        checkpointer (optional): Checkpoint manager for state persistence
                               and conversation history management
    
    Returns:
        Compiled supervisor graph ready to invoke with messages
        
    Note:
        The supervisor's effectiveness depends heavily on the underlying
        LLM's ability to understand tool schemas and make routing decisions.
        Stronger models (GPT-4, Claude) work better than open-source models.
    """
    llm = get_openai_llm()
    email_agent = get_email_agent()
    research_agent = get_research_agent()

    # Create supervisor that coordinates agent workflows
    supervisor = create_supervisor(
        agents=[email_agent, research_agent],
        model=llm,
        prompt=SUPERVISOR_SYSTEM_PROMPT
    ).compile(checkpointer=checkpointer)
    
    return supervisor