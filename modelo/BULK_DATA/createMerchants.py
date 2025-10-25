import requests
import json
import random

api_key = "e710fb6636d68f42e81ba638ea314131"
api_url = "http://api.nessieisreal.com/merchants?key={}".format(api_key)

def create_merchant(api_url, merchant_data):
    headers = {
        'Content-Type': 'application/json'
    }

    print(merchant_data)
    
    response = requests.post(url=api_url, headers=headers, data=json.dumps(merchant_data))

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def generate_random_merchant_data():
    categories = ["RETAIL", "FOOD", "SERVICES", "TECH", "HEALTH", "ENTERTAINMENT", "TRAVEL", "EDUCATION", "AUTOMOTIVE", "REAL ESTATE"]
    merchant_name = f"Merchant {random.randint(1, 1000)}"
    category = random.choice(categories)
    
    address = {
        "street_number": str(random.randint(1000, 9999)),
        "street_name": f"{random.choice(['Main', 'Second', 'Third', 'Fourth'])} Street",
        "city": f"City {random.randint(1, 100)}",
        "state": f"{random.choice(['AB', 'BC', 'CD', 'DE', 'EF'])}",
        "zip": str(random.randint(10000, 99999))
    }

    geocode = {
        "lat": round(random.uniform(-90, 90), 6),
        "lng": round(random.uniform(-180, 180), 6)
    }

    return {
        "name": merchant_name,
        "category": category,
        "address": address,
        "geocode": geocode
    }

def main():
    for _ in range(10):  # Crear 10 comerciantes
        merchant_data = generate_random_merchant_data()
        try:
            merchant = create_merchant(api_url=api_url, merchant_data=merchant_data)
            with open('./RESPONSE/CreatedMerchants.json', 'a') as f:
                json.dump(merchant, f)
                f.write('\n')
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()