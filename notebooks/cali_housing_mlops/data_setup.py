# Databricks notebook source
# MAGIC %md
# MAGIC # `setup_data`
# MAGIC
# MAGIC Pipeline to setup data that we will use for our ML experiment.

# COMMAND ----------
# DBTITLE 1,Install requirements
# MAGIC %pip install -r ../../requirements.txt

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
# DBTITLE 1,Module Imports
from databricks_common.common import MetastoreTable
from src.utils.notebook_utils import load_config, load_and_set_env_vars
from src.get_data_utils.cali_housing_data_setup import (
    SetupCaliHousingConfig,
    CaliHousingDataSetup,
)

# COMMAND ----------
# DBTITLE 1,Load Config
# Load env vars from config file (`conf/env_name/` dir)
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"))

# Load pipeline config from config file (`conf/pipeline_config/` dir)
pipeline_config = load_config(
    pipeline_name="data_setup_cfg",
    project="cali_housing_mlops",
)

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config
setup_cali_housing_mlops_cfg = SetupCaliHousingConfig(
    train_table=MetastoreTable(
        catalog=env_vars["cali_catalog"],
        schema=env_vars["cali_schema"],
        table=env_vars["cali_train_table"],
    ),
    holdout_table=MetastoreTable(
        catalog=env_vars["cali_catalog"],
        schema=env_vars["cali_schema"],
        table=env_vars["cali_holdout_table"],
    ),
    holdout_pct=pipeline_config["holdout_params"]["holdout_pct"],
    random_seed=pipeline_config["holdout_params"]["random_seed"],
)

# COMMAND ----------
# DBTITLE 1, Execute Pipeline
setup_cali_housing_mlops = CaliHousingDataSetup(cfg=setup_cali_housing_mlops_cfg)
setup_cali_housing_mlops.run()
