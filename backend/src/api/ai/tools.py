"""
AI Agent Tools Module

This module defines callable tools/functions that AI agents can invoke during
conversation. Tools include email management (sending, reading) and research capabilities.

Each tool is decorated with @tool from LangChain, making it discoverable and
callable by language models in an agentic workflow.
"""

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from api.myemailer.sender import send_mail
from api.myemailer.inbox_reader import read_inbox
from api.ai.services import generate_email_message


@tool
def research_email(query: str, config: RunnableConfig) -> str:
    """
    Generate research content for a given query and format it as email content.
    
    This tool uses the email service to generate structured research responses
    that can be formatted and sent via email.
    
    Args:
        query (str): The research topic or question to investigate
        config (RunnableConfig): Runtime configuration including metadata
        
    Returns:
        str: Formatted email content with subject and body
    """
    metadata = config.get('metadata', {})
    additional_field = metadata.get("additional_field")
    
    # Generate research content
    research_response = generate_email_message(query)
    
    # Format as email with subject and body
    formatted_message = f"Subject: {research_response.subject}\nBody: {research_response.contents}"
    return formatted_message


@tool
def send_me_email(subject: str, content: str) -> str:
    """
    Send an email with the specified subject and content.
    
    This tool interfaces with the email sending service to deliver messages
    to the configured recipient.
    
    Args:
        subject (str): Email subject line
        content (str): Email body content
        
    Returns:
        str: Status message indicating success or failure
    """
    try:
        send_mail(subject=subject, content=content)
        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {str(e)}"


@tool
def get_unread_emails(hours_ago: int = 48) -> str:
    """
    Retrieve unread emails from the inbox within a specified time window.
    
    Fetches emails from the configured inbox and formats them for display.
    HTML content is stripped to keep responses concise.
    
    Args:
        hours_ago (int): Number of hours to look back (default: 48 hours).
                        Retrieves emails from the past 48 hours if not specified.
        
    Returns:
        str: Formatted string of emails separated by '-----' delimiters.
             Returns up to 500 characters of content.
             
    Raises:
        Returns error message string if inbox read operation fails.
    """
    try:
        emails = read_inbox(hours_ago=hours_ago, verbose=False)
    except Exception as e:
        return f"Error retrieving emails: {str(e)}"
    
    # Process and format emails
    formatted_emails = []
    for email in emails:
        email_data = email.copy()
        
        # Remove HTML content to keep responses clean
        if "html_body" in email_data:
            email_data.pop('html_body')
        
        # Format email fields
        email_message = ""
        for key, value in email_data.items():
            email_message += f"{key}:\t{value}\n"
        
        formatted_emails.append(email_message)
    
    # Join emails and limit output size
    return "\n-----\n".join(formatted_emails)[:500]