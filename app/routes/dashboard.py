"""
Dashboard blueprint.

Renders the main dashboard UI. All routes here are protected with login_required.
"""
from __future__ import annotations

from flask import Blueprint, render_template
from app.auth import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    # Show dashboard page (templates/dashboard.html)
    user = current_user()
    return render_template('dashboard.html', user=user)


@dashboard_bp.route('/docker')
@login_required
def docker_ui():
    """Optional page for Docker dedicated UI."""
    return render_template('docker.html')


@dashboard_bp.route('/terminal')
@login_required
def terminal_ui():
    """Terminal full-screen UI page."""
    return render_template('terminal.html')