import pandas as pd
import numpy as np
from faker import Faker

# Parameters
NUM_RECORDS = 1_000_000
CSV_PATH = '../sales.csv'

fake = Faker()

# Product categories
categories = ['electronics', 'clothing', 'accessories', 'home', 'beauty', 'sports']

# Generate data
def generate_data(num_records):
    data = {
        'transaction_id': np.arange(1, num_records + 1),
        'order_id': np.random.randint(10000, 99999, num_records),
        'customer_id': np.random.choice(np.append(np.arange(1000, 9999), [None]), num_records),
        'product_id': np.random.randint(100, 999, num_records),
        'order_date': [fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_records)],
        'quantity': np.random.randint(1, 5, num_records),
        'unit_price': np.round(np.random.uniform(5.0, 500.0, num_records), 2),
        'product_category': np.random.choice(categories, num_records)
    }
    df = pd.DataFrame(data)
    # Standardize product_category to lowercase
    df['product_category'] = df['product_category'].str.lower()
    # Calculate total_price
    df['total_price'] = df['quantity'] * df['unit_price']
    # Handle missing customer_id
    df['customer_id'] = df['customer_id'].fillna(-1).astype(int)
    return df

if __name__ == '__main__':
    df = generate_data(NUM_RECORDS)
    df.to_csv(CSV_PATH, index=False)
    print(f"Generated {NUM_RECORDS} records to {CSV_PATH}")
