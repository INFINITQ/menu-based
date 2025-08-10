"""
Small validation helpers for inputs coming from the frontend.
"""
from __future__ import annotations

import re


def is_safe_name(name: str) -> bool:
    """Allow only alphanumeric, hyphen, underscore and dot, and length limit."""
    if not name:
        return False
    if len(name) > 255:
        return False
    return re.match(r'^[A-Za-z0-9_\-\.]+$', name) is not None