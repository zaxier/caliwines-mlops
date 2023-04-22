# Databricks notebook source
# MAGIC %md
# MAGIC # `model_inference_batch`
# MAGIC
# MAGIC Pipeline to execute model inference. Model will be loaded from MLflow Model Registry and used to make predictions on a holdout dataset.

# COMMAND ----------
# DBTITLE 1,install requirement here if necessary
# MAGIC %pip install -r ../../requirements.txt

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
# DBTITLE 1,Module Imports
from packaged_poc.mlops.model_inference_batch import ModelInferenceBatch
from packaged_poc.common import MetastoreTable
from packaged_poc.utils.notebook_utils import load_config, load_and_set_env_vars

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config
pipeline_config = load_config(pipeline_name="model_inference_batch", project="cali_housing_mlops")
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"))
# TODO: Figure out if you want to move things like model name to the config file

model_name = pipeline_config["mlflow_params"]["model_name"] + f"_{env_vars['env']}"
model_registry_stage = pipeline_config["mlflow_params"]["model_registry_stage"]
model_uri = f"models:/{model_name}/{model_registry_stage}"

# COMMAND ----------
# DBTITLE 1,Execute Pipeline
model_inference = ModelInferenceBatch(
    model_uri=model_uri,
    input_table=MetastoreTable(
        catalog=env_vars["catalog"],
        schema=env_vars["cali_housing_schema"],
        table=pipeline_config["data_input"]["table_name"],
    ),
    output_table=MetastoreTable(
        catalog=env_vars["catalog"],
        schema=env_vars["cali_housing_schema"],
        table=pipeline_config["predictions_table_name"],
    ),
)

model_inference.run_and_write_batch()
