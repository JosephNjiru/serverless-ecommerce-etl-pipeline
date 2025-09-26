Automated ETL Pipeline for E-commerce Analytics
This project demonstrates a fully automated, serverless ETL (Extract, Transform, Load) pipeline built on AWS. The pipeline is designed to process daily e-commerce sales data, clean it, and load it into a PostgreSQL data warehouse for analytics and business intelligence.

1. Business Problem & Strategic Value
A fast-growing e-commerce startup needs to centralize its daily sales transaction data to power its business intelligence (BI) dashboards and reporting. A legacy system uploads raw sales data as CSV files to an AWS S3 bucket at the end of each day.

The key challenge is to move this data into a structured analytical database in a way that is:

Automated: Eliminates the need for manual intervention, reducing the risk of human error.

Timely: Ensures data is available for the analytics team at the start of each business day.

Scalable: Can handle a growing volume of sales data without performance degradation.

Cost-Effective: Leverages serverless technology to minimize infrastructure costs.

This project showcases foundational data engineering skills in cloud automation, ETL processes, and database management—core competencies for any modern data role.   

2. Solution Architecture
The pipeline is event-driven and built entirely on serverless AWS components. This architecture ensures high availability and scalability while only incurring costs when data is actively being processed.

The data flows through the following steps:

File Upload: A .csv file containing raw sales data is uploaded to a designated AWS S3 bucket (source-data-bucket).

Event Trigger: The S3 PutObject event automatically triggers an AWS Lambda function.

ETL Execution: The Lambda function, written in Python, executes the core ETL logic:

Extract: Reads the newly uploaded CSV file from S3 into a Pandas DataFrame.

Transform: Cleans and transforms the data (handles missing values, corrects data types, calculates new fields).

Load: Connects to a PostgreSQL database and appends the cleaned data into the sales_transactions table.

Data Warehouse: The structured data is now available in the PostgreSQL data warehouse for querying by BI tools like Tableau or Power BI.

┌──────────────────┐      ┌───────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   Upload CSV to  │ ───► │ S3 Event Trigger  │ ───► │  AWS Lambda      │ ───► │  PostgreSQL      │
│       S3         │      │  (PutObject)      │      │ (Python ETL)     │      │  Data Warehouse  │
└──────────────────┘      └───────────────────┘      └──────────────────┘      └──────────────────┘
3. Technologies Used
Technology	Purpose
AWS S3	Scalable object storage for raw data files.
AWS Lambda	Serverless compute for running the ETL script without managing servers.
PostgreSQL	Relational database serving as the analytical data warehouse.
Python	Core programming language for the ETL logic.
Pandas	Python library for efficient data manipulation and transformation.
Boto3	AWS SDK for Python, used to interact with S3.
Psycopg2	PostgreSQL adapter for Python to connect and load data.
AWS SAM/Serverless	Framework for deploying the serverless application infrastructure as code.

## Project Structure
```
serverless-ecommerce-etl-pipeline/
├── src/
│   ├── __init__.py
│   ├── handler.py
│   └── sql/
│       └── create_tables.sql
├── tests/
│   ├── __init__.py
│   └── test_handler.py
├── requirements/
│   ├── base.txt
│   └── dev.txt
├── .gitignore
├── Case_Study.md
├── template.yaml
└── README.md
```

Export to Sheets
4. ETL Logic Details
Extract
The Lambda function is triggered by an S3 event notification. The event payload contains the bucket name and the object key (file name) of the newly uploaded file. The function uses boto3 to stream this file directly from S3 into a Pandas DataFrame.

Transform
The transformation logic, executed within the Lambda function, performs several key operations to ensure data quality and consistency:

Data Type Conversion: Ensures columns like order_date are converted to datetime objects and price is converted to a numeric type.

Handling Missing Values: Implements a strategy for null values, such as filling missing customer_id with a placeholder like -1.

Data Standardization: Standardizes text fields, such as converting product_category to lowercase.

Feature Engineering: Creates a new column, total_price, by multiplying quantity and unit_price.

Load
After transformation, the script establishes a connection to the PostgreSQL database using credentials securely stored in AWS Secrets Manager. The cleaned DataFrame is then efficiently appended to the sales_transactions table using psycopg2.

5. Target Database Schema
The data is loaded into a structured table designed for analytical queries. The following SQL statement defines the target schema in PostgreSQL:

SQL

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
6. Deployment Instructions
This serverless application is designed to be deployed using the AWS Serverless Application Model (SAM) CLI.

Prerequisites:

AWS CLI configured with appropriate permissions.

AWS SAM CLI installed.

Docker installed and running.

Deployment Steps:

Clone the repository:

Bash

git clone https://github.com/JosephNjiru/serverless-ecommerce-etl-pipeline.git
cd serverless-ecommerce-etl-pipeline
Build the application:
This command builds the dependencies and creates a deployment package.

Bash

sam build
Deploy the application:
This command packages and deploys the application to AWS CloudFormation. You will be guided through a series of prompts to set parameters like the S3 bucket name and database credentials.

Bash

sam deploy --guided
The SAM template (template.yaml) defines all the necessary AWS resources, including the S3 bucket, the Lambda function, and the necessary IAM roles and permissions.

7. How to Trigger and Monitor
Triggering the Pipeline
To trigger the ETL process, simply upload a CSV file with the correct schema to the source S3 bucket specified during deployment. You can use the AWS Management Console or the AWS CLI:

Bash

aws s3 cp sample_data.csv s3://your-source-data-bucket/
Monitoring
The pipeline's execution can be monitored through AWS CloudWatch:

Logs: All print statements and any errors from the Lambda function are logged in CloudWatch Logs. This is the primary place to debug any issues.

Metrics: CloudWatch automatically tracks metrics for the Lambda function, such as the number of invocations, execution duration, and error rates.

Alarms: For a production environment, CloudWatch Alarms can be configured to send notifications (e.g., via SNS) if the Lambda function fails or experiences a high error rate.
