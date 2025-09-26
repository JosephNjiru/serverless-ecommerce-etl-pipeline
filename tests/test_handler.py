import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

# In a real-world scenario, you would import the transformation logic 
# from your source code, e.g., from src.handler import apply_transformations
# For this test, we are redefining it to keep the test self-contained.
def apply_transformations(df: pd.DataFrame) -> pd.DataFrame:
    """Applies all the required data transformations."""
    # Convert order_date to datetime objects
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Clean and convert unit_price to numeric, removing currency symbols
    df['unit_price'] = df['unit_price'].replace({r'\$': ''}, regex=True).astype(float)

    # Ensure quantity is a numeric type, coercing errors
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    # Calculate total_price
    df['total_price'] = df['quantity'] * df['unit_price']

    # Handle missing customer_id
    df['customer_id'] = df['customer_id'].fillna(-1).astype(int)

    # Standardize product_category to lowercase
    df['product_category'] = df['product_category'].str.lower()
    
    return df


def test_transformation_logic():
    """Unit test for the ETL transformation logic."""
    # 1. Arrange: Create a sample DataFrame with raw, messy data
    raw_data = {
        'transaction_id': [1, 2, 3, 4],
        'order_id': [101, 102, 103, 104],
        'customer_id': [1001, None, 1003, 1004],
        'product_id': [2001, 2002, 2003, 2004],
        'order_date': ['12/01/2023 10:00', '12/01/2023 11:00', '12/01/2023 12:00', '12/01/2023 13:00'],
        'quantity': [1, '2', 3, 1],
        'unit_price': ['$10.00', '20.50', '$5.00', '15.00'],
        'product_category': ['Tops', 'Leggings', 'ACCESSORIES', 'Tops']
    }
    source_df = pd.DataFrame(raw_data)

    # 2. Act: Apply the transformation logic
    transformed_df = apply_transformations(source_df.copy())

    # 3. Assert: Check if the transformations were successful
    
    # Expected data after transformations
    expected_data = {
        'transaction_id': [1, 2, 3, 4],
        'order_id': [101, 102, 103, 104],
        'customer_id': [1001, -1, 1003, 1004],
        'product_id': [2001, 2002, 2003, 2004],
        'order_date': pd.to_datetime(['12/01/2023 10:00', '12/01/2023 11:00', '12/01/2023 12:00', '12/01/2023 13:00']),
        'quantity': [1, 2, 3, 1],
        'unit_price': [10.0, 20.50, 5.0, 15.0],
        'product_category': ['tops', 'leggings', 'accessories', 'tops'],
        'total_price': [10.0, 41.0, 15.0, 15.0]
    }
    expected_df = pd.DataFrame(expected_data)
    
    # Use pandas' testing utility to compare DataFrames
    assert_frame_equal(transformed_df, expected_df, check_dtype=True)