# Databricks notebook source
# MAGIC %md
# MAGIC # `model_deployment`
# MAGIC
# MAGIC Pipeline to execute model deployment. Model will be loaded from MLflow Model Registry and deployed.

# COMMAND ----------
# DBTITLE 1,install requirement here if necessary
# MAGIC %pip install -r ../../requirements.txt

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
# DBTITLE 1,Module Imports
from packaged_poc.cali_housing_mlops.model_deployment import (
    ModelDeployment,
    ModelDeploymentConfig,
)
from packaged_poc.cali_housing_mlops.mlflow_utils import MLflowTrackingConfig
from packaged_poc.utils.notebook_utils import load_and_set_env_vars, load_config
from packaged_poc.common import MetastoreTable

# COMMAND ----------
# DBTITLE 1,Load Config
pipeline_config = load_config(pipeline_name="model_deployment", project="cali_housing_mlops")
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"))

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config
mlflow_tracking_cfg = MLflowTrackingConfig(
    run_name="staging_vs_prod_comparison",
    experiment_path=env_vars["model_deploy_experiment_path"],
    model_name=env_vars["model_name"],
)

model_deployment_cfg = ModelDeploymentConfig(
    mlflow_tracking_cfg=mlflow_tracking_cfg,
    reference_data=MetastoreTable(
        catalog=env_vars["catalog"],
        schema=env_vars["cali_housing_schema"],
        table=env_vars["reference_table_name"],
    ),
    comparison_metric=pipeline_config["model_comparison_params"]["metric"],
    higher_is_better=pipeline_config["model_comparison_params"]["higher_is_better"],
)

# COMMAND ----------
# DBTITLE 1,Execute Pipeline
model_deployment = ModelDeployment(cfg=model_deployment_cfg)
model_deployment.run()
