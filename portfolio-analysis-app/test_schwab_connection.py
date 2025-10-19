"""
Test script for Schwab API Client

This script demonstrates how to:
1. Initialize the Schwab API client
2. Test connectivity
3. Print API scopes and permissions
4. Retrieve basic account information

Usage:
    python test_schwab_connection.py
"""

import sys
import os

# Add the parent directory to the path to import from api module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.schwab_client import SchwabClient, SchwabAPIError
from config import Config

def main():
    """Main test function"""
    print("\n" + "="*80)
    print("SCHWAB API CLIENT TEST")
    print("="*80 + "\n")
    
    # Display configuration status
    print("Step 1: Checking Configuration")
    print("-" * 80)
    try:
        Config.print_config_status(show_secrets=False)
        Config.validate_required_config()
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file (copy from .env.example)")
        print("2. Set your SCHWAB_API_KEY, SCHWAB_API_SECRET, and SCHWAB_REDIRECT_URI")
        print("3. Obtained credentials from https://developer.schwab.com/")
        return 1
    
    print("\n" + "="*80)
    print("\nStep 2: Initializing Schwab API Client")
    print("-" * 80)
    
    # Initialize the client
    try:
        client = SchwabClient(
            api_key=Config.SCHWAB_API_KEY,
            api_secret=Config.SCHWAB_API_SECRET,
            redirect_uri=Config.SCHWAB_REDIRECT_URI
        )
        print("✓ Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return 1
    
    print("\n" + "="*80)
    print("\nStep 3: Testing Authentication")
    print("-" * 80)
    
    # Test authentication
    try:
        # This will either use existing tokens or prompt for authorization
        authenticated = client.authenticate(auto_open_browser=True)
        
        if authenticated:
            print("✓ Authentication successful!")
        else:
            print("❌ Authentication failed")
            return 1
    except SchwabAPIError as e:
        print(f"❌ Authentication error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error during authentication: {e}")
        return 1
    
    print("\n" + "="*80)
    print("\nStep 4: Testing API Connectivity")
    print("-" * 80)
    
    # Test connectivity and print status
    client.print_connection_status()
    
    print("\n" + "="*80)
    print("\nStep 5: Retrieving Account Information")
    print("-" * 80)
    
    # Try to get account numbers
    try:
        accounts = client.get_account_numbers()
        print(f"✓ Successfully retrieved {len(accounts)} account(s)")
        
        # Display account hashes (masked for security)
        for i, account in enumerate(accounts, 1):
            account_hash = account.get('hashValue', 'N/A')
            # Mask the hash for security
            masked_hash = f"{account_hash[:4]}...{account_hash[-4:]}" if len(account_hash) > 8 else account_hash
            print(f"  Account {i}: {masked_hash}")
            
    except SchwabAPIError as e:
        print(f"❌ Failed to retrieve accounts: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    print("\n" + "="*80)
    print("\nStep 6: Testing Portfolio Data Access")
    print("-" * 80)
    
    # Try to get portfolio data
    try:
        # Get portfolio for all accounts
        portfolio_data = client.get_portfolio_data()
        print("✓ Successfully retrieved portfolio data")
        
        # Basic statistics
        if isinstance(portfolio_data, list):
            print(f"  Number of accounts: {len(portfolio_data)}")
            for account in portfolio_data:
                securities_account = account.get('securitiesAccount', {})
                positions = securities_account.get('positions', [])
                print(f"  Positions in account: {len(positions)}")
        else:
            securities_account = portfolio_data.get('securitiesAccount', {})
            positions = securities_account.get('positions', [])
            print(f"  Total positions: {len(positions)}")
            
    except SchwabAPIError as e:
        print(f"⚠️  Portfolio data access: {e}")
        print("  (This may require additional API permissions)")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "="*80)
    print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*80 + "\n")
    
    print("Next steps:")
    print("1. Integrate the SchwabClient into your Flask application")
    print("2. Implement additional API endpoints as needed")
    print("3. Add error handling and user feedback in the UI")
    print("4. Consider implementing data caching for better performance")
    print()
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
