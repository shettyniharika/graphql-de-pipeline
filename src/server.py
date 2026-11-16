import pandas as pd
import uvicorn
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional

# Load and clean the CSV dataset on startup
CSV_PATH = "data/online_retail.csv"
print(f"Loading dataset from {CSV_PATH}...")

try:
    # Read the CSV (handling potential encoding issues common with UCI datasets)
    df = pd.read_csv(CSV_PATH, encoding="ISO-8859-1")
    
    # Clean up column names and drop rows with missing CustomerIDs or descriptions
    df = df.dropna(subset=['CustomerID', 'Description'])
    df['CustomerID'] = df['CustomerID'].astype(int).astype(str)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Limit to first 5,000 rows for fast local execution and query performance
    df = df.head(5000)
    print(f"Successfully loaded {len(df)} rows from online_retail.csv!")
except Exception as e:
    print(f"Error loading CSV: {e}")
    df = pd.DataFrame()

# Define GraphQL Types based on the UCI Retail Schema
@strawberry.type
class RetailItem:
    invoice_no: str
    stock_code: str
    description: str
    quantity: int
    invoice_date: str
    unit_price: float
    customer_id: str
    country: str

@strawberry.type
class Query:
    @strawberry.field
    def retail_transactions(self, limit: int = 50, country: Optional[str] = None) -> List[RetailItem]:
        global df
        if df.empty:
            return []
        
        filtered_df = df
        if country:
            filtered_df = df[df['Country'].str.lower() == country.lower()]
            
        limited_df = filtered_df.head(limit)
        
        results = []
        for _, row in limited_df.iterrows():
            results.append(RetailItem(
                invoice_no=str(row['InvoiceNo']),
                stock_code=str(row['StockCode']),
                description=str(row['Description']),
                quantity=int(row['Quantity']),
                invoice_date=str(row['InvoiceDate']),
                unit_price=float(row['UnitPrice']),
                customer_id=str(row['CustomerID']),
                country=str(row['Country'])
            ))
        return results

schema = strawberry.Schema(query=Query)
app = FastAPI(title="UCI Online Retail GraphQL API")
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)