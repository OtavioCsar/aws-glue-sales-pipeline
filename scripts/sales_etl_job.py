from awsglue.transforms import *
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

# Lê dados do Glue Data Catalog (tabela criada por crawler)
sales_df = glueContext.create_dynamic_frame.from_catalog(
    database="sales_db",
    table_name="sales_data"
).toDF()

# Transformação: Calcula o total de vendas (quantity * price) por região
sales_df = sales_df.withColumn("total_sale", sales_df.quantity * sales_df.price)
aggregated_df = sales_df.groupBy("region").agg({"total_sale": "sum"})

# Salva o resultado em Parquet no S3
glueContext.write_dynamic_frame.from_df(
    aggregated_df,
    glueContext,
    "processed_sales"
).write_parquet(
    "s3://processed-sales-data-<seu-nome>/sales_parquet/"
)


job.commit()