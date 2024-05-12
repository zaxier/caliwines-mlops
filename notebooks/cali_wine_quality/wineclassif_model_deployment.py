# Databricks notebook source
# MAGIC %md
# MAGIC # `model_deployment`
# MAGIC Pipeline to execute model deployment. Model will be loaded from MLflow Model Registry and deployed.

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
from src.mlops.evaluation_utils import ClassificationEvaluation
from src.mlops.mlflow_utils import MLflowTrackingConfig

# COMMAND ----------
# DBTITLE 1,Load Config
# Load env vars from config file (`conf/env_name/` dir)
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"))
print(env_vars)

# Load pipeline config from config file (`conf/pipeline_config/` dir)
pipeline_config = load_config(
    pipeline_name="wineclassif_model_deployment_cfg",
)
print(pipeline_config)

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config
mlflow_tracking_cfg = MLflowTrackingConfig(
    run_name="staging_vs_prod_comparison",
    experiment_path=env_vars["wineclassif_model_deploy_exper_path"],
    model_name=env_vars["wineclassif_model_name"],
)

model_deployment_cfg = ModelDeploymentConfig(
    mlflow_tracking_cfg=mlflow_tracking_cfg,
    reference_data=Table(
        catalog=env_vars["catalog"],
        schema=env_vars["wine_schema"],
        table=env_vars["wine_reference_table"],
    ),
    label_col=env_vars["wine_label_col"],
    model_evaluation=ClassificationEvaluation(),
    comparison_metric=pipeline_config["model_comparison_params"]["metric"],
    higher_is_better=pipeline_config["model_comparison_params"]["higher_is_better"],
)

# COMMAND ----------
# DBTITLE 1,Execute Pipeline
model_deployment = ModelDeployment(cfg=model_deployment_cfg)
if dbutils.widgets.get("compare_stag_v_prod").lower() == "true":
    model_deployment.run()
else:
    model_deployment.run_wo_comparison()
