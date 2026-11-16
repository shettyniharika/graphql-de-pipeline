import sys
import os

# Ensure Python can locate modules inside the src folder
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from extractor import extract_retail_data
from transformer import transform_and_load_retail

def run_pipeline():
    print("==================================================")
    print("🚀 Starting E-Commerce GraphQL Data Pipeline Run")
    print("==================================================")
    
    # Step 1: Extraction Phase
    print("\n[Phase 1/2] Executing GraphQL Extractor...")
    extracted_data = extract_retail_data()
    
    if not extracted_data:
        print("\n❌ Pipeline failed during extraction phase! Aborting.")
        return

    # Step 2: Transformation & Warehouse Loading Phase
    print("\n[Phase 2/2] Executing Transformer & DuckDB Loader...")
    try:
        transform_and_load_retail()
    except Exception as e:
        print(f"\n❌ Pipeline failed during transformation phase: {e}")
        return

    print("\n==================================================")
    print("🎉 E-Commerce Pipeline Completed Successfully!")
    print("==================================================")

if __name__ == "__main__":
    run_pipeline()