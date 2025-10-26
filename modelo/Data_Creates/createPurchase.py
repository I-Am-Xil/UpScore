import requests
import json

api_key = "e710fb6636d68f42e81ba638ea314131"
api_url = "http://api.nessieisreal.com/accounts/68fd0f239683f20dd51a46a3/purchases?key={}".format(api_key)

def create_purchase(api_url, api_key, purchase_data):
    headers = {
        'Content-Type': 'application/json'
    }

    print(purchase_data)
    
    response = requests.post(url=api_url, headers=headers, data=json.dumps(purchase_data))

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def main():

    purchase_data = {
            "merchant_id": "68fd16569683f20dd51a46b0",
            "medium": "balance",
            "purchase_date": "2025-10-25",
            "amount": 5000,
            "status": "pending",
            "description": "TEST PURCHASE"
    }   

    try:
        purchase = create_purchase(api_url=api_url, api_key=api_key, purchase_data=purchase_data)
        print("Purchase created successfully:")
        print(json.dumps(purchase, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()