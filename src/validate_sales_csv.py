import pandas as pd
import os

CSV_PATH = '../sales.csv'
EXPECTED_COLUMNS = [
    'transaction_id', 'order_id', 'customer_id', 'product_id', 'order_date',
    'quantity', 'unit_price', 'product_category', 'total_price'
]
EXPECTED_DTYPES = {
    'transaction_id': 'int64',
    'order_id': 'int64',
    'customer_id': 'int64',
    'product_id': 'int64',
    'order_date': 'object',  # Will check conversion to datetime
    'quantity': 'int64',
    'unit_price': 'float64',
    'product_category': 'object',
    'total_price': 'float64'
}

def validate_csv(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return False
    # Read a sample
    df = pd.read_csv(path, nrows=1000)
    # Check columns
    if list(df.columns) != EXPECTED_COLUMNS:
        print("Column mismatch!")
        print("Expected:", EXPECTED_COLUMNS)
        print("Found:", list(df.columns))
        return False
    # Check dtypes
    for col, dtype in EXPECTED_DTYPES.items():
        if col not in df.columns:
            print(f"Missing column: {col}")
            return False
        if dtype == 'object' and col == 'order_date':
            try:
                pd.to_datetime(df[col])
            except Exception as e:
                print(f"order_date conversion error: {e}")
                return False
        elif not str(df[col].dtype).startswith(dtype):
            print(f"Column {col} has dtype {df[col].dtype}, expected {dtype}")
            return False
    print("CSV validation passed. Sample data:")
    print(df.head())
    return True

if __name__ == '__main__':
    validate_csv(CSV_PATH)
