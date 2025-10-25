import requests
import json
import random


api_key = "e710fb6636d68f42e81ba638ea314131"


def create_account(api_url, account_data):
    headers = {
        'Content-Type': 'application/json'
    }

    print(account_data)
    
    response = requests.post(url=api_url, headers=headers, data=json.dumps(account_data))

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def generate_random_account_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])

def generate_random_balance():
    return random.randint(1000, 100000)  # Balance entre 1,000 y 100,000

def generate_random_rewards():
    return random.randint(0, 100)  # Recompensas entre 0 y 100

def main():
    # Cargar los datos de los clientes desde el archivo JSON
    with open('./RESPONSE/CreatedCustomers.json') as f:
        customers = json.load(f)

    for customer in customers:
        customer_id = customer['objectCreated']['_id']
        api_url_template = "http://api.nessieisreal.com/customers/{}/accounts?key={}".format(customer_id,api_key)
        # Crear cuentas para cada cliente
        savings_account_data = {
            "type": "Savings",
            "nickname": "Bank of Nessie",
            "rewards": 0,
            "balance": generate_random_balance(),
            "account_number": generate_random_account_number() 
        }
        
        credit_card_account_data = {
            "type": "Credit Card",
            "nickname": "SNOOPY BANK",
            "rewards": generate_random_rewards(),
            "balance": generate_random_balance(),
            "account_number": generate_random_account_number()
        }

        try:
            savings_api_url = api_url_template.format(customer_id)
            response_saving = create_account(api_url=savings_api_url, account_data=savings_account_data)
            print(f"Savings account created for {customer['objectCreated']['first_name']}")

            response_credit = create_account(api_url=savings_api_url, account_data=credit_card_account_data)
            print(f"Credit Card account created for {customer['objectCreated']['first_name']}")

            with open('./RESPONSE/CreatedAccounts.json', 'a') as outfile:
                json.dump(response_saving, outfile)
                outfile.write('\n')
                json.dump(response_credit, outfile)
                outfile.write('\n')

        except requests.exceptions.RequestException as e:
            print(f"An error occurred for {customer['objectCreated']['first_name']}: {e}")

if __name__ == "__main__":
    main()