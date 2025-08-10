"""
JavaScript-related endpoints and Gemini proxy placeholders.

- Proxy to Gemini text/image generation (placeholder)
- Endpoint to accept uploaded media (photo/video) and prepare for emailing
- Note: All Gemini calls require API keys and you must add them to env vars.
"""
from __future__ import annotations

import os
import base64
from pathlib import Path
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app

from app.auth import login_required

js_bp = Blueprint('js_tools', __name__)


@js_bp.route('/gemini_text', methods=['POST'])
@login_required
def gemini_text():
    """Proxy endpoint to send a text prompt to Gemini API and return response.

    Expects JSON: {"prompt": "..."}
    """
    payload = request.json or {}
    prompt = payload.get('prompt')
    if not prompt:
        return jsonify({'error': 'prompt required'}), 400

    # Placeholder: implement your Gemini HTTP call here using requests
    # For now, return the prompt echoed back as "response".
    return jsonify({'response': f"(gemini placeholder) {prompt}"})


@js_bp.route('/upload_media', methods=['POST'])
@login_required
def upload_media():
    """Accept multipart file uploads (photo/video) from the JS frontend and save locally.

    Responds with a path that frontend can use to trigger email sending.
    """
    uploaded = request.files.get('file')
    if not uploaded:
        return jsonify({'error': 'file required'}), 400

    save_dir = Path(current_app.root_path) / 'uploads'
    save_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"upload_{timestamp}_{uploaded.filename}"
    dest = save_dir / filename
    uploaded.save(str(dest))

    return jsonify({'path': str(dest), 'filename': filename})


@js_bp.route('/send_captured_email', methods=['POST'])
@login_required
def send_captured_email():
    """Sample endpoint to send an uploaded image to an email address.

    Expects JSON: {"to": "...", "file_path": "...", "subject": "..."}
    """
    data = request.json or {}
    to = data.get('to')
    file_path = data.get('file_path')
    subject = data.get('subject', 'Captured Media')

    if not to or not file_path:
        return jsonify({'error': 'to and file_path required'}), 400

    # Use existing social_api.send_email function ideally — for brevity we just
    # return success if file exists.
    if not Path(file_path).exists():
        return jsonify({'error': 'file not found'}), 404

    # Placeholder: call sendgrid / smtp to attach and send the file
    return jsonify({'status': 'queued', 'to': to, 'file': file_path})
