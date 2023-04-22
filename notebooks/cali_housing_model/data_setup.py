# Databricks notebook source
# MAGIC %md
# MAGIC # `setup_data`
# MAGIC
# MAGIC Pipeline to setup data that we will use for our ML experiment.

# COMMAND ----------
# DBTITLE 1,install requirement here if necessary
# MAGIC %pip install -r ../../requirements.txt

# COMMAND ----------
# DBTITLE 1,Set env
dbutils.widgets.dropdown("env", "dev", ["dev", "staging", "prod"], "Environment Name")

# COMMAND ----------
# DBTITLE 1,Module Imports
from packaged_poc.common import MetastoreTable
from packaged_poc.get_data_utils.cali_housing_data_setup import (
    SetupCaliHousingConfig,
    SetupCaliHousing,
)
from packaged_poc.utils.notebook_utils import load_config, load_and_set_env_vars

# COMMAND ----------
# DBTITLE 1,Load Config
pipeline_config = load_config(config_name="cali_setup_config")
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"))

# COMMAND ----------
# DBTITLE 1,Setup Pipeline Config
setup_cali_housing_mlops_cfg = SetupCaliHousingConfig(
    train_table=MetastoreTable(
        catalog=env_vars["catalog"],
        schema=env_vars["cali_housing_schema"],
        table=env_vars["cali_train_table"],
    ),
    holdout_table=MetastoreTable(
        catalog=env_vars["catalog"],
        schema=env_vars["cali_housing_schema"],
        table=env_vars["cali_holdout_table"],
    ),
    holdout_pct=pipeline_config["holdout_params"]["holdout_pct"],
    random_seed=pipeline_config["holdout_params"]["random_seed"],
)

# COMMAND ----------
# DBTITLE 1, Execute Pipeline
setup_cali_housing_mlops = SetupCaliHousing(cfg=setup_cali_housing_mlops_cfg)
setup_cali_housing_mlops.run()
