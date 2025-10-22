"""
Get encrypted account hash from Schwab
"""
import json
import requests

with open('schwab_tokens.json') as f:
    tokens = json.load(f)

access_token = tokens['access_token']

url = "https://api.schwabapi.com/trader/v1/accounts/accountNumbers"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json"
}

print("Fetching account numbers (encrypted hashes)...")
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"\nResponse: {json.dumps(data, indent=2)}")
    
    # Save it
    with open('data/schwab/account_hashes.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("\n✓ Saved to data/schwab/account_hashes.json")
else:
    print(f"Error: {response.text}")
