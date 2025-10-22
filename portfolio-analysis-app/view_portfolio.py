"""
Quick portfolio summary viewer
"""
import json
from pathlib import Path

data_dir = Path("data/schwab")
account_file = data_dir / "account_17857716.json"

with open(account_file) as f:
    data = json.load(f)

account = data["securitiesAccount"]
balances = account["currentBalances"]

print("\n" + "="*70)
print("📊 PORTFOLIO SUMMARY")
print("="*70)
print(f"\nAccount Number: {account['accountNumber']}")
print(f"Account Type: {account['type']}")
print(f"\n💰 Account Value: ${balances['liquidationValue']:,.2f}")
print(f"   Cash Balance: ${balances['cashBalance']:,.2f}")
print(f"   Buying Power: ${balances['buyingPower']:,.2f}")

positions = account.get("positions", [])
print(f"\n📈 Positions: {len(positions)}")
print("\n" + "-"*70)

for pos in positions:
    instrument = pos["instrument"]
    symbol = instrument.get("symbol", "N/A")
    qty = pos.get("longQuantity", 0)
    market_value = pos.get("marketValue", 0)
    
    print(f"  {symbol:10} | Qty: {qty:>8.2f} | Value: ${market_value:>12,.2f}")

print("="*70 + "\n")
