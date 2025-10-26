import pandas as pd 
import json

def create_csv_from_json(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    # Normalize the JSON data to a flat table
    df = pd.json_normalize(data)
    
    # Save the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)
    print(f"CSV file '{csv_file}' created successfully.")

def join_csv_files(csv_file1, csv_file2, output_file):
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    
    # Merge the two DataFrames on the specified key
    merged_df = pd.merge(df1, df2, left_on='customer_id', right_on='_id', how='inner')
    
    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(f"./results_csv/{output_file}", index=False)
    print(f"Merged CSV file '{output_file}' created successfully.")

def main():
    create_csv_from_json('accounts.json', './results_csv/accounts.csv')
    create_csv_from_json('customers.json', './results_csv/customers.csv')

    join_csv_files('./results_csv/accounts.csv', './results_csv/customers.csv', 'all_base.csv')

if __name__ == "__main__":
    main()