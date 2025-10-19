"""
API Blueprint for Portfolio Analysis Application

This blueprint handles all API endpoints for Schwab integration and portfolio analysis.
"""

from flask import Blueprint

# Create the API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import routes after blueprint creation to avoid circular imports
from app.blueprints.api import routes_auth, routes_overview, routes_risk
