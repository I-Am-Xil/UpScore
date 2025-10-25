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

    with open('./CustomersBulk.json', 'r') as file:
        customer_data = json.load(file)
        
        for i in customer_data:
            try:
                customer = create_customer(api_url=api_url, api_key=api_key, customer_data=i)
                print("Customer created successfully:")
                with open('./RESPONSE/CreatedCustomers.json', 'a') as outfile:
                    json.dump(customer, outfile)
                    outfile.write('\n')
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

    # try:
    #     customer = create_customer(api_url=api_url, api_key=api_key, customer_data=customer_data)
    #     print("Customer created successfully:")
    #     print(json.dumps(customer, indent=4))
    # except requests.exceptions.RequestException as e:
    #     print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

#print(api_url)