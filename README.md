# 🏦 Credit Card Transaction ETL Pipeline using AWS Glue (Banking Domain)

This project demonstrates an end-to-end **ETL pipeline** built on AWS for processing and transforming **credit card transaction data** in the **banking domain** using AWS Glue, S3, and Athena.

---

## 🚀 Architecture Overview

<img width="1536" height="1024" alt="ChatGPT Image Jul 21, 2025, 04_00_39 PM" src="https://github.com/user-attachments/assets/fe5fabff-7852-4804-af1b-51f73c79e9a7" />


## 📂 Components

### 🗂 Data Source (Raw)
- Location: `s3://banking-cc-transactions/raw/`
- Format: CSV
- Sample Fields: `transaction_id`, `customer_id`, `amount`, `timestamp`, `merchant`, `category`

### 🧹 AWS Glue Job
- **PySpark script** performs:
  - Null filtering
  - Type casting (amount → double)
  - Timestamp parsing
  - Trimming & lowercasing of strings
- **Output Format**: Parquet
- **Output Path**: `s3://banking-cc-transactions/processed/`

### 📅 AWS Glue Trigger
- Type: **Scheduled**
- Time: Every day at `12:00 PM IST`
- Automatically triggers the Glue job

### 📊 AWS Glue Crawler
- Crawls the `processed` folder to update table schema
- Updates the Glue Data Catalog

### 🔍 Athena
- Query processed transactions via SQL:
```sql
SELECT * FROM "cc_transactions_db"."processed" LIMIT 10;
