# Databricks notebook source
# MAGIC %md
# MAGIC # `data_cleanup`

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
# DBTITLE 1,Module Imports
from src.common import Schema
from src.utils.notebook_utils import load_and_set_env_vars, load_config


# COMMAND ----------
# DBTITLE 1,Load Config
# Load env vars from config file (`conf/env_name/` dir)
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"), project="cali_mlops")

# Load pipeline config from config file (`conf/pipeline_config/` dir)
# pipeline_config = load_config(
#     pipeline_name="data_cleanup_cfg",
#     project="cali_mlops",
# )

# COMMAND ----------
# TODO: Update for new data oriented programming approach
cali_schema = Schema(catalog=env_vars["cali_catalog"], schema=env_vars["cali_schema"])
iris_schema = Schema(catalog=env_vars["iris_catalog"], schema=env_vars["iris_schema"])
wine_schema = Schema(catalog=env_vars["wine_catalog"], schema=env_vars["wine_schema"])

spark.sql(f"DROP SCHEMA IF EXISTS {cali_schema.qualified_name} CASCADE")
spark.sql(f"DROP SCHEMA IF EXISTS {iris_schema.qualified_name} CASCADE")
spark.sql(f"DROP SCHEMA IF EXISTS {wine_schema.qualified_name} CASCADE")
