import os
import json
import boto3
import pandas as pd
import psycopg2

# Initialize AWS S3 client
s3_client = boto3.client('s3')

# Database connection details from environment variables
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT')

def etl_handler(event, context):
    """
    AWS Lambda handler for the ETL process.

    - Extracts data from an S3 trigger event.
    - Transforms the data using pandas.
    - Loads the transformed data into a PostgreSQL database.
    """
    try:
        # Extract file details from the S3 event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        
        print(f"Source Bucket: {bucket_name}")
        print(f"Object Key: {object_key}")

        # Get the CSV file from S3
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(s3_object['Body'])
        print(f"Initial DataFrame shape: {df.shape}")

        # --- Transform --- 
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

        print(f"DataFrame shape after transformation: {df.shape}")

        # --- Load --- 
        conn = None
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT
            )
            cursor = conn.cursor()

            for index, row in df.iterrows():
                insert_query = """
                INSERT INTO sales_transactions (transaction_id, order_id, customer_id, product_id, order_date, quantity, unit_price, total_price, product_category)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    row['transaction_id'],
                    row['order_id'],
                    row['customer_id'],
                    row['product_id'],
                    row['order_date'],
                    row['quantity'],
                    row['unit_price'],
                    row['total_price'],
                    row['product_category']
                ))
            
            conn.commit()
            print(f"Successfully inserted {len(df)} rows into the database.")

        finally:
            if conn:
                cursor.close()
                conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps(f"Successfully processed {len(df)} rows.")
        }

    except Exception as e:
        print(f"Error during ETL process: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error during ETL process: {e}")
        }