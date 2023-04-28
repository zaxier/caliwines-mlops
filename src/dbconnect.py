from databricks.connect import DatabricksSession
from databricks.sdk.core import Config

spark = DatabricksSession.builder.getOrCreate()

spark.range(1, 10).show()
