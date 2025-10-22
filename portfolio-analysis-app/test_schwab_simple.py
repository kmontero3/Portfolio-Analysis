"""
Simple test to check Schwab API with raw requests.
"""

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config

# Load tokens
with open('schwab_tokens.json', 'r') as f:
    tokens = json.load(f)

access_token = tokens['access_token']

print("=" * 70)
print("🔬 SCHWAB API RAW REQUEST TEST")
print("=" * 70)
print(f"\nAccess Token (first 20 chars): {access_token[:20]}...")
print(f"Token Expiry: {tokens['token_expiry']}")

import requests

# Test 1: Try to get a stock quote (often the most permissive endpoint)
print("\n" + "-" * 70)
print("Test 1: Get Stock Quote for AAPL")
print("-" * 70)

url = "https://api.schwabapi.com/marketdata/v1/quotes?symbols=AAPL"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text[:500]}")

# Test 2: Try accounts endpoint with different headers
print("\n" + "-" * 70)
print("Test 2: Accounts Endpoint")
print("-" * 70)

url = "https://api.schwabapi.com/trader/v1/accounts"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Response: {response.text}")

# Test 3: Try with market data endpoint
print("\n" + "-" * 70)
print("Test 3: Market Hours")
print("-" * 70)

url = "https://api.schwabapi.com/marketdata/v1/markets?markets=equity"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text[:500]}")

print("\n" + "=" * 70)
