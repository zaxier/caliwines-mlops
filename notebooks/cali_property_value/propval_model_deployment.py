# Databricks notebook source
# MAGIC %md
# MAGIC # `model_deployment`
# MAGIC Pipeline to execute model deployment. Model will be loaded from MLflow Model Registry and deployed.

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")
dbutils.widgets.dropdown("first_run", "True", ["True", "False"], "First Run?")

# COMMAND ----------
# DBTITLE 1,Module Imports
from src.common import Table
from src.utils.notebook_utils import load_and_set_env_vars, load_config
from src.mlops.model_deployment import (
    ModelDeployment,
    ModelDeploymentConfig,
)
from src.mlops.evaluation_utils import RegressionEvaluation
from src.mlops.mlflow_utils import MLflowTrackingConfig

# COMMAND ----------
# DBTITLE 1,Load Config
# Load env vars from config file (`conf/env_name/` dir)
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"))
print(env_vars)

# Load pipeline config from config file (`conf/pipeline_config/` dir)
pipeline_config = load_config(
    pipeline_name="propval_model_deployment_cfg",
    project="cali_mlops",
)
print(pipeline_config)

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config
mlflow_tracking_cfg = MLflowTrackingConfig(
    run_name="staging_vs_prod_comparison",
    experiment_path=env_vars["propval_model_deploy_exper_path"],
    model_name=env_vars["propval_model_name"],
)

model_deployment_cfg = ModelDeploymentConfig(
    mlflow_tracking_cfg=mlflow_tracking_cfg,
    reference_data=Table(
        catalog=env_vars["catalog"],
        schema=env_vars["property_schema"],
        table=env_vars["propval_reference_table"],
    ),
    label_col=env_vars["propval_label_col"],
    model_evaluation=RegressionEvaluation(),
    comparison_metric=pipeline_config["model_comparison_params"]["metric"],
    higher_is_better=pipeline_config["model_comparison_params"]["higher_is_better"],
)

# COMMAND ----------
# DBTITLE 1,Execute Pipeline
model_deployment = ModelDeployment(cfg=model_deployment_cfg)
if dbutils.widgets.get("first_run") == "True":
    model_deployment.run_wo_comparison()
else:
    model_deployment.run()
