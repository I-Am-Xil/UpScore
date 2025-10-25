import requests
import json

api_key = "e710fb6636d68f42e81ba638ea314131"
api_url = "http://api.nessieisreal.com/merchants?key={}".format(api_key)


def create_merchant(api_url, api_key, merchant_data):
    headers = {
        'Content-Type': 'application/json'
    }

    print(merchant_data)
    
    response = requests.post(url=api_url, headers=headers, data=json.dumps(merchant_data))

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def main():

    merchant_data = {
        "name": "TEST MERCHANT",
        "category": "RETAIL",
        "address":{
            "street_number": "1234",
            "street_name": "MERCHANT STREET",
            "city": "MERCHANT CITY",
            "state": "MC",
            "zip": "12345"
        },
        "geocode": {
            "lat": 0,
            "lng": 0
        }
    }

    try:
        merchant = create_merchant(api_url=api_url, api_key=api_key, merchant_data=merchant_data)
        print("Merchant created successfully:")
        print(json.dumps(merchant, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    main()