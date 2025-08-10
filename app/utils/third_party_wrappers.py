"""
Wrappers for SendGrid, Twilio and placeholder methods for social posting.

Store API keys in environment variables and keep this file small and focused.
"""
from __future__ import annotations

import os
from typing import Dict, Any


def send_email_sendgrid(to: str, subject: str, html_content: str) -> Dict[str, Any]:
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
    except Exception as e:
        raise RuntimeError('sendgrid package not installed') from e

    api_key = os.environ.get('SENDGRID_API_KEY') or 'PASTE_YOUR_SENDGRID_KEY'
    from_addr = os.environ.get('EMAIL_FROM', 'noreply@example.com')

    message = Mail(from_email=from_addr, to_emails=to, subject=subject, html_content=html_content)
    sg = SendGridAPIClient(api_key)
    resp = sg.send(message)
    return {'status_code': resp.status_code}


def send_sms_twilio(to: str, body: str) -> Dict[str, Any]:
    try:
        from twilio.rest import Client
    except Exception as e:
        raise RuntimeError('twilio package not installed') from e

    account_sid = os.environ.get('TWILIO_ACCOUNT_SID', 'PASTE_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN', 'PASTE_TOKEN')
    from_number = os.environ.get('TWILIO_FROM_NUMBER', '')

    client = Client(account_sid, auth_token)
    msg = client.messages.create(body=body, from_=from_number, to=to)
    return {'sid': msg.sid, 'status': msg.status}


def placeholder_post_x(text: str) -> Dict[str, Any]:
    # Implement OAuth flow and use Twitter/X API
    return {'status': 'not_implemented'}


def placeholder_post_linkedin(text: str) -> Dict[str, Any]:
    # Implement LinkedIn Graph API usage here
    return {'status': 'not_implemented'}