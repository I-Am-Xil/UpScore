import requests
import pandas
import json


api_key = "e710fb6636d68f42e81ba638ea314131"
api_url = "http://api.nessieisreal.com/customers/?key={}".format(api_key)

def create_customer(api_url, api_key, customer_data):
    headers = {
        'Content-Type': 'application/json'
    }

    print(customer_data)
    
    response = requests.post(url=api_url, headers=headers, data=json.dumps(customer_data))

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()


def main():

    # first_name = input("Enter first name: ")
    # last_name = input("Enter last name: ")
    # street_number = input("Enter street number: ")
    # street_name = input("Enter street name: ")
    # city = input("Enter city: ")
    # state = input("Enter state: ")
    # zip_code = input("Enter zip code: ")    

    customer_data = {
        "first_name": "TEST",
        "last_name": "ONE",
        "address": {
            "street_number": "9999",
            "street_name": "TEST STREET",
            "city": "TEST CITY",
            "state": "TC",
            "zip": "99999"
        }
    }

    try:
        customer = create_customer(api_url=api_url, api_key=api_key, customer_data=customer_data)
        print("Customer created successfully:")
        print(json.dumps(customer, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

#print(api_url)