from awsglue.transform import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import sys

# Inicializa o contexto do Glue
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Lê os dados de vendas do Glue Data Catalog
sales_data = glueContext.create_dynamic_frame.from_catalog(
    database="sales_db",
    table_name="sales_table",
).toDF()

# Transformação: Calcula o total de vendas (quantity * price) por região
sales_df = sales_df.withColumn("total_sales", sales.df["quantity"] * sales_df["price"])
aggregated_df = sales_df.groupBy("region").agg({"total_sales": "sum"})

# Salva o resultado em Parquet no S3
glueContext.write_dynamic_frame.from_df(
    aggregated_df,
    glueContext,
    "processed_sales",
).write_parquet(
    "s3://processed-sales-data-<test>-region/sales_parquet/"
)

job.commit()
