import os
import pathlib
import dotenv
import yaml
import pprint
from typing import Dict, Any

from packaged_poc.utils.get_spark import spark
from pyspark.sql import SparkSession

relative_root = os.path.join(os.pardir, os.pardir)


def load_and_set_env_vars(env: str) -> Dict[str, Any]:
    """
    Utility function to use in Databricks notebooks to load .env files and set them via os
    Return a dict of set environment variables
    Parameters
    ----------
    env : str
        Name of deployment environment. One of
    Returns
    -------
    Dictionary of set environment variables
    """
    env_vars_path = os.path.join(relative_root, "conf", env, f".{env}.env")
    dotenv.load_dotenv(env_vars_path)

    base_data_vars_vars_path = os.path.join(relative_root, "conf", ".base_data_params.env")
    dotenv.load_dotenv(base_data_vars_vars_path)

    os_dict = dict(os.environ)
    pprint.pprint(os_dict)

    return os_dict


def load_config_depr(pipeline_name) -> Dict[str, Any]:
    """
    Utility function to use in Databricks notebooks to load the config yaml file for a given pipeline
    Return dict of specified config params
    Parameters
    ----------
    pipeline_name :  str
        Name of pipeline
    Returns
    -------
    Dictionary of config params
    """
    config_path = os.path.join(os.pardir, os.pardir, "conf", "pipeline_configs", f"{pipeline_name}.yml")
    pipeline_config = yaml.safe_load(pathlib.Path(config_path).read_text())
    pprint.pprint(pipeline_config)

    return pipeline_config


def load_config(pipeline_name, project) -> Dict[str, Any]:
    """
    Utility function to use in Databricks notebooks to load the config yaml file for a given pipeline
    Return dict of specified config params
    Parameters
    ----------
    pipeline_name :  str
        Name of pipeline
    project : str
        Name of project (e.g. "cali_housing_mlops")
    Returns
    -------
    Dictionary of config params
    """
    config_path = os.path.join(
        relative_root,
        "conf",
        project,
        "pipeline_configs",
        f"{pipeline_name}.yml",
    )
    config = yaml.safe_load(pathlib.Path(config_path).read_text())
    pprint.pprint(config)
    return config


# def get_dbutils(
#     spark: SparkSession,
# ):  # please note that this function is used in mocking by its name
#     try:
#         from pyspark.dbutils import DBUtils  # noqa

#         if "dbutils" not in locals():
#             utils = DBUtils(spark)
#             return utils
#         else:
#             return locals().get("dbutils")
#     except ImportError:
#         return None


# def profile_df(df):
#     utils = get_dbutils(spark)
#     utils.data.summarize(df)
