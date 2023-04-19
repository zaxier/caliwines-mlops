# Databricks notebook source
# MAGIC %md
# MAGIC # Access config notebook

# COMMAND ----------
from packaged_poc.cali_housing_mlops.pipelines._access_config import AccessConfig
from packaged_poc.utils.notebook_utils import load_and_set_env_vars, load_config
import os

# TODO LOAD AND SET ENV VARS
# load_and_set_env_vars()

print(os.getcwd())
task_config = load_config(pipeline_name="_access_config_config")
task = AccessConfig(init_conf=task_config)
task.launch()
