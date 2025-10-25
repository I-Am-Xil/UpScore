import json
import random
import requests
from datetime import datetime, timedelta

# API Key
api_key = "e710fb6636d68f42e81ba638ea314131"

# Load accounts data
with open('RESPONSE/CreatedAccounts.json', 'r') as file:
    accounts_data = json.load(file)

# Filter Savings accounts
savings_accounts = [account["objectCreated"]["_id"] for account in accounts_data 
                   if account["objectCreated"]["type"] == "Savings"]

# Get current date and calculate next biweekly date
current_date = datetime.strptime("2025-10-25", "%Y-%m-%d")
next_biweekly = current_date + timedelta(days=15)

# Format dates
current_date_str = current_date.strftime("%Y-%m-%d")
next_biweekly_str = next_biweekly.strftime("%Y-%m-%d")

# Create deposits for each savings account
all_deposits = []

for account_id in savings_accounts:
    # Create two deposits for each account
    for date in [current_date_str, next_biweekly_str]:
        deposit_data = {
            "medium": "balance",
            "transaction_date": date,
            "status": "completed",
            "amount": random.randint(1000, 50000),
            "description": "Biweekly Pay"
        }
        
        # Make API request
        url = f"http://api.nessieisreal.com/accounts/{account_id}/deposits?key={api_key}"
        response = requests.post(url, json=deposit_data)
        
        # Store response
        if response.status_code == 201:
            deposit_response = response.json()
            all_deposits.append({
                "account_id": account_id,
                "deposit": deposit_response
            })
            print(f"Created deposit for account {account_id} on {date}")
        else:
            print(f"Failed to create deposit for account {account_id} on {date}: {response.text}")

# Save all deposits to a file
with open('RESPONSE/CreatedDeposits.json', 'w') as file:
    json.dump(all_deposits, file, indent=2)

print("\nDeposit creation completed. Results saved to CreatedDeposits.json")