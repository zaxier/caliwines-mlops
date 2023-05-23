# Databricks notebook source
# MAGIC %md
# MAGIC # `setup_data`
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
from src.get_data_utils.fetch_sklearn_datasets import (
    fetch_sklearn_cali_housing,
    fetch_sklearn_iris,
    fetch_sklearn_wine,
)
from src.utils.notebook_utils import load_and_set_env_vars

# COMMAND ----------
# DBTITLE 1,Load Config
# Load env vars from config file (`conf/env_name/` dir)
env_vars = load_and_set_env_vars(env=dbutils.widgets.get("env"), project="mlops")

holdout_pct = 20
random_seed = 42

cali_housing_table = MetastoreTable(
    name=env_vars["cali_train_table"],
    catalog=env_vars["cali_catalog"],
    schema=env_vars["cali_schema"],
)

iris_table = MetastoreTable(
    name=env_vars["iris_train_table"],
    catalog=env_vars["iris_catalog"],
    schema=env_vars["iris_schema"],
)

wine_table = MetastoreTable(
    name=env_vars["wine_train_table"],
    catalog=env_vars["wine_catalog"],
    schema=env_vars["wine_schema"],
)


# COMMAND ----------
def setup_data(fn, table: MetastoreTable) -> None:
    """
    Setup data for ML experiment.
    """
    if table.check_exists():
        pass
    else:
        # Load data
        df = fn()

        # Separate holdout set
        holdout_decimal = holdout_pct / 100
        train_df, holdout_df = df.randomSplit([(1 - holdout_decimal), holdout_decimal], seed=random_seed)

        train_df.write.format("delta").saveAsTable(table.ref)
        holdout_df.write.format("delta").saveAsTable(table.ref)


setup_data(fetch_sklearn_cali_housing, cali_housing_table)
setup_data(fetch_sklearn_iris, iris_table)
setup_data(fetch_sklearn_wine, wine_table)
