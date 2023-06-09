# Databricks notebook source
# MAGIC %md
# MAGIC # `setup_data`
# MAGIC Pipeline to setup data that we will use for our ML experiment.

# COMMAND ----------
# DBTITLE 1,Install requirements
# MAGIC %pip install -r ../../requirements.txt

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
# DBTITLE 1,Module Imports
from src.common import Table, Schema
from src.get_data_utils.fetch_sklearn_datasets import (
    fetch_sklearn_cali_housing,
    fetch_sklearn_iris,
    fetch_sklearn_wine,
)
from src.utils.notebook_utils import load_and_set_env_vars

# COMMAND ----------
# Dev imports
from src.utils.logger_utils import get_logger
from src.utils.get_spark import spark

_logger = get_logger()

# COMMAND ----------
# DBTITLE 1,Load Config
# Load env vars from config file (`conf/env_name/` dir)
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"), project="mlops")

# COMMAND ----------
# DBTITLE 1,Set Variables
holdout_pct = 20
random_seed = 42

cali_schema = Schema(
    catalog=env_vars["cali_catalog"],
    schema=env_vars["cali_schema"],
)

iris_schema = Schema(
    catalog=env_vars["iris_catalog"],
    schema=env_vars["iris_schema"],
)

wine_schema = Schema(
    catalog=env_vars["wine_catalog"],
    schema=env_vars["wine_schema"],
)

# COMMAND ----------
# DBTITLE 1,Create Schemas
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {cali_schema.qualified_name}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {iris_schema.qualified_name}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {wine_schema.qualified_name}")


# COMMAND ----------
def setup_data(fn, schema: Schema) -> None:
    """
    Setup data for ML experiment.
    """
    train_table = Table.from_string(schema.qualified_name + ".train")
    _logger.debug(f"schema.qualified_name: {schema.qualified_name}")
    _logger.debug(f"table.qualified_name: {schema.qualified_name}.train")
    _logger.debug(f"train_table.qualified_name: {train_table.qualified_name}")

    holdout_table = Table.from_string(schema.qualified_name + ".holdout")
    _logger.info(f"schema.qualified_name: {schema.qualified_name}")
    _logger.info(f"table.qualified_name: {schema.qualified_name}.holdout")
    _logger.info(f"holdout_table.qualified_name: {holdout_table.qualified_name}")

    df = fn()

    # Separate holdout set
    holdout_decimal = holdout_pct / 100
    train_df, holdout_df = df.randomSplit([(1 - holdout_decimal), holdout_decimal], seed=random_seed)

    # Write to metastore
    train_df.write.mode("overwrite").format("delta").saveAsTable(train_table.qualified_name)
    holdout_df.write.mode("overwrite").format("delta").saveAsTable(holdout_table.qualified_name)


setup_data(fetch_sklearn_cali_housing, cali_schema)
setup_data(fetch_sklearn_iris, iris_schema)
setup_data(fetch_sklearn_wine, wine_schema)
