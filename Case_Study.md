The Company:
"Zenith Active," a rapidly growing direct-to-consumer startup specializing in high-end activewear.

The Business Problem:
Zenith Active's sales are booming, but their analytics capabilities are lagging. Every night, their third-party payment processor uploads a raw CSV file of the day's transactions to an AWS S3 bucket. Currently, an analyst manually downloads this file, cleans it in Excel, and uploads it to a database. This process is slow, prone to errors, and cannot scale with the company's growth. The Head of Analytics needs an automated, reliable pipeline to get this data into their PostgreSQL data warehouse every morning so the team can update their BI dashboards.

The Data Source (Raw CSV File):
The file, named sales_YYYY-MM-DD.csv, contains the following columns. However, the data quality is inconsistent:

transaction_id: Unique identifier for the transaction.

order_id: Identifier for the customer's order.

customer_id: The customer's unique ID. Sometimes this field is blank.

product_id: The ID of the product purchased.

order_date: The date and time of the transaction in MM/DD/YYYY HH:MM format.

quantity: Number of units sold.

unit_price: The price of a single unit. Sometimes contains currency symbols like '$'.

product_category: The category of the product (e.g., "Tops", "Leggings", "accessories"). The casing is inconsistent (e.g., "tops", "Tops").

The Transformation Requirements (Business Rules):
The data must be cleaned and standardized before being loaded into the data warehouse. The Head of Analytics has specified the following rules:

Data Types: Ensure all columns have the correct data type (e.g., order_date must be a proper timestamp, unit_price must be a numeric type).

Handle Missing customer_id: For any transaction with a missing customer_id, assign a placeholder value of -1 to signify an anonymous or guest checkout.

Clean unit_price: Remove any currency symbols or commas from the unit_price column before converting it to a numeric type.

Standardize product_category: Convert all entries in the product_category column to lowercase to ensure consistency (e.g., "Tops" and "tops" both become "tops").

Create total_price: A new column, total_price, must be calculated by multiplying quantity by the cleaned unit_price.

The Desired Outcome:
A clean, structured sales_transactions table in the PostgreSQL data warehouse that is automatically updated daily. This table will be the single source of truth for all sales-related reporting and will directly feed into the company's daily performance dashboards used by the leadership team.

