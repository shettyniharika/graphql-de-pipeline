import requests
import json
import os

GRAPHQL_URL = "http://127.0.0.1:8000/graphql"

# GraphQL Query targeting our real retail transactions
QUERY = """
{
  retailTransactions(limit: 100, country: "United Kingdom") {
    invoiceNo
    stockCode
    description
    quantity
    invoiceDate
    unitPrice
    customerId
    country
  }
}
"""

def extract_retail_data():
    print(f"Connecting to GraphQL endpoint at {GRAPHQL_URL}...")
    try:
        response = requests.post(GRAPHQL_URL, json={"query": QUERY})
        response.raise_for_status()
        
        result = response.json()
        
        if "errors" in result:
            print("GraphQL query returned errors:", result["errors"])
            return None
            
        transactions = result.get("data", {}).get("retailTransactions", [])
        print(f"Successfully extracted {len(transactions)} retail records from GraphQL API!")
        
        os.makedirs("data", exist_ok=True)
        output_path = "data/raw_retail_orders.json"
        with open(output_path, "w") as f:
            json.dump(transactions, f, indent=4)
            
        print(f"Raw data successfully saved to {output_path}")
        return transactions

    except requests.exceptions.ConnectionError:
        print("Failed to connect to the GraphQL server. Is it running? Start it using 'python src/server.py'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    extract_retail_data()