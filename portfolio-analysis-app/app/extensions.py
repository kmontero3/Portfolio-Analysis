"""
Flask Extensions

Initialize Flask extensions here. Extensions are initialized without an app instance
and then initialized with the app in the create_app factory function.
"""

from flask_cors import CORS

# Initialize extensions
cors = CORS()

def init_extensions(app):
    """Initialize Flask extensions with app instance"""
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
