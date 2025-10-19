"""
Temporary OAuth Callback Server for Schwab API

This script starts a local web server to automatically capture the
authorization code from Schwab's OAuth redirect.

Usage:
    python auth_callback_server.py
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import webbrowser
import sys

# Global variable to store the authorization code
authorization_code = None


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP request handler for OAuth callback"""
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass
    
    def do_GET(self):
        """Handle GET request from OAuth redirect"""
        global authorization_code
        
        # Parse the URL and query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Extract the authorization code
        if 'code' in query_params:
            authorization_code = query_params['code'][0]
            
            # Send success response to browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            success_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Authorization Successful</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                        max-width: 500px;
                    }
                    h1 {
                        color: #28a745;
                        margin-bottom: 20px;
                    }
                    .code {
                        background: #f8f9fa;
                        padding: 15px;
                        border-radius: 5px;
                        font-family: monospace;
                        word-break: break-all;
                        margin: 20px 0;
                        border: 1px solid #dee2e6;
                    }
                    .checkmark {
                        font-size: 60px;
                        margin-bottom: 20px;
                    }
                    .info {
                        color: #6c757d;
                        margin-top: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="checkmark">✓</div>
                    <h1>Authorization Successful!</h1>
                    <p>Your authorization code has been captured.</p>
                    <div class="code">""" + authorization_code + """</div>
                    <p class="info">You can close this window and return to the terminal.</p>
                    <p class="info">The authorization will complete automatically.</p>
                </div>
            </body>
            </html>
            """
            
            self.wfile.write(success_html.encode())
            print(f"\n✓ Authorization code received: {authorization_code[:20]}...")
            
        else:
            # No code in URL - show error
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            error_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Authorization Failed</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                        max-width: 500px;
                    }
                    h1 {
                        color: #dc3545;
                        margin-bottom: 20px;
                    }
                    .error-icon {
                        font-size: 60px;
                        margin-bottom: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="error-icon">✗</div>
                    <h1>Authorization Failed</h1>
                    <p>No authorization code was found in the URL.</p>
                    <p>Please try the authorization process again.</p>
                </div>
            </body>
            </html>
            """
            
            self.wfile.write(error_html.encode())
            print("\n✗ No authorization code found in callback URL")


def main():
    """Main function to run the callback server"""
    from config import Config
    from api.schwab_client import SchwabClient
    
    print("\n" + "="*80)
    print("SCHWAB API - OAUTH CALLBACK SERVER")
    print("="*80 + "\n")
    
    # Initialize the Schwab client
    client = SchwabClient(
        api_key=Config.SCHWAB_API_KEY,
        api_secret=Config.SCHWAB_API_SECRET,
        redirect_uri=Config.SCHWAB_REDIRECT_URI
    )
    
    # Get the authorization URL
    auth_url = client.get_authorization_url()
    
    print("Step 1: Starting local callback server...")
    print("Server will listen on: https://127.0.0.1:5000")
    print()
    
    # Start the server in a separate thread
    server_address = ('127.0.0.1', 5000)
    
    try:
        # Note: This creates HTTP server, not HTTPS
        # For HTTPS, you'd need SSL certificates
        print("⚠️  Note: Starting HTTP server (not HTTPS)")
        print("If your redirect URI is HTTPS, you may need to manually copy the code from the URL.")
        print()
        
        server = HTTPServer(('127.0.0.1', 5000), CallbackHandler)
        
        print("Step 2: Opening authorization URL in browser...")
        print(f"URL: {auth_url}")
        print()
        
        # Open the browser
        webbrowser.open(auth_url)
        
        print("Step 3: Waiting for authorization...")
        print("Please log in and authorize the application in your browser.")
        print()
        print("Waiting for callback... (Press Ctrl+C to cancel)")
        print("-" * 80)
        
        # Handle one request (the callback)
        server.handle_request()
        
        if authorization_code:
            print("\n" + "="*80)
            print("Step 4: Exchanging code for tokens...")
            print("="*80 + "\n")
            
            # Exchange the code for tokens
            if client._exchange_code_for_token(authorization_code):
                print("✓ Successfully authenticated!")
                print()
                
                # Test connectivity
                print("Testing API connectivity...")
                client.print_connection_status()
                
                return 0
            else:
                print("✗ Failed to exchange code for tokens")
                return 1
        else:
            print("\n✗ No authorization code received")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Authorization cancelled by user")
        return 1
    except OSError as e:
        if "Address already in use" in str(e):
            print("✗ Error: Port 5000 is already in use!")
            print()
            print("Solutions:")
            print("1. Stop any other application using port 5000")
            print("2. Use the manual method (copy code from browser URL)")
            print("3. Change SCHWAB_REDIRECT_URI to use a different port")
        else:
            print(f"✗ Server error: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
