"""
Authentication blueprint.

- Single user: username 'FINITQ' and password 'INFINITQ' as requested.
- Uses Flask sessions for login state.
- Provides a `login_required` decorator for other routes.
"""
from __future__ import annotations

import functools
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, flash

auth_bp = Blueprint('auth', __name__)

# Hard-coded credentials as requested. You can later change to env vars.
_ALLOWED_USERNAME = "FINITQ"
_ALLOWED_PASSWORD = "INFINITQ"


def login_required(view):
    """Decorator to protect routes behind authentication."""

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)

    return wrapped_view


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if username == _ALLOWED_USERNAME and password == _ALLOWED_PASSWORD:
            session.clear()
            session['user'] = username
            # On successful login redirect to dashboard
            return redirect(url_for('dashboard.index'))
        else:
            error = 'Invalid credentials'
            flash(error, 'error')

    # Render a simple login page; templates/login.html should exist
    return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# Optional helper to get current user
def current_user():
    return session.get('user')