# 🚀 End-to-End E-Commerce Data Pipeline (GraphQL, Python & DuckDB)

An enterprise-grade, modern data engineering pipeline that simulates extracting transactional e-commerce data from a custom **FastAPI GraphQL microservice**, transforming and flattening it, and loading it into a local **DuckDB analytical data warehouse** for high-performance OLAP queries.

---

## 🎯 The Problem You Are Solving

In modern software architecture, application backends and analytical warehouses speak two completely different languages:

1. **The Application Layer (GraphQL):** Frontend applications and microservices expose data as **nested, hierarchical graphs** (e.g., Orders containing nested Line Items containing nested Product objects). While efficient for UI consumption, these nested structures are notoriously difficult to query directly for business intelligence or machine learning.
2. **The Analytical Layer (DuckDB / Data Warehouses):** Analytics teams require **flat, normalized relational tables** (Star Schemas, Fact, and Dimension tables) optimized for columnar storage and vectorized SQL aggregations.

**The Solution:** This pipeline bridges the gap by programmatically consuming a GraphQL API, flattening complex multi-level JSON graphs into clean tabular structures, and loading them into a high-performance local data warehouse to execute fast, multi-table analytical queries.

---

## 🧠 Core Skills & Competencies Demonstrated

By building and executing this project, you demonstrate mastery across several pillars of modern data engineering:

* **API & Microservice Design:** Building asynchronous Python microservices using **FastAPI** and **Strawberry GraphQL** to serve typed, queryable data schemas.
* **Extraction & Ingestion (E):** Writing robust Python extraction scripts (`requests`) with error handling, status validation, and automated local landing zones (`raw_retail_orders.json`).
* **Transformation & Flattening (T):** Using **Pandas** to cleanse messy raw inputs (handling missing values, type casting, datetime parsing) and restructuring nested hierarchies into tabular analytical formats.
* **Analytical Storage & OLAP Warehousing (L):** Utilizing **DuckDB** as a high-performance embedded analytical database to execute lightning-fast SQL joins, aggregations, and revenue analysis.
* **Pipeline Orchestration:** Designing a master orchestration script (`main.py`) to manage sequential execution phases, error aborts, and end-to-end monitoring.

---

## 🏗️ Architecture & Data Flow

```text
[ Kaggle Dataset (UCI Online Retail CSV) ] 
       │ (Loaded on Startup)
       ▼
[ FastAPI + Strawberry GraphQL Microservice ] 
       │ (Targeted GraphQL Queries)
       ▼
[ Python Extractor (`extractor.py`) ] 
       │ (JSON Landing Zone)
       ▼
[ Python Transformer (`transformer.py`) ] 
       │ (Schema Flattening & Line Total Calculations)
       ▼
[ DuckDB Analytical Warehouse (`warehouse.duckdb`) ] 
       │ (Vectorized SQL Aggregations & Revenue Analytics)
       ▼
[ Automation Orchestrator (`main.py`) ]
```
---

## 🛠️ Tech Stack

Language: Python 3.10+

API Framework: FastAPI, Strawberry GraphQL, Uvicorn

Data Manipulation: Pandas, NumPy

Analytical Database: DuckDB (Embedded OLAP)

Dataset: UCI Online Retail (Kaggle)

Orchestration: Python Custom Runner

---

## 📁 Project Structure
```text
graphql-de-pipeline/
│
├── data/
│   ├── online_retail.csv           # Raw source dataset (Kaggle)
│   ├── raw_retail_orders.json      # Extracted landing zone data
│   └── warehouse.duckdb            # Local DuckDB analytical database
│
├── src/
│   ├── server.py                   # FastAPI + Strawberry GraphQL microservice
│   ├── extractor.py                # Programmatic GraphQL data extraction script
│   ├── transformer.py              # Data cleansing, structuring, and warehouse loader
│   └── main.py                     # Master automation orchestration runner
│
├── requirements.txt                # Project dependencies
└── README.md                       # Project documentation
```


---

## ⚙️ How to Run Locally

**1. Clone & Set Up Environment**
```text
Bash
git clone [https://github.com/shettyniharika/graphql-de-pipeline.git](https://github.com/shettyniharika/graphql-de-pipeline.git)
cd graphql-de-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


**2. Start the GraphQL Microservice (Terminal Tab 1)**
```text
Bash
python src/server.py
```


**3. Run the Full End-to-End Pipeline (Terminal Tab 2)**
```text
Bash
python src/main.py
```
