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

# Calculate date range (2 months ago to current date)
end_date = datetime.strptime("2025-10-25", "%Y-%m-%d")
start_date = end_date - timedelta(days=60)

def random_date(start, end):
    time_between = end - start
    days_between = time_between.days
    random_days = random.randint(0, days_between)
    return start + timedelta(days=random_days)

# Create withdrawals for each savings account
all_withdrawals = []

for account_id in savings_accounts:
    # Create at least 2 withdrawals for each account
    num_withdrawals = random.randint(2, 4)  # Random number between 2 and 4 withdrawals
    
    for _ in range(num_withdrawals):
        # Generate random date
        transaction_date = random_date(start_date, end_date)
        
        withdrawal_data = {
            "medium": "balance",
            "transaction_date": transaction_date.strftime("%Y-%m-%d"),
            "status": "completed",
            "amount": random.randint(1000, 20000),
            "description": "Withdrawal"
        }
        
        # Make API request
        url = f"http://api.nessieisreal.com/accounts/{account_id}/withdrawals?key={api_key}"
        response = requests.post(url, json=withdrawal_data)
        
        # Store response
        if response.status_code == 201:
            withdrawal_response = response.json()
            all_withdrawals.append({
                "account_id": account_id,
                "withdrawal": withdrawal_response
            })
            print(f"Created withdrawal for account {account_id} on {withdrawal_data['transaction_date']}")
        else:
            print(f"Failed to create withdrawal for account {account_id} on {withdrawal_data['transaction_date']}: {response.text}")

# Save all withdrawals to a file
with open('RESPONSE/CreatedWithdrawals.json', 'w') as file:
    json.dump(all_withdrawals, file, indent=2)

print("\nWithdrawal creation completed. Results saved to CreatedWithdrawals.json")