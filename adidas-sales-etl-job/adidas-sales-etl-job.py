# -*- coding: utf-8 -*-
"""adidas-sales-etl-job1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e01S18dp3ktLplj0wt0aJ8HLV1eZawbr

# AWS Glue Studio Notebook
##### You are now running a AWS Glue Studio notebook; To start using your notebook you need to start an AWS Glue Interactive Session.

#### Optional: Run this cell to see available notebook commands ("magics").

####  Run this cell to set up and start your interactive session.
"""

# Commented out IPython magic to ensure Python compatibility.
# %idle_timeout 2880
# %glue_version 5.0
# %worker_type G.1X
# %number_of_workers 5

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

"""#### Example: Create a DynamicFrame from a table in the AWS Glue Data Catalog and display its schema

"""

# Read data from S3 via Glue Data Catalog
data_source = glueContext.create_dynamic_frame.from_catalog(
    database = "adaidas",
    table_name="raw"
    ).toDF()

data_source.printSchema()

# Step 1: Data Type Conversion
from pyspark.sql.functions import *
from pyspark.sql.types import *

df = (
    data_source
    .withColumn("invoice date", to_date(col("invoice date"), "M/d/yyyy"))
    .withColumn("price per unit", regexp_replace(trim(col("price per unit")), "[$,\"]", "").cast(DecimalType(10, 2)))
    .withColumn("units sold", regexp_replace(trim(col("units sold")), ",", "").cast("int"))
    .withColumn("total sales", regexp_replace(trim(col("total sales")), "[$,\"]", "").cast(DecimalType(15, 2)))
    .withColumn("operating profit", regexp_replace(trim(col("operating profit")), "[$,\"]", "").cast(DecimalType(15, 2)))
    .withColumn("operating margin", regexp_replace(trim(col("operating margin")), "[%,\"]", "").cast(DecimalType(5, 2)))

)

df.printSchema()

# Step 2: Handle Missing Values
df = df.fillna(value = 0 , subset = ["operating profit","operating margin"])
df = df.fillna({"sales method" : "In-store", "product" : "Unknown"})

# Step 3: Standardize Data (example for State)
state_mapping = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY"
}
df = df.replace(state_mapping, subset = ["state"])

# Step 4: Correct Calculation Errors
from pyspark.sql.functions import *
from pyspark.sql.types import *

df = df.withColumn("Calculated_Total_Sales", col("price per unit") * col("units sold")) \
        .withColumn("total sales", when(col("total sales") != col("Calculated_Total_Sales"), col("Calculated_Total_Sales")).otherwise(col("total sales"))) \
        .drop("Calculated_Total_Sales")

df = df.withColumn("Calculated_Operating_Profit", col("operating profit") * col("total sales")) \
        .withColumn("operating profit", when(col("operating profit") != col("Calculated_Operating_Profit"), col("Calculated_Operating_Profit")).otherwise(col("operating profit"))) \
        .drop("Calculated_Operating_Profit")

# Step 5: Create Derived Columns
from pyspark.sql.functions import *
from pyspark.sql.types import *

df = df.withColumn("year",year(col("invoice date")))
df = df.withColumn("month",month(col("invoice date")))
df = df.withColumn("quarter",quarter(col("invoice date")))

# Step 6: Round Numerical Columns
from pyspark.sql.functions import *
from pyspark.sql.types import *

numerical_columns = ["price per unit","total sales","operating profit","operating margin"]
for column in numerical_columns:
    df = df.withColumn(column, round(col(column),2))

# Step 7: Reanming Required Columns
df = df.withColumnRenamed("retailer id","retailer_id") \
        .withColumnRenamed("invoice date","invoice_date") \
        .withColumnRenamed("price per unit","price_per_unit") \
        .withColumnRenamed("units sold","units_sold") \
        .withColumnRenamed("total sales","total_sales") \
        .withColumnRenamed("operating profit","operating_profit") \
        .withColumnRenamed("operating margin","operating_margin") \
        .withColumnRenamed("sales method","sales_method") \
        .withColumnRenamed("year","sale_year") \
        .withColumnRenamed("month","sale_month") \
        .withColumnRenamed("quarter","sale_quarter")

# Step 8: Final Data Validation
df = df.filter((col("units_sold") >= 0) & (col("total_sales") >= 0))

df.printSchema()

# Write cleaned data to S3
df.write.mode("overwrite").csv("s3://adidas-buckets3/processed/adidas_sales_cleaned")