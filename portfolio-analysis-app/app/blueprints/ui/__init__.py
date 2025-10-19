"""
UI Blueprint for Portfolio Analysis Application

This blueprint handles all user-facing web pages and templates.
"""

from flask import Blueprint

# Create the UI blueprint with static/templates folders
ui_bp = Blueprint(
    'ui',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

# Import routes after blueprint creation to avoid circular imports
from app.blueprints.ui import routes
