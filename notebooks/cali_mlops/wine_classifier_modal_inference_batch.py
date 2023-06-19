# Databricks notebook source
# MAGIC %md
# MAGIC # `model_inference_batch`
# MAGIC Pipeline to execute model inference. Model will be loaded from MLflow Model Registry and used to make predictions on a holdout dataset.

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")
dbutils.widgets.text("job-id", "test", "Job ID")  # TODO
dbutils.widgets.text("start-time", "", "Start Time")  # TODO

# COMMAND ----------
# DBTITLE 1,Module Imports
from src.common import Table
from src.utils.notebook_utils import load_config, load_and_set_env_vars
from src.mlops.model_inference_batch import ModelInferenceBatchPipeline

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config

# Load env vars from config file (`conf/env_name/` dir)
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"), project="cali_mlops")

# Load pipeline config from config file (`conf/pipeline_config/` dir)
pipeline_config = load_config(
    pipeline_name="wine_model_inference_batch_cfg",
    project="cali_mlops",
)

model_name = env_vars["wine_model_name"]
model_registry_stage = pipeline_config["mlflow_params"]["model_registry_stage"]
model_uri = f"models:/{model_name}/{model_registry_stage}"

input_table = Table(
    catalog=env_vars["wine_catalog"],
    schema=env_vars["wine_schema"],
    table=pipeline_config["data_input"]["table_name"],
)

output_table = Table(
    catalog=env_vars["wine_catalog"],
    schema=env_vars["wine_schema"],
    table=pipeline_config["data_output"]["table_name"],
)

# COMMAND ----------
# DBTITLE 1,Execute Pipeline
cali_housing_inference_pipeline = ModelInferenceBatchPipeline(
    model_uri=model_uri,
    input_table=input_table,
    output_table=output_table,
)

cali_housing_inference_pipeline.run_and_write_batch()
