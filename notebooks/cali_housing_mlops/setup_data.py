# Databricks notebook source
# MAGIC %md
# MAGIC # `setup_data`
# MAGIC
# MAGIC Pipeline to setup data that we will use for our ML experiment.

# COMMAND ----------
# DBTITLE 1,install requirement here if necessary
# MAGIC %pip install -r ../../requirements.txt

# COMMAND ----------
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
# DBTITLE 1,Module Imports
from packaged_poc.common import MetastoreTable
from packaged_poc.cali_housing_mlops.setup_data import (
    SetupCaliHousingMLopsConfig,
    SetupCaliHousingMLops,
)
from packaged_poc.utils.notebook_utils import load_config, load_and_set_env_vars_with_project

# COMMAND ----------
# DBTITLE 1,Load Config
pipeline_config = load_config(pipeline_name="setup_data", project="cali_housing_mlops")
env_vars = load_and_set_env_vars_with_project(env=dbutils.widgets.get("env"), project="cali_housing_mlops")

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config
setup_cali_housing_mlops_cfg = SetupCaliHousingMLopsConfig(
    train_table=MetastoreTable(
        catalog=env_vars["setup_data_catalog"],
        schema=env_vars["setup_data_schema"],
        table=env_vars["train_table_name"],
    ),
    holdout_table=MetastoreTable(
        catalog=env_vars["setup_data_catalog"],
        schema=env_vars["setup_data_schema"],
        table=env_vars["holdout_table_name"],
    ),
    holdout_pct=pipeline_config["holdout_params"]["holdout_pct"],
    random_seed=pipeline_config["holdout_params"]["random_seed"],
)

# COMMAND ----------
# DBTITLE 1, Execute Pipeline
setup_cali_housing_mlops = SetupCaliHousingMLops(cfg=setup_cali_housing_mlops_cfg)
setup_cali_housing_mlops.run()
