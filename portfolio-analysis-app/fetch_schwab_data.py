"""
Schwab API Data Fetcher

This script fetches data from the Schwab API and saves it to JSON files
for offline testing and development.

Endpoints implemented:
- /accounts - Get all accounts with positions
- /accounts/accountNumbers - Get account hashes
- /accounts/{accountNumber}/orders - Get all orders (recursive, 1 year per call)

Usage:
    python fetch_schwab_data.py
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import time

from app.blueprints.api.schwab_integration import SchwabClient, SchwabAPIError
from config import Config


class SchwabDataFetcher:
    """Fetches and saves Schwab API data to JSON files"""
    
    def __init__(self, output_dir: str = "data/schwab"):
        """
        Initialize the data fetcher.
        
        Args:
            output_dir: Directory to save JSON files (default: data/schwab)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Schwab client
        self.client = SchwabClient(
            api_key=Config.SCHWAB_API_KEY,
            api_secret=Config.SCHWAB_API_SECRET,
            redirect_uri=Config.SCHWAB_REDIRECT_URI
        )
        
        print(f"📁 Output directory: {self.output_dir.absolute()}")
    
    def save_json(self, filename: str, data: Any) -> None:
        """
        Save data to a JSON file with pretty formatting.
        
        Args:
            filename: Name of the file (will be saved in output_dir)
            data: Data to save (dict or list)
        """
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"  ✓ Saved: {filename}")
    
    def fetch_account_numbers(self) -> List[Dict[str, Any]]:
        """
        Fetch all account numbers and their encrypted hashes.
        
        Returns:
            List of account information dictionaries with accountNumber and hashValue
        """
        print("\n📊 Fetching account numbers...")
        
        try:
            # Use the accountNumbers endpoint which returns encrypted hashes
            # This endpoint requires direct API call
            endpoint = "/trader/v1/accounts/accountNumbers"
            accounts = self.client._make_api_request("GET", endpoint)
            
            # Save to JSON
            self.save_json("account_numbers.json", accounts)
            
            print(f"  Found {len(accounts)} account(s)")
            return accounts
            
        except SchwabAPIError as e:
            print(f"  ❌ Error fetching account numbers: {e}")
            return []
    
    def fetch_accounts_data(self) -> List[Dict[str, Any]]:
        """
        Fetch detailed account data including positions for all accounts.
        
        Returns:
            List of account data dictionaries
        """
        print("\n📊 Fetching detailed account data (with positions)...")
        
        try:
            # Get all accounts with positions
            accounts_data = self.client.get_account_data(fields="positions")
            
            # Save to JSON
            self.save_json("accounts.json", accounts_data)
            
            # If multiple accounts, also save individual account files
            if isinstance(accounts_data, list):
                print(f"  Found {len(accounts_data)} account(s)")
                
                for i, account in enumerate(accounts_data, 1):
                    account_hash = account.get('securitiesAccount', {}).get('accountNumber', f'account_{i}')
                    self.save_json(f"account_{account_hash}.json", account)
            else:
                print("  Found 1 account")
            
            return accounts_data if isinstance(accounts_data, list) else [accounts_data]
            
        except SchwabAPIError as e:
            print(f"  ❌ Error fetching accounts data: {e}")
            return []
    
    def fetch_orders_for_account(
        self, 
        account_hash: str, 
        from_date: datetime = None,
        to_date: datetime = None,
        max_results: int = 3000
    ) -> List[Dict[str, Any]]:
        """
        Fetch orders for a specific account within a date range.
        
        Args:
            account_hash: Encrypted account hash identifier (from accountNumbers endpoint)
            from_date: Start date (default: 1 year ago)
            to_date: End date (default: today)
            max_results: Maximum results per API call (default: 3000)
            
        Returns:
            List of order dictionaries
        """
        # Default to last year if not specified
        if to_date is None:
            to_date = datetime.now()
        if from_date is None:
            from_date = to_date - timedelta(days=365)
        
        # Use the encrypted hash in the endpoint
        endpoint = f"/trader/v1/accounts/{account_hash}/orders"
        
        params = {
            "fromEnteredTime": from_date.strftime("%Y-%m-%dT00:00:00.000Z"),
            "toEnteredTime": to_date.strftime("%Y-%m-%dT23:59:59.999Z"),
            "maxResults": max_results
        }
        
        try:
            orders = self.client._make_api_request("GET", endpoint, params=params)
            return orders if isinstance(orders, list) else []
        except SchwabAPIError as e:
            print(f"    ⚠️  Error fetching orders for date range: {e}")
            return []
    
    def fetch_all_orders_for_account(
        self, 
        account_hash: str,
        account_number: str,
        years_back: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Recursively fetch all orders for an account, going back specified years.
        Uses 1-year chunks to stay within API limits.
        
        Args:
            account_hash: Encrypted account hash identifier
            account_number: Plain account number (for display)
            years_back: How many years back to fetch (default: 10)
            
        Returns:
            List of all order dictionaries
        """
        print(f"\n📋 Fetching orders for account {account_number}...")
        print(f"  Retrieving up to {years_back} years of order history (1 year per API call)")
        
        all_orders = []
        end_date = datetime.now()
        
        for year in range(years_back):
            # Calculate date range (364 days to ensure it's less than 1 year)
            # Schwab API requires the range to be strictly less than 1 year
            to_date = end_date - timedelta(days=364 * year)
            from_date = to_date - timedelta(days=364)
            
            print(f"  📅 Fetching: {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}")
            
            # Fetch orders for this date range
            orders = self.fetch_orders_for_account(account_hash, from_date, to_date)
            
            if orders:
                all_orders.extend(orders)
                print(f"    ✓ Retrieved {len(orders)} order(s)")
            else:
                print(f"    • No orders in this period")
            
            # Rate limiting - be nice to the API
            time.sleep(0.5)
        
        print(f"  ✅ Total orders retrieved: {len(all_orders)}")
        return all_orders
    
    def fetch_all_orders(self, account_numbers: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch orders for all accounts.
        
        Args:
            account_numbers: List of account information with accountNumber and hashValue
            
        Returns:
            Dictionary mapping account_number to list of orders
        """
        all_orders_by_account = {}
        
        for account_info in account_numbers:
            account_number = account_info.get('accountNumber')
            account_hash = account_info.get('hashValue')
            
            if not account_number or not account_hash:
                print(f"  ⚠️  Skipping account - missing account number or hash")
                continue
            
            # Fetch all orders for this account (10 years back)
            orders = self.fetch_all_orders_for_account(
                account_hash=account_hash,
                account_number=account_number,
                years_back=10
            )
            
            if orders:
                all_orders_by_account[account_number] = orders
                
                # Save individual account orders
                self.save_json(f"orders_{account_number}.json", orders)
        
        # Save combined orders file
        self.save_json("all_orders.json", all_orders_by_account)
        
        return all_orders_by_account
    
    def fetch_all_data(self) -> None:
        """
        Main method to fetch all data from Schwab API.
        Orchestrates the entire data fetching process.
        """
        print("\n" + "="*70)
        print("🔄 SCHWAB DATA FETCHER")
        print("="*70)
        
        # Check authentication
        if not self.client.access_token:
            print("\n❌ Not authenticated!")
            print("Please run the Flask app and authenticate first:")
            print("  python app.py")
            print("  Then visit https://127.0.0.1:5000 and connect to Schwab")
            return
        
        print("\n✓ Authenticated with Schwab API")
        
        # Step 1: Fetch account numbers
        account_numbers = self.fetch_account_numbers()
        
        if not account_numbers:
            print("\n❌ No accounts found or error fetching accounts")
            return
        
        # Step 2: Fetch detailed account data
        accounts_data = self.fetch_accounts_data()
        
        # Step 3: Fetch all orders for all accounts
        all_orders = self.fetch_all_orders(account_numbers)
        
        # Summary
        print("\n" + "="*70)
        print("✅ DATA FETCH COMPLETE")
        print("="*70)
        print(f"\n📊 Summary:")
        print(f"  • Accounts: {len(account_numbers)}")
        
        total_orders = sum(len(orders) for orders in all_orders.values())
        print(f"  • Total Orders: {total_orders}")
        
        print(f"\n📁 All data saved to: {self.output_dir.absolute()}")
        print("\nFiles created:")
        for file in sorted(self.output_dir.glob("*.json")):
            size_kb = file.stat().st_size / 1024
            print(f"  • {file.name} ({size_kb:.1f} KB)")
        
        print("\n🎉 You can now use this data for offline testing!")
        print("="*70 + "\n")


def main():
    """Main entry point"""
    try:
        # Create fetcher instance
        fetcher = SchwabDataFetcher(output_dir="data/schwab")
        
        # Fetch all data
        fetcher.fetch_all_data()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Fetch interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
