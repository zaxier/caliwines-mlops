# Databricks notebook source
# MAGIC %md
# MAGIC # `model_deployment`
# MAGIC Pipeline to execute model deployment. Model will be loaded from MLflow Model Registry and deployed.

# COMMAND ----------
# DBTITLE 1,Install requirements
# MAGIC %pip install -r ../../requirements.txt

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
# DBTITLE 1,Module Imports
from src.common import Table
from src.utils.notebook_utils import load_and_set_env_vars, load_config
from src.mlops.model_deployment import (
    ModelDeployment,
    ModelDeploymentConfig,
)
from src.mlops.mlflow_utils import MLflowTrackingConfig

# COMMAND ----------
# DBTITLE 1,Load Config
# Load env vars from config file (`conf/env_name/` dir)
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"), project="mlops")
print(env_vars)

# Load pipeline config from config file (`conf/pipeline_config/` dir)
pipeline_config = load_config(
    pipeline_name="cali_housing_model_deployment_cfg",
    project="mlops",
)
print(pipeline_config)

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config
mlflow_tracking_cfg = MLflowTrackingConfig(
    run_name="staging_vs_prod_comparison",
    experiment_path=env_vars["cali_deploy_exper_path"],
    model_name=env_vars["cali_model_name"],
)

model_deployment_cfg = ModelDeploymentConfig(
    mlflow_tracking_cfg=mlflow_tracking_cfg,
    reference_data=Table(
        name=env_vars["cali_reference_table"],
        catalog=env_vars["cali_catalog"],
        schema=env_vars["cali_schema"],
    ),
    label_col=env_vars["cali_label_col"],
    comparison_metric=pipeline_config["model_comparison_params"]["metric"],
    higher_is_better=pipeline_config["model_comparison_params"]["higher_is_better"],
)

# COMMAND ----------
# DBTITLE 1,Execute Pipeline
model_deployment = ModelDeployment(cfg=model_deployment_cfg)
model_deployment.run_wo_comparison()
