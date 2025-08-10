"""
Endpoints for email, SMS, calls, and social posts.

This module contains wrapper functions that call third-party APIs. API keys
should be stored in environment variables. All functions are intentionally
minimal and include placeholders where you must paste your API credentials.
"""
from __future__ import annotations

import os
from typing import Dict

from flask import Blueprint, request, jsonify

from app.auth import login_required

social_bp = Blueprint('social_api', __name__)


@social_bp.route('/send_email', methods=['POST'])
@login_required
def send_email():
    """Send an email using SendGrid (placeholder).

    Expects JSON: { "to": "to@example.com", "subject": "..", "content": ".." }
    """
    data = request.json or {}
    to = data.get('to')
    subject = data.get('subject')
    content = data.get('content')

    if not to or not subject or not content:
        return jsonify({'error': 'to, subject and content are required'}), 400

    # Placeholder SendGrid implementation
    # Install sendgrid: pip install sendgrid
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
    except Exception:
        return jsonify({'error': 'sendgrid package not installed'}), 500

    sg_api_key = os.environ.get('SENDGRID_API_KEY', 'PASTE_YOUR_SENDGRID_KEY')
    message = Mail(from_email=os.environ.get('EMAIL_FROM', 'noreply@example.com'), to_emails=to, subject=subject, html_content=content)
    try:
        sg = SendGridAPIClient(sg_api_key)
        resp = sg.send(message)
        return jsonify({'status': 'sent', 'code': resp.status_code}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@social_bp.route('/send_sms', methods=['POST'])
@login_required
def send_sms():
    """Send SMS using Twilio. Expects JSON: {"to": "+9112345...", "body": "..."}
    """
    data = request.json or {}
    to = data.get('to')
    body = data.get('body')
    if not to or not body:
        return jsonify({'error': 'to and body required'}), 400

    try:
        from twilio.rest import Client
    except Exception:
        return jsonify({'error': 'twilio package not installed'}), 500

    account_sid = os.environ.get('TWILIO_ACCOUNT_SID', 'PASTE_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN', 'PASTE_TOKEN')
    from_number = os.environ.get('TWILIO_FROM_NUMBER', 'whatsapp:+1415...')

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(body=body, from_=from_number, to=to)
        return jsonify({'status': 'sent', 'sid': message.sid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@social_bp.route('/post_x', methods=['POST'])
@login_required
def post_x():
    """Placeholder for posting to X (Twitter). Implement OAuth and posting properly."""
    data = request.json or {}
    text = data.get('text')
    if not text:
        return jsonify({'error': 'text required'}), 400

    # TODO: implement X posting via OAuth2 or OAuth1.0a
    return jsonify({'status': 'not_implemented', 'message': 'Add your X/Twitter implementation here'}), 501


@social_bp.route('/post_linkedin', methods=['POST'])
@login_required
def post_linkedin():
    """Placeholder for LinkedIn posting. Requires OAuth and app approval."""
    data = request.json or {}
    text = data.get('text')
    if not text:
        return jsonify({'error': 'text required'}), 400
    return jsonify({'status': 'not_implemented', 'message': 'Add LinkedIn Graph API call here'}), 501
