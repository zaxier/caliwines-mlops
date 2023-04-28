# Databricks notebook source
# MAGIC %md
# MAGIC # `model_inference_batch`
# MAGIC
# MAGIC Pipeline to execute model inference. Model will be loaded from MLflow Model Registry and used to make predictions on a holdout dataset.

# COMMAND ----------
# DBTITLE 1,Install requirements
# MAGIC %pip install -r ../../requirements.txt

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
# DBTITLE 1,Module Imports
from databricks_common import MetastoreTable
from src.utils.notebook_utils import load_config, load_and_set_env_vars
from src.mlops.model_inference_batch import ModelInferenceBatch

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config

# Load env vars from config file (`conf/env_name/` dir)
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"))

# Load pipeline config from config file (`conf/pipeline_config/` dir)
pipeline_config = load_config(
    pipeline_name="model_inference_batch_cfg",
    project="cali_housing_mlops",
)

env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"))

model_name = env_vars["cali_model_name"]
model_registry_stage = pipeline_config["mlflow_params"]["model_registry_stage"]
model_uri = f"models:/{model_name}/{model_registry_stage}"

# COMMAND ----------
# DBTITLE 1,Execute Pipeline
model_inference = ModelInferenceBatch(
    model_uri=model_uri,
    input_table=MetastoreTable(
        catalog=env_vars["cali_catalog"],
        schema=env_vars["cali_schema"],
        table=pipeline_config["data_input"]["table_name"],
    ),
    output_table=MetastoreTable(
        catalog=env_vars["cali_catalog"],
        schema=env_vars["cali_schema"],
        table=pipeline_config["data_output"]["table_name"],
    ),
)

model_inference.run_and_write_batch()
