import json
import os
import pandas as pd
import duckdb

def transform_and_load_retail():
    json_path = "data/raw_retail_orders.json"
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Please run src/extractor.py first!")
        return

    print("Reading raw retail JSON data...")
    with open(json_path, "r") as f:
        records = json.load(f)

    if not records:
        print("No records found to transform.")
        return

    # Convert raw JSON records to a Pandas DataFrame
    df = pd.DataFrame(records)

    # Clean and rename columns to match clean database standards
    df = df.rename(columns={
        "invoiceNo": "invoice_no",
        "stockCode": "stock_code",
        "description": "description",
        "quantity": "quantity",
        "invoiceDate": "invoice_date",
        "unitPrice": "unit_price",
        "customerId": "customer_id",
        "country": "country"
    })

    # Calculate total line amount (quantity * unit_price)
    df["line_total"] = df["quantity"] * df["unit_price"]

    print(f"Transformed {len(df)} retail transaction records.")

    # --- Load into DuckDB (Local Data Warehouse) ---
    db_path = "data/warehouse.duckdb"
    print(f"Loading data into DuckDB warehouse at {db_path}...")
    
    conn = duckdb.connect(db_path)

    # Write table to DuckDB
    conn.execute("CREATE OR REPLACE TABLE fact_retail_sales AS SELECT * FROM df")

    # Run an analytical query on the real retail data
    print("\n--- Top Products by Total Sales Revenue (from DuckDB) ---")
    query_result = conn.execute("""
        SELECT 
            description,
            SUM(quantity) AS total_units_sold,
            ROUND(SUM(line_total), 2) AS total_revenue
        FROM fact_retail_sales
        GROUP BY description
        ORDER BY total_revenue DESC
        LIMIT 5;
    """).fetchdf()

    print(query_result)
    
    conn.close()
    print("\nRetail transformation and warehouse loading completed successfully!")

if __name__ == "__main__":
    transform_and_load_retail()