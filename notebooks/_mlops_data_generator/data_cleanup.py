# Databricks notebook source
# MAGIC %md
# MAGIC # `data_cleanup`

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
# DBTITLE 1,Module Imports
from src.common import Schema, drop_schema
from src.utils.notebook_utils import load_and_set_env_vars, load_config


# COMMAND ----------
# DBTITLE 1,Load Config
# Load env vars from config file (`conf/env_name/` dir)
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"), project="mlops")

# Load pipeline config from config file (`conf/pipeline_config/` dir)
# pipeline_config = load_config(
#     pipeline_name="data_cleanup_cfg",
#     project="mlops",
# )

# COMMAND ----------
# TODO: Update for new data oriented programming approach
cali_schema = Schema(name=env_vars["cali_schema"], catalog=env_vars["cali_catalog"])
wine_schema = Schema(name=env_vars["wine_schema"], catalog=env_vars["wine_catalog"])
iris_schema = Schema(name=env_vars["iris_schema"], catalog=env_vars["iris_catalog"])

drop_schema(cali_schema, cascade=True)
drop_schema(wine_schema, cascade=True)
drop_schema(iris_schema, cascade=True)
notebooks / _mlops_data_generator / data_cleanup.py
