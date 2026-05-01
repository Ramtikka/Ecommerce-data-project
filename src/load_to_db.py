from sqlalchemy import create_engine
import pandas as pd

df = pd.read_csv("../data/processed/fact_orders.csv")

engine = create_engine("postgresql://postgres:6979%40Ramu@localhost:5432/ecommerce")

df.to_sql("fact_orders", engine, if_exists='replace', index=False)

print("Data loaded successfully!")