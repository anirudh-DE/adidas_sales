# Adidas US Sales Data Engineering and Visualization Project (2020-2021)

## Overview
This project builds an end-to-end data engineering pipeline to process, analyze, and visualize the Adidas US Sales dataset (2020-2021). The pipeline extracts raw sales data, transforms and cleanses it using AWS services, loads it into a data warehouse, and creates interactive dashboards in Tableau to derive insights.

### Objectives
- Build a scalable ELT pipeline using AWS cloud services.
- Cleanse and transform sales data for analysis.
- Create interactive dashboards to visualize sales trends, top products, retailers, and regional performance.
- Highlight key metrics like total sales, average price per product, and top cities.

### Dataset
The dataset (`Adidas US Sales Datasets.xlsx`) contains sales transactions for Adidas products in the US from 2020 to 2021. Key columns include:
- `Retailer`, `Retailer ID`, `Date`, `Region`, `State`, `City`, `Product`, `Price per Unit`, `Units Sold`, `Total Sales`, `Operating Profit`, `Operating Margin`, `Sales Method`.

## Project Architecture
1. **AWS S3**: Stores raw data (`s3://adidas-buckets3/raw/`) and processed data (`s3://adidas-buckets3/processed/`).
2. **AWS Glue**: Extracts data from S3, performs transformations (e.g., handling missing values, standardizing data, correcting calculations), and writes to S3.
3. **Amazon Redshift**: Loads the processed data into a data warehouse for querying.
4. **Tableau**: Connects to Redshift to create two interactive dashboards:
   - **Dashboard 1**: 2020-2021 sales across the US.

## Tech Stack
- **Storage**: AWS S3
- **ETL/ELT**: AWS Glue (PySpark)
- **Data Warehouse**: Amazon Redshift
- **Visualization**: Tableau
- **Programming**: Python (PySpark)

## Key Features
- **Data Pipeline**:
  - Extracts raw Excel data from S3.
  - Transforms data using Glue jobs (e.g., type conversion, deduplication, standardization).
  - Loads data into Redshift using the `COPY` command.
- **Dashboards**:
  - Visualizations: Top products by sales (bar chart), top states/cities (pie chart), most popular retailers (bar chart), top products by units sold (pie chart), and KPI metrics.
  - Total sales: $900M (entire dataset)
  - Average price per product: $45.22 (entire dataset)
    
### Prerequisites
- AWS Account with permissions for S3, Glue, Redshift.
- Tableau Desktop or Tableau Public.
- Redshift JDBC driver (for Glue-to-Redshift connection).
- Python (for local testing of Glue scripts).

### Dashboard
![Image](https://github.com/user-attachments/assets/f0d97fc1-ed0a-43df-ba84-761f7e8d6afe)
