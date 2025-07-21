import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, trim, lower
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

# Glue boilerplate
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load data from S3 (Glue catalog table or direct path)
input_path = "s3://banking-cc-transactions/raw/"
df = spark.read.option("header", "true").csv(input_path)

# Data Cleaning
df_clean = (
    df.dropna(subset=["transaction_id", "customer_id", "amount", "timestamp"])  # Remove rows with critical nulls
      .withColumn("amount", col("amount").cast("double"))
      .withColumn("timestamp", to_timestamp("timestamp", "yyyy-MM-dd HH:mm:ss"))
      .withColumn("merchant", lower(trim(col("merchant"))))
      .withColumn("category", lower(trim(col("category"))))
)

# Write cleaned data back to S3
output_path = "s3://banking-cc-transactions/processed/"
df_clean.write.mode("overwrite").parquet(output_path)

# end Glue Job
job.commit()