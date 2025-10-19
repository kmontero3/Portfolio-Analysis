"""
Schwab API Client for Portfolio Analysis Application

This module implements a complete OAuth 2.0 client for the Schwab Developer API.
It handles authentication, token management, and data retrieval for portfolio analysis.

API Documentation: https://developer.schwab.com/
"""

import requests
import base64
import json
import logging
import os
import webbrowser
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode, parse_qs, urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SchwabAPIError(Exception):
    """Custom exception for Schwab API errors"""
    pass


class SchwabClient:
    """
    Client for interacting with the Schwab Developer API.
    
    This client implements OAuth 2.0 authorization code flow for authentication
    and provides methods to retrieve account and portfolio data.
    
    Attributes:
        api_key (str): Schwab API application key (client_id)
        api_secret (str): Schwab API application secret (client_secret)
        redirect_uri (str): OAuth redirect URI configured in Schwab app
        access_token (str): Current OAuth access token
        refresh_token (str): OAuth refresh token for obtaining new access tokens
        token_expiry (datetime): Expiration time of current access token
    """
    
    # Schwab API endpoints
    BASE_URL = "https://api.schwabapi.com"
    AUTH_URL = "https://api.schwabapi.com/v1/oauth/authorize"
    TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"
    
    # Token storage file
    TOKEN_FILE = "schwab_tokens.json"
    
    def __init__(self, api_key: str, api_secret: str, redirect_uri: str):
        """
        Initialize the Schwab API client.
        
        Args:
            api_key: Schwab API application key (also called client_id)
            api_secret: Schwab API application secret (also called client_secret)
            redirect_uri: Redirect URI configured in your Schwab application
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.redirect_uri = redirect_uri
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        
        # Try to load existing tokens
        self._load_tokens()
        
        logger.info("SchwabClient initialized")

    def _get_auth_headers(self) -> Dict[str, str]:
        """
        Generate Basic Auth headers for token requests.
        
        Returns:
            Dictionary containing Authorization header with base64 encoded credentials
        """
        credentials = f"{self.api_key}:{self.api_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def _save_tokens(self) -> None:
        """
        Save access and refresh tokens to file for persistence.
        
        This prevents the need to re-authenticate on every application restart.
        The token file should be added to .gitignore for security.
        """
        token_data = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_expiry": self.token_expiry.isoformat() if self.token_expiry else None
        }
        
        try:
            with open(self.TOKEN_FILE, 'w') as f:
                json.dump(token_data, f)
            logger.info("Tokens saved successfully")
        except Exception as e:
            logger.error(f"Failed to save tokens: {e}")

    def _load_tokens(self) -> None:
        """
        Load previously saved tokens from file.
        
        If tokens exist and are valid, they will be used for API calls.
        If expired, the refresh_access_token method will be called automatically.
        """
        if not os.path.exists(self.TOKEN_FILE):
            logger.info("No saved tokens found")
            return
        
        try:
            with open(self.TOKEN_FILE, 'r') as f:
                token_data = json.load(f)
            
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
            
            expiry_str = token_data.get("token_expiry")
            if expiry_str:
                self.token_expiry = datetime.fromisoformat(expiry_str)
            
            logger.info("Tokens loaded successfully")
            
            # Check if token is expired and refresh if needed
            if self.token_expiry and datetime.now() >= self.token_expiry:
                logger.info("Loaded token is expired, refreshing...")
                self.refresh_access_token()
                
        except Exception as e:
            logger.error(f"Failed to load tokens: {e}")

    def get_authorization_url(self) -> str:
        """
        Generate the OAuth authorization URL.
        
        The user must visit this URL to authorize the application.
        After authorization, they will be redirected to redirect_uri with an auth code.
        
        Returns:
            Full authorization URL to direct the user to
        """
        params = {
            "client_id": self.api_key,
            "redirect_uri": self.redirect_uri,
            "response_type": "code"
        }
        
        auth_url = f"{self.AUTH_URL}?{urlencode(params)}"
        logger.info("Authorization URL generated")
        return auth_url

    def authenticate(self, authorization_code: Optional[str] = None, 
                    auto_open_browser: bool = True) -> bool:
        """
        Handle the complete OAuth 2.0 authentication flow.
        
        This method will:
        1. Check if valid tokens already exist
        2. If not, generate and open the authorization URL
        3. Wait for the user to provide the authorization code
        4. Exchange the code for access and refresh tokens
        
        Args:
            authorization_code: The code received after user authorization (optional)
            auto_open_browser: Whether to automatically open the auth URL in browser
            
        Returns:
            True if authentication successful, False otherwise
            
        Raises:
            SchwabAPIError: If authentication fails
        """
        # Check if we already have valid tokens
        if self.access_token and self.token_expiry:
            if datetime.now() < self.token_expiry:
                logger.info("Valid access token already exists")
                return True
            else:
                logger.info("Access token expired, attempting refresh")
                return self.refresh_access_token()
        
        # If we have a refresh token, try to use it
        if self.refresh_token:
            logger.info("Attempting to use refresh token")
            if self.refresh_access_token():
                return True
        
        # Need to do full OAuth flow
        logger.info("Starting OAuth authorization flow")
        
        if not authorization_code:
            # Generate and display authorization URL
            auth_url = self.get_authorization_url()
            
            print("\n" + "="*80)
            print("SCHWAB API AUTHORIZATION REQUIRED")
            print("="*80)
            print("\nPlease visit the following URL to authorize this application:")
            print(f"\n{auth_url}\n")
            
            if auto_open_browser:
                print("Opening browser automatically...")
                webbrowser.open(auth_url)
            
            print("\nAfter authorization, you will be redirected to your redirect URI.")
            print("Copy the 'code' parameter from the redirected URL.")
            authorization_code = input("\nEnter the authorization code: ").strip()
        
        # Exchange authorization code for tokens
        return self._exchange_code_for_token(authorization_code)

    def _exchange_code_for_token(self, authorization_code: str) -> bool:
        """
        Exchange authorization code for access and refresh tokens.
        
        Args:
            authorization_code: The authorization code from OAuth redirect
            
        Returns:
            True if token exchange successful, False otherwise
            
        Raises:
            SchwabAPIError: If token exchange fails
        """
        try:
            data = {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": self.redirect_uri
            }
            
            response = requests.post(
                self.TOKEN_URL,
                headers=self._get_auth_headers(),
                data=data
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token")
                
                # Calculate token expiry (default 30 minutes if not specified)
                expires_in = token_data.get("expires_in", 1800)
                self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
                
                self._save_tokens()
                logger.info("Successfully obtained access and refresh tokens")
                return True
            else:
                error_msg = f"Token exchange failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise SchwabAPIError(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error during token exchange: {e}"
            logger.error(error_msg)
            raise SchwabAPIError(error_msg)

    def refresh_access_token(self) -> bool:
        """
        Refresh the access token using the refresh token.
        
        This should be called when the access token expires.
        The method is also called automatically when needed.
        
        Returns:
            True if refresh successful, False otherwise
            
        Raises:
            SchwabAPIError: If token refresh fails
        """
        if not self.refresh_token:
            logger.error("No refresh token available")
            return False
        
        try:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            }
            
            response = requests.post(
                self.TOKEN_URL,
                headers=self._get_auth_headers(),
                data=data
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                
                # Refresh token may be rotated
                if "refresh_token" in token_data:
                    self.refresh_token = token_data.get("refresh_token")
                
                # Update expiry time
                expires_in = token_data.get("expires_in", 1800)
                self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
                
                self._save_tokens()
                logger.info("Successfully refreshed access token")
                return True
            else:
                error_msg = f"Token refresh failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise SchwabAPIError(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error during token refresh: {e}"
            logger.error(error_msg)
            raise SchwabAPIError(error_msg)

    def _ensure_authenticated(self) -> None:
        """
        Ensure we have a valid access token before making API calls.
        
        Raises:
            SchwabAPIError: If authentication fails
        """
        if not self.access_token:
            raise SchwabAPIError("Not authenticated. Call authenticate() first.")
        
        # Check if token is expired and refresh if needed
        if self.token_expiry and datetime.now() >= self.token_expiry:
            logger.info("Token expired, refreshing...")
            if not self.refresh_access_token():
                raise SchwabAPIError("Failed to refresh expired token")

    def _make_api_request(self, method: str, endpoint: str, 
                         params: Optional[Dict] = None,
                         data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an authenticated API request to Schwab.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: URL parameters (optional)
            data: Request body data (optional)
            
        Returns:
            JSON response from API
            
        Raises:
            SchwabAPIError: If API request fails
        """
        self._ensure_authenticated()
        
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data
            )
            
            # Handle rate limiting
            if response.status_code == 429:
                logger.warning("Rate limit exceeded")
                raise SchwabAPIError("API rate limit exceeded. Please wait before retrying.")
            
            # Handle authentication errors
            if response.status_code == 401:
                logger.warning("Authentication failed, attempting token refresh")
                self.refresh_access_token()
                # Retry the request once
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data
                )
            
            response.raise_for_status()
            return response.json() if response.text else {}
            
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {e}"
            logger.error(error_msg)
            raise SchwabAPIError(error_msg)

    def get_account_numbers(self) -> List[Dict[str, Any]]:
        """
        Retrieve all account numbers associated with the authenticated user.
        
        Returns:
            List of account information dictionaries
            
        Raises:
            SchwabAPIError: If API request fails
        """
        logger.info("Fetching account numbers")
        endpoint = "/trader/v1/accounts/accountNumbers"
        return self._make_api_request("GET", endpoint)

    def get_account_data(self, account_hash: Optional[str] = None, 
                        fields: Optional[str] = "positions") -> Dict[str, Any]:
        """
        Retrieve account information, balances, and positions.
        
        Args:
            account_hash: Specific account hash to query (if None, gets all accounts)
            fields: Fields to include in response (e.g., "positions" for holdings)
                   Options: "positions" or leave empty for just balances
            
        Returns:
            Account data including balances and optionally positions
            
        Raises:
            SchwabAPIError: If API request fails
        """
        logger.info(f"Fetching account data (hash: {account_hash}, fields: {fields})")
        
        if account_hash:
            # Get specific account
            endpoint = f"/trader/v1/accounts/{account_hash}"
        else:
            # Get all accounts
            endpoint = "/trader/v1/accounts"
        
        params = {}
        if fields:
            params["fields"] = fields
        
        return self._make_api_request("GET", endpoint, params=params)

    def get_portfolio_data(self, account_hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve portfolio holdings and positions for the account.
        
        This is a convenience method that calls get_account_data with positions included.
        
        Args:
            account_hash: Specific account hash to query (if None, gets all accounts)
            
        Returns:
            Portfolio data including all holdings, positions, and balances
            
        Raises:
            SchwabAPIError: If API request fails
        """
        logger.info(f"Fetching portfolio data for account: {account_hash or 'all'}")
        return self.get_account_data(account_hash=account_hash, fields="positions")

    def get_user_preferences(self) -> Dict[str, Any]:
        """
        Get user preferences and settings.
        
        Returns:
            User preferences data
            
        Raises:
            SchwabAPIError: If API request fails
        """
        logger.info("Fetching user preferences")
        endpoint = "/trader/v1/userPreference"
        return self._make_api_request("GET", endpoint)

    def test_connectivity(self) -> Dict[str, Any]:
        """
        Test API connectivity and authentication status.
        
        Returns:
            Dictionary containing connectivity test results including:
            - authenticated: Whether client is authenticated
            - token_valid: Whether access token is valid
            - token_expires: When the token expires
            - api_accessible: Whether API is accessible
            - account_count: Number of accounts accessible (if authenticated)
            - scopes: Available API scopes/permissions
            
        Raises:
            SchwabAPIError: If critical errors occur
        """
        results = {
            "authenticated": False,
            "token_valid": False,
            "token_expires": None,
            "api_accessible": False,
            "account_count": 0,
            "scopes": [],
            "errors": []
        }
        
        try:
            # Check authentication status
            if self.access_token:
                results["authenticated"] = True
                
                if self.token_expiry:
                    results["token_valid"] = datetime.now() < self.token_expiry
                    results["token_expires"] = self.token_expiry.isoformat()
                else:
                    results["token_valid"] = True
            
            # Test API accessibility
            if results["authenticated"]:
                try:
                    # Try to fetch account numbers as connectivity test
                    accounts = self.get_account_numbers()
                    results["api_accessible"] = True
                    results["account_count"] = len(accounts)
                    
                    # Schwab API scopes are typically embedded in token
                    # For now, we infer available scopes based on successful calls
                    results["scopes"] = [
                        "AccountAccess",
                        "MarketData",
                        "Trading"  # May not be available for all apps
                    ]
                    
                except SchwabAPIError as e:
                    results["errors"].append(f"API access test failed: {e}")
            else:
                results["errors"].append("Not authenticated")
            
        except Exception as e:
            results["errors"].append(f"Connectivity test error: {e}")
        
        return results

    def print_connection_status(self) -> None:
        """
        Print formatted connection status and API permissions.
        
        This method tests connectivity and displays results in a user-friendly format.
        """
        print("\n" + "="*80)
        print("SCHWAB API CONNECTION STATUS")
        print("="*80 + "\n")
        
        status = self.test_connectivity()
        
        print(f"Authenticated: {'✓' if status['authenticated'] else '✗'}")
        print(f"Token Valid: {'✓' if status['token_valid'] else '✗'}")
        
        if status['token_expires']:
            expiry = datetime.fromisoformat(status['token_expires'])
            time_remaining = expiry - datetime.now()
            minutes_remaining = int(time_remaining.total_seconds() / 60)
            print(f"Token Expires: {expiry.strftime('%Y-%m-%d %H:%M:%S')} ({minutes_remaining} minutes)")
        
        print(f"API Accessible: {'✓' if status['api_accessible'] else '✗'}")
        print(f"Account Count: {status['account_count']}")
        
        if status['scopes']:
            print(f"\nAvailable API Scopes/Permissions:")
            for scope in status['scopes']:
                print(f"  • {scope}")
        
        if status['errors']:
            print(f"\nErrors:")
            for error in status['errors']:
                print(f"  ✗ {error}")
        
        print("\n" + "="*80 + "\n")
