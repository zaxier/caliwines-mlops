# Databricks notebook source
# MAGIC %md
# MAGIC # `model_train`
# MAGIC
# MAGIC Pipeline to execute model training. Params, metrics and model artifacts will be tracked to MLflow Tracking.
# MAGIC Optionally, the resulting model will be registered to MLflow Model Registry if provided.

# COMMAND ----------
# DBTITLE 1,install requirement here if necessary
# MAGIC %md
# MAGIC `%pip install -r ../requirements.txt`

# COMMAND ----------
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
from packaged_poc.cali_housing_mlops.model_train import (
    ModelTrain,
    ModelTrainConfig,
    MLflowTrackingConfig,
)
from packaged_poc.utils.notebook_utils import load_and_set_env_vars, load_config
from packaged_poc.common import MetastoreTable

# COMMAND ----------
# DBTITLE 1,Load Config
pipeline_config = load_config(pipeline_name="model_train", project="cali_housing_mlops")
env_vars = load_and_set_env_vars(
    env=dbutils.widgets.get("env"), project="cali_housing_mlops"
)

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config
mlflow_tracking_cfg = MLflowTrackingConfig(
    run_name=pipeline_config["mlflow_params"]["run_name"],
    experiment_path=env_vars["model_train_experiment_path"],
    model_name=env_vars["model_name"],
)

train_table = MetastoreTable(
    catalog=env_vars["catalog"],
    schema=env_vars["train_table_schema"],
    table=env_vars["train_table_name"],
)

model_train_cfg = ModelTrainConfig(
    mlflow_tracking_cfg=mlflow_tracking_cfg,
    train_table=train_table,
    label_col=env_vars["train_table_label_col"],
    pipeline_params=pipeline_config["pipeline_params"],
    model_params=pipeline_config["model_params"],
    conf=pipeline_config,
    env_vars=env_vars,
)

# COMMAND ----------
# DBTITLE 1,Execute Pipeline
model_train = ModelTrain(cfg=model_train_cfg)
model_train.run()
