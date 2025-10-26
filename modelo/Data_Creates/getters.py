import requests
import json

api_key = "e710fb6636d68f42e81ba638ea314131"



def get_accounts(api_url, headers):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        accounts = response.json()
        return accounts
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def write_accounts_to_file(accounts, filename='accounts.json'):
    with open(filename, 'w') as f:
        json.dump(accounts, f, indent=4)

# def get_customer_id(accounts):
#     if accounts and 'results' in accounts and len(accounts['results']) > 0:
#         return accounts['results'][0].get('customer_id')
#     return None

def get_customers(api_url, headers):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        customers = response.json()
        return customers
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def write_customers_to_file(customers, filename='customers.json'):
    with open(filename, 'w') as f:
        json.dump(customers, f, indent=4)

def get_purchases(api_url, headers):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        purchases = response.json()
        return purchases
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def main():

    api_url_acc = "http://api.nessieisreal.com/accounts/?key={}".format(api_key)
    api_url_cust = "http://api.nessieisreal.com/customers/?key={}".format(api_key)
    
    


    headers = {
        'Content-Type': 'application/json'
    }

    accounts = get_accounts(api_url=api_url_acc, headers=headers)
    customers = get_customers(api_url=api_url_cust, headers=headers)
    if accounts:
        print("Accounts retrieved successfully:")
        write_accounts_to_file(accounts)

    if customers:
        print("Customers retrieved successfully:")
        write_customers_to_file(customers)
    
    for i in range(len(accounts)):
      if accounts:
        print(accounts[i]['_ids'])



    


if __name__ == "__main__":
    main()