CREATE TABLE adidas_sales (
    Retailer VARCHAR(50),
    Retailer_ID VARCHAR(20),
    Date DATE,
    Region VARCHAR(20),
    State VARCHAR(50),
    City VARCHAR(50),
    Product VARCHAR(50),
    Price_per_Unit DECIMAL(10,2),
    Units_Sold INT,
    Total_Sales DECIMAL(15,2),
    Operating_Profit DECIMAL(15,2),
    Operating_Margin DECIMAL(5,2),
    Sales_Method VARCHAR(20),
    Year INT,
    Month INT,
    Quarter INT
);

COPY adidas_sales
FROM 's3://adidas-buckets3/processed/adidas_sales_cleaned/'
IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-s3-access'
CSV
IGNOREHEADER 1;
