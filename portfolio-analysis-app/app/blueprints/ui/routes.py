"""
UI Routes for Portfolio Analysis Application

Handles rendering of HTML pages and templates.
"""

from flask import render_template, redirect, url_for
from app.blueprints.ui import ui_bp


@ui_bp.route('/')
def index():
    """
    Home page - redirects to overview.
    """
    return redirect(url_for('ui.overview'))


@ui_bp.route('/overview')
def overview():
    """
    Portfolio overview page.
    
    Displays portfolio summary, holdings, charts, and risk metrics.
    """
    return render_template('overview.html')


@ui_bp.route('/risk')
def risk_analysis():
    """
    Risk analysis page.
    
    Displays detailed risk metrics and analysis.
    """
    # Placeholder for future implementation
    return render_template('base.html')


@ui_bp.route('/performance')
def performance():
    """
    Performance tracking page.
    
    Displays portfolio performance over time.
    """
    # Placeholder for future implementation
    return render_template('base.html')


@ui_bp.route('/settings')
def settings():
    """
    Application settings page.
    """
    # Placeholder for future implementation
    return render_template('base.html')
