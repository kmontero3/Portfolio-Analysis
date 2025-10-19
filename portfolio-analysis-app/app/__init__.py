"""
Flask Application Factory

This module creates and configures the Flask application instance.
"""

from flask import Flask
from config import Config
from app.extensions import init_extensions


def create_app(config=None):
    """
    Create and configure the Flask application.
    
    Args:
        config: Configuration object or name ('development', 'production')
                If None, uses environment variable FLASK_ENV
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        # Use Config class directly - it already loads from environment
        app.config.from_object(Config)
    elif isinstance(config, str):
        # If a string is passed, still use Config (which reads from .env)
        app.config.from_object(Config)
    else:
        # If a config object is passed, use it
        app.config.from_object(config)
    
    # Initialize Flask extensions
    init_extensions(app)
    
    # Register blueprints
    from app.blueprints.ui import ui_bp
    from app.blueprints.api import api_bp
    
    app.register_blueprint(ui_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Log registered routes (useful for debugging)
    with app.app_context():
        print("\n=== Registered Routes ===")
        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            print(f"{rule.endpoint:50s} {methods:20s} {rule.rule}")
        print("========================\n")
    
    return app
