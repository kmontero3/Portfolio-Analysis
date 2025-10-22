"""
Test script to check Schwab API connectivity and endpoints.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.blueprints.api.schwab_integration import SchwabClient
from config import Config

def test_endpoints():
    """Test various Schwab API endpoints to see which ones work."""
    
    # Initialize client
    client = SchwabClient(
        api_key=Config.SCHWAB_API_KEY,
        api_secret=Config.SCHWAB_API_SECRET,
        redirect_uri=Config.SCHWAB_REDIRECT_URI
    )
    
    print("=" * 70)
    print("🔬 SCHWAB API ENDPOINT TESTER")
    print("=" * 70)
    
    if not client.access_token:
        print("\n❌ Not authenticated. Please run the OAuth flow first.")
        return
    
    print("\n✓ Authenticated with Schwab API")
    print(f"  Token expires: {client.token_expiry}")
    
    # Test 1: User Preferences (simple endpoint)
    print("\n" + "-" * 70)
    print("Test 1: User Preferences (/trader/v1/userPreference)")
    print("-" * 70)
    try:
        result = client.get_user_preferences()
        print(f"✓ Success! Response keys: {list(result.keys()) if isinstance(result, dict) else 'List response'}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 2: Accounts endpoint (no hash)
    print("\n" + "-" * 70)
    print("Test 2: Accounts List (/trader/v1/accounts)")
    print("-" * 70)
    try:
        result = client.get_account_data(account_hash=None, fields=None)
        print(f"✓ Success!")
        if isinstance(result, list):
            print(f"  Found {len(result)} account(s)")
            for idx, acc in enumerate(result, 1):
                print(f"  Account {idx}: {list(acc.keys())}")
        else:
            print(f"  Response type: {type(result)}")
            print(f"  Keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 3: Account Numbers endpoint
    print("\n" + "-" * 70)
    print("Test 3: Account Numbers (/trader/v1/accounts/accountNumbers)")
    print("-" * 70)
    try:
        result = client.get_account_numbers()
        print(f"✓ Success!")
        if isinstance(result, list):
            print(f"  Found {len(result)} account number(s)")
            for idx, acc in enumerate(result, 1):
                print(f"  Account {idx}: {acc}")
        else:
            print(f"  Response: {result}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print("\n" + "=" * 70)
    print("Testing complete")
    print("=" * 70)

if __name__ == "__main__":
    test_endpoints()
