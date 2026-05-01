# 📊 E-Commerce Data Analysis & BI Dashboard
 
> An end-to-end data analytics pipeline using **Python**, **PostgreSQL**, and **Power BI** to analyze Brazilian e-commerce data and deliver actionable business insights through an interactive dashboard.
 
![Final Dashboard](screenshots/Final_report.png)
 
---
 
## 📌 Table of Contents
 
- [Project Overview](#-project-overview)
- [Business Objective](#-business-objective)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Phase 1: Data Loading](#-phase-1-data-loading-python)
- [Phase 2: Data Cleaning & Transformation](#-phase-2-data-cleaning--transformation)
- [Phase 3: Feature Engineering](#-phase-3-feature-engineering)
- [Phase 4: Database Setup (PostgreSQL)](#-phase-4-database-setup-postgresql)
- [Phase 5: Load Data into PostgreSQL](#-phase-5-load-data-into-postgresql)
- [Phase 6: SQL Validation & Analysis](#-phase-6-sql-validation--analysis)
- [Phase 7: Power BI Dashboard](#-phase-7-power-bi-dashboard)
- [Key Insights](#-key-insights)
- [Limitations & Future Work](#-limitations--future-work)
---
 
## 🚀 Project Overview
 
This project demonstrates a complete **data analytics workflow** applied to a real-world e-commerce dataset (Olist — Brazilian marketplace). The pipeline covers everything from raw CSV ingestion to a business-ready Power BI dashboard, with PostgreSQL serving as the analytical data store.
 
The project analyzes:
- 📦 Customer purchasing behavior
- 💰 Revenue trends over time
- 🚚 Delivery performance metrics
- 🗺️ Regional distribution of orders
---
 
## 🏢 Business Objective
 
The goal is to equip business stakeholders with clear, data-driven answers to:
 
| Question | Metric |
|----------|--------|
| How is revenue trending? | Monthly revenue chart |
| Where are our customers? | Orders by state / map |
| How fast do we deliver? | Average delivery time (days) |
| Are customers returning? | Repeat vs. one-time buyer analysis |
 
---
 
## 🛠️ Tech Stack
 
| Tool | Purpose |
|------|---------|
| **Python (Pandas, SQLAlchemy)** | Data ingestion, cleaning, transformation |
| **PostgreSQL** | Relational data store & SQL analysis |
| **SQL** | Validation queries & analytical reporting |
| **Power BI** | Interactive business dashboard |
| **VS Code** | Development environment |
 
---
 
## 📁 Project Structure
 
```
ecommerce-data-project/
│
├── data/
│   ├── raw/                         # Original CSV datasets
│   └── processed/                   # Cleaned & transformed data
│
├── src/
│   ├── load_data.py                 # Data ingestion script
│   └── load_to_db.py                # PostgreSQL loading script
│
├── screenshots/                     # Step-by-step process screenshots
│   ├── data_load.png
│   ├── data_load_executed.png
│   ├── data_load_result.png
│   ├── datestamp_error.png
│   ├── datestap_remapping.png
│   ├── delivery_performance.png
│   ├── fact_table_check_unique_id.png
│   ├── Final_report.png
│   ├── load_data_to_db.png
│   ├── load_data_to_db_execution.png
│   ├── monthly_revenue.png
│   ├── postgre_table_creation.png
│   ├── postgresql_all_commands.png
│   ├── power_bi_data_upload.png
│   ├── repeat_customer_null_table.png
│   ├── repeat_customer_unique_id.png
│   └── top_customers.png
│
└── README.md
```
 
---
 
## 📌 Phase 1: Data Loading (Python)
 
Raw CSV datasets from the Olist e-commerce platform were loaded into Python using **Pandas**. Three core tables were ingested: orders, customers, and payments.
 
```python
import pandas as pd
 
orders    = pd.read_csv("../data/raw/olist_orders_dataset.csv")
customers = pd.read_csv("../data/raw/olist_customers_dataset.csv")
payments  = pd.read_csv("../data/raw/olist_order_payments_dataset.csv")
 
print(orders.shape)
print(orders.head())
```
 
**Script written and executed in VS Code:**
 
![Data Load Script](screenshots/data_load.png)
 
**Script executed successfully:**
 
![Data Load Executed](screenshots/data_load_executed.png)
 
**Output — confirming data shape and structure:**
 
![Data Load Result](screenshots/data_load_result.png)
 
---
 
## 📌 Phase 2: Data Cleaning & Transformation
 
### Timestamp Handling
 
Raw timestamp columns were stored as plain strings and needed conversion to proper `datetime` objects for time-based calculations.
 
**Error encountered before conversion:**
 
![Timestamp Error](screenshots/datestamp_error.png)
 
```python
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
```
 
**Remapping applied — timestamps correctly parsed:**
 
![Timestamp Remapping](screenshots/datestap_remapping.png)
 
### Delivery Time Calculation
 
A new derived column `delivery_time_days` was engineered to measure fulfilment speed:
 
```python
orders['delivery_time_days'] = (
    orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']
).dt.days
```
 
**Delivery performance distribution:**
 
![Delivery Performance](screenshots/delivery_performance.png)
 
---
 
## 📌 Phase 3: Feature Engineering
 
Aggregated payment values at the order level and merged them into the master orders dataframe to build the **fact table**.
 
```python
# Aggregate payment value per order
order_value = payments.groupby('order_id')['payment_value'].sum().reset_index()
 
# Merge with orders
df = orders.merge(order_value, on='order_id', how='left')
 
# Merge customer location data
df = df.merge(customers[['customer_id', 'customer_city', 'customer_state']],
              on='customer_id', how='left')
 
print(df.shape)
print(df.isnull().sum())
```
 
**Unique order ID validation — confirming no duplicates in the fact table:**
 
![Fact Table Unique ID Check](screenshots/fact_table_check_unique_id.png)
 
**Repeat customer analysis — checking for NULL customer IDs:**
 
![Repeat Customer Null Table](screenshots/repeat_customer_null_table.png)
 
**Repeat customer — unique ID verification:**
 
![Repeat Customer Unique ID](screenshots/repeat_customer_unique_id.png)
 
**Top customers by order value:**
 
![Top Customers](screenshots/top_customers.png)
 
---
 
## 📌 Phase 4: Database Setup (PostgreSQL)
 
### Create the Database
 
```sql
CREATE DATABASE ecommerce;
```
 
### Create the Fact Table
 
```sql
CREATE TABLE fact_orders (
    order_id                        TEXT,
    customer_id                     TEXT,
    order_purchase_timestamp        TIMESTAMP,
    order_delivered_customer_date   TIMESTAMP,
    delivery_time_days              INT,
    payment_value                   NUMERIC,
    customer_city                   TEXT,
    customer_state                  TEXT
);
```
 
**Table creation confirmed in PostgreSQL:**
 
![PostgreSQL Table Creation](screenshots/postgre_table_creation.png)
 
**Full PostgreSQL command history:**
 
![PostgreSQL All Commands](screenshots/postgresql_all_commands.png)
 
---
 
## 📌 Phase 5: Load Data into PostgreSQL
 
The cleaned and transformed `fact_orders` dataframe was pushed directly into PostgreSQL using **SQLAlchemy**.
 
```python
from sqlalchemy import create_engine
 
engine = create_engine("postgresql://username:password@localhost:5432/ecommerce")
 
df.to_sql("fact_orders", engine, if_exists='replace', index=False)
 
print("Data loaded successfully!")
```
 
> ⚠️ Replace `username` and `password` with your actual PostgreSQL credentials before running.
 
**Load script in VS Code:**
 
![Load Data to DB Script](screenshots/load_data_to_db.png)
 
**Script execution — data flowing into PostgreSQL:**
 
![Load Data to DB Execution](screenshots/load_data_to_db_execution.png)
 
---
 
## 📌 Phase 6: SQL Validation & Analysis
 
After loading, several SQL queries were run directly in PostgreSQL to validate data integrity and extract analytical insights.
 
### Orders by State
 
```sql
SELECT
    customer_state,
    COUNT(*) AS total_orders
FROM fact_orders
GROUP BY customer_state
ORDER BY total_orders DESC;
```
 
### Monthly Revenue Trend
 
```sql
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month,
    ROUND(SUM(payment_value)::NUMERIC, 2)         AS total_revenue
FROM fact_orders
WHERE payment_value IS NOT NULL
GROUP BY month
ORDER BY month;
```
 
### Average Delivery Time
 
```sql
SELECT
    ROUND(AVG(delivery_time_days), 1) AS avg_delivery_days
FROM fact_orders
WHERE delivery_time_days IS NOT NULL;
```
 
**Monthly revenue query result:**
 
![Monthly Revenue](screenshots/monthly_revenue.png)
 
---
 
## 📌 Phase 7: Power BI Dashboard
 
PostgreSQL was connected to Power BI via the native PostgreSQL connector. The `fact_orders` table was imported and relationships were configured in the data model before building visuals.
 
**Data upload from PostgreSQL into Power BI:**
 
![Power BI Data Upload](screenshots/power_bi_data_upload.png)
 
### KPI Cards
 
| KPI | Description |
|-----|-------------|
| 💰 **Total Revenue** | Sum of all `payment_value` |
| 📦 **Total Orders** | Count of distinct `order_id` |
| 👥 **Total Customers** | Count of distinct `customer_id` |
| 🚚 **Avg. Delivery Time** | Average of `delivery_time_days` |
 
### Visuals Built
 
- 📈 **Revenue Trend** — Line chart showing monthly revenue over time
- 🗺️ **Orders by State** — Filled map showing order density by Brazilian state
- 🏙️ **Top Cities** — Bar chart of highest-order cities
- 👤 **Customer Distribution** — Repeat vs. one-time buyer breakdown
### Final Dashboard
 
![Final Power BI Dashboard](screenshots/Final_report.png)
 
---
 
## 💡 Key Insights
 
| Insight | Finding |
|---------|---------|
| 📍 Top region | São Paulo (SP) accounts for the majority of all orders |
| 📈 Revenue trend | Clear growth trajectory with visible seasonal spikes |
| 🚚 Delivery speed | Average delivery time is approximately **13–14 days** |
| 🔁 Customer loyalty | Majority of customers are **one-time buyers** |
 
---
 
## ⚠️ Limitations & Future Work
 
### Current Limitations
- No machine learning models included
- Basic feature engineering (no RFM segmentation)
- Dashboard is static — not deployed online
### Planned Improvements
 
- [ ] **RFM Analysis** — Customer segmentation by Recency, Frequency, Monetary value
- [ ] **Predictive Modeling** — Churn prediction & repeat purchase probability
- [ ] **Power BI Service** — Deploy dashboard online for live access
- [ ] **Automated Pipeline** — Schedule data refresh with Apache Airflow or cron jobs
- [ ] **dbt Integration** — Modular SQL transformations with lineage tracking
---
 
## 📈 What I Learned
 
- Designing and implementing an **end-to-end data pipeline**
- Data cleaning and transformation using **Pandas**
- Relational **database modeling** with PostgreSQL
- Writing analytical **SQL queries** for business reporting
- Building stakeholder-ready **Power BI dashboards**
- Translating raw data into **actionable business insights**
---
 
## 👨‍💻 Author
 
**Ramakrishna Tikka**
 
> If you found this project useful, feel free to ⭐ the repository!
 


