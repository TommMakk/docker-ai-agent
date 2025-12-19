"""
Inbox Reading Module

High-level interface for reading and retrieving emails from Gmail inbox.
Abstracts the complexity of IMAP operations.

Environment Variables:
    EMAIL_ADDRESS: Gmail address (required)
    EMAIL_PASSWORD: Gmail app password (required)
"""

import os
from api.myemailer.gmail_imap_parser import GmailImapParser

# ============================================================================
# Email Configuration
# ============================================================================

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise ValueError(
        "EMAIL_ADDRESS and EMAIL_PASSWORD environment variables are required."
    )


# ============================================================================
# Inbox Operations
# ============================================================================

def read_inbox(hours_ago: int = 24, unread_only: bool = True, verbose: bool = False) -> list:
    """
    Retrieve emails from Gmail inbox.
    
    Fetches emails from the inbox within a specified time window.
    Can filter for unread messages only.
    
    Args:
        hours_ago (int): Number of hours to look back (default: 24 hours).
                        Retrieves emails from the past N hours.
        unread_only (bool): If True, only retrieve unread emails (default: True)
        verbose (bool): If True, print details about fetched emails (default: False)
        
    Returns:
        list: List of email dictionaries containing:
            - 'from': Sender email address
            - 'subject': Email subject
            - 'timestamp': Email date/time
            - 'body': Email body content
            - Additional email fields from IMAP
            
    Example:
        emails = read_inbox(hours_ago=48, unread_only=False)
        for email in emails:
            print(f"From: {email['from']}")
            print(f"Subject: {email['subject']}")
            print("---")
    """
    # Initialize IMAP parser
    parser = GmailImapParser(
        email_address=EMAIL_ADDRESS,
        app_password=EMAIL_PASSWORD
    )

    # Fetch emails within the time window
    emails = parser.fetch_emails(
        hours=hours_ago,
        unread_only=unread_only
    )

    # Print email summary if verbose mode enabled
    if verbose:
        print(f"\nRetrieved {len(emails)} emails from the past {hours_ago} hours:")
        for email in emails:
            print(f"  From: {email.get('from', 'Unknown')}")
            print(f"  Subject: {email.get('subject', '(No subject)')}")
            print(f"  Date: {email.get('timestamp', 'Unknown')}")
            print("  ---")

    return emails