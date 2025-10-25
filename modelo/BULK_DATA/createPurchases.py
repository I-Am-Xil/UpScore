import requests
import json
import random
from datetime import datetime, timedelta

api_key = "e710fb6636d68f42e81ba638ea314131"


def create_purchase(api_url, purchase_data):
    headers = {
        'Content-Type': 'application/json'
    }

    print(purchase_data)
    
    response = requests.post(url=api_url, headers=headers, data=json.dumps(purchase_data))

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def generate_random_purchase_data(merchant_ids):

    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    random_date = start_date + (end_date - start_date) * random.random()

    return {
        "merchant_id": random.choice(merchant_ids),
        "medium": "balance",
        "purchase_date": random_date.strftime("%Y-%m-%d"),
        "amount": random.randint(1000, 10000),  # Monto entre 1,000 y 10,000
        "status": "pending",
        "description": "Random Purchase"
    }

def main():
    # Cargar los datos de las cuentas y comerciantes desde los archivos JSON
    with open('./RESPONSE/CreatedAccounts.json') as f:
        accounts = json.load(f)

    with open('./RESPONSE/CreatedMerchants.json') as f:
        merchants = json.load(f)

    merchant_ids = [merchant['objectCreated']['_id'] for merchant in merchants]

    for account in accounts:
        account_id = account['objectCreated']['_id']
        api_url_template = "http://api.nessieisreal.com/accounts/{}/purchases?key={}".format(account_id,api_key)
        for _ in range(5):  # Crear 5 compras por cuenta
            purchase_data = generate_random_purchase_data(merchant_ids)
            api_url = api_url_template.format(account_id)
            try:
                purchase = create_purchase(api_url=api_url, purchase_data=purchase_data)
                print("Purchase created successfully:")
                with open('./RESPONSE/CreatedPurchases.json', 'a') as outfile:
                    json.dump(purchase, outfile)
                    outfile.write('\n')
            except requests.exceptions.RequestException as e:
                print(f"An error occurred for account {account_id}: {e}")

if __name__ == "__main__":
    main()