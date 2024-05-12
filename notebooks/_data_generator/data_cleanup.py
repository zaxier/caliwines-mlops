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
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"))

# COMMAND ----------
property_schema = Schema(catalog=env_vars["catalog"], schema=env_vars["property_schema"])
wine_schema = Schema(catalog=env_vars["catalog"], schema=env_vars["wine_schema"])

spark.sql(f"DROP SCHEMA IF EXISTS {property_schema.qualified_name} CASCADE")
spark.sql(f"DROP SCHEMA IF EXISTS {wine_schema.qualified_name} CASCADE")
