CREATE TABLE sales_transactions (
    transaction_id INT PRIMARY KEY,
    order_id INT,
    customer_id INT,
    product_id INT,
    order_date TIMESTAMP,
    quantity INT,
    unit_price NUMERIC(10, 2),
    total_price NUMERIC(10, 2),
    product_category VARCHAR(255),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
