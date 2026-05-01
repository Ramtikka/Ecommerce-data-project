import pandas as pd

orders = pd.read_csv("../data/raw/olist_orders_dataset.csv")
customers = pd.read_csv("../data/raw/olist_customers_dataset.csv")
payments = pd.read_csv("../data/raw/olist_order_payments_dataset.csv")

print(orders.head())
print(customers.head())
print(payments.head())

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])

print("\nMissing Values:")
print(orders.isnull().sum())

# Drop rows without purchase date
orders = orders.dropna(subset=['order_purchase_timestamp'])

# Fill missing delivery dates 
orders['order_delivered_customer_date'] = orders['order_delivered_customer_date'].ffill()

orders['delivery_time_days'] = (
    orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']
).dt.days

order_value = payments.groupby('order_id')['payment_value'].sum().reset_index()

df = orders.merge(order_value, on='order_id', how='left')
df = df.merge(
    customers[['customer_id', 'customer_unique_id', 'customer_city', 'customer_state']],
    on='customer_id',
    how='left'
)

df.to_csv("../data/processed/fact_orders.csv", index=False)