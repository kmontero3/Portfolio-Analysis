"""
Development Entry Point

Run the Flask application in development mode with debug enabled.

Usage:
    python app.py
"""

from app import create_app

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Portfolio Analysis Application - Development Server")
    print("="*60)
    print(f"  Environment: {app.config.get('ENV', 'development')}")
    print(f"  Debug Mode: {app.config.get('DEBUG', True)}")
    print(f"  Server: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    # Run development server
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=True
    )
