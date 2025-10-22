"""
Helper script to extract and decode the authorization code from Schwab callback URL

Usage:
    python extract_auth_code.py
    
Then paste the full callback URL when prompted.
"""

from urllib.parse import urlparse, parse_qs, unquote

def extract_auth_code(callback_url):
    """
    Extract and decode the authorization code from the callback URL.
    
    Args:
        callback_url: Full callback URL with code parameter
        
    Returns:
        Decoded authorization code
    """
    try:
        # Parse the URL
        parsed = urlparse(callback_url)
        
        # Extract query parameters
        params = parse_qs(parsed.query)
        
        # Get the code parameter
        if 'code' in params:
            # URL decode the code (handles %40 -> @, etc.)
            code = unquote(params['code'][0])
            return code
        else:
            print("❌ No 'code' parameter found in URL")
            return None
            
    except Exception as e:
        print(f"❌ Error parsing URL: {e}")
        return None


def main():
    print("\n" + "="*80)
    print("SCHWAB AUTHORIZATION CODE EXTRACTOR")
    print("="*80 + "\n")
    
    print("After authorizing with Schwab, you'll be redirected to a URL like:")
    print("https://127.0.0.1:5000/callback?code=LONG_CODE_HERE&session=...")
    print()
    print("Paste the FULL callback URL below:\n")
    
    callback_url = input("Callback URL: ").strip()
    
    if not callback_url:
        print("\n❌ No URL provided")
        return 1
    
    print("\n" + "-"*80)
    code = extract_auth_code(callback_url)
    
    if code:
        print("\n✓ Authorization code extracted successfully!")
        print("\n" + "="*80)
        print("DECODED AUTHORIZATION CODE:")
        print("="*80)
        print(code)
        print("="*80 + "\n")
        print("Copy this code (without the lines) and paste it when running:")
        print("    python test_schwab_connection.py")
        print()
        return 0
    else:
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
