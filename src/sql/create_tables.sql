CREATE TABLE sales_transactions (
    transaction_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    order_date TIMESTAMP,
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    total_price NUMERIC(10,2),
    product_category VARCHAR,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);