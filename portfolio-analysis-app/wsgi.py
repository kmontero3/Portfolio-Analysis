"""
Production WSGI Entry Point

This module provides the WSGI application for production deployment.

Usage with Gunicorn:
    gunicorn wsgi:application

Usage with uWSGI:
    uwsgi --http :5000 --wsgi-file wsgi.py --callable application
"""

from app import create_app

# Create Flask application instance for production
application = create_app()

# For debugging production setup (remove in actual production)
if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Portfolio Analysis Application - Production WSGI")
    print("="*60)
    print("  WARNING: This is the WSGI entry point.")
    print("  Do not run directly. Use a WSGI server like Gunicorn:")
    print("  ")
    print("    gunicorn wsgi:application")
    print("  ")
    print("  Or for testing production config:")
    print("  ")
    print("    python wsgi.py")
    print("="*60 + "\n")
    
    # Allow running directly for testing (not recommended for production)
    application.run(host='0.0.0.0', port=5000, debug=False)
