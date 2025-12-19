"""
Email Sending Module

Handles SMTP operations for sending emails via Gmail or other SMTP providers.

Environment Variables:
    EMAIL_ADDRESS: Sender email address (required)
    EMAIL_PASSWORD: Email account password or app password (required)
    EMAIL_HOST: SMTP server hostname (default: smtp.gmail.com for Gmail)
    EMAIL_PORT: SMTP server port (default: 465 for SSL)
"""

import os
import smtplib
from email.message import EmailMessage

# ============================================================================
# Email Configuration
# ============================================================================

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 465))

# Validate required configuration
if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise ValueError(
        "EMAIL_ADDRESS and EMAIL_PASSWORD environment variables are required. "
        "For Gmail, use an app password instead of your account password."
    )


# ============================================================================
# Email Sending
# ============================================================================

def send_mail(
    subject: str = "No subject provided",
    content: str = "No message provided",
    to_email: str = None,
    from_email: str = None
) -> None:
    """
    Send an email via SMTP.
    
    Sends an email message using the configured SMTP server. Supports
    Gmail and other SMTP providers.
    
    Args:
        subject (str): Email subject line (default: generic text)
        content (str): Email body content (default: generic text)
        to_email (str): Recipient email address (default: configured EMAIL_ADDRESS)
        from_email (str): Sender email address (default: configured EMAIL_ADDRESS)
        
    Returns:
        None: Returns SMTP send status code on success
        
    Raises:
        smtplib.SMTPException: If SMTP operation fails
        ValueError: If email configuration is missing
        
    Note:
        For Gmail:
        - Use Gmail App Passwords (not your main password)
        - Enable "Less secure app access" if using account password
        - Ensure 2-factor authentication is enabled for app passwords
        
    Example:
        send_mail(
            subject="Hello",
            content="This is a test email",
            to_email="recipient@example.com"
        )
    """
    # Use configured defaults if not provided
    if to_email is None:
        to_email = EMAIL_ADDRESS
    if from_email is None:
        from_email = EMAIL_ADDRESS

    # Create email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(content)

    # Send via SMTP with SSL encryption
    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except smtplib.SMTPException as e:
        raise smtplib.SMTPException(
            f"Failed to send email to {to_email}: {str(e)}"
        ) from e