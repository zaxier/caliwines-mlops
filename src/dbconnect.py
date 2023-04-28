from databricks.connect import DatabricksSession
from databricks.sdk.core import Config

config = Config(profile="aws-e2-demo")
spark = DatabricksSession.builder.sdkConfig(config).getOrCreate()

spark.range(1, 10).show()

# pyspark --remote "sc://e2-demo-field-eng.cloud.databricks.com:443/;token=dapia7b7ac4fd147b8fe7f83551bc26a2977;x-databricks-cluster-id=0420-014219-930j61s2"
