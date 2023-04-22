from dataclasses import dataclass
from typing import Callable, List, Union

import pyspark.sql.dataframe
from sklearn.datasets import fetch_california_housing, load_iris
import pandas as pd

from packaged_poc.utils.logger_utils import get_logger
from packaged_poc.utils.get_spark import spark
from packaged_poc.utils.notebook_utils import load_and_set_env_vars, load_config

_logger = get_logger()


class SklearnDataFetcher:
    """
    Class to fetch sklearn datasets easily
    """

    def __init__(self, datasets: Union[str, List[str]]):
        self.datasets = datasets

    @staticmethod
    def _fetch_sklearn_cali_housing() -> pyspark.sql.DataFrame:
        _data: pd.DataFrame = fetch_california_housing(as_frame=True).frame
        return spark.createDataFrame(_data)

    @staticmethod
    def _fetch_sklearn_iris() -> pyspark.sql.DataFrame:
        df: pd.DataFrame = load_iris(as_frame=True).frame
        return spark.createDataFrame(df)

    @staticmethod
    def fetch_dataset_from_name(dataset_name: str):
        function_dict: dict = {
            "california_housing": SklearnDataFetcher._fetch_sklearn_cali_housing(),
            "iris": SklearnDataFetcher._fetch_sklearn_iris(),
        }
        try:
            return function_dict[dataset_name]
        except KeyError as e:
            _logger.error(
                f"The name '{dataset_name}' is not a valid option, select from list {list(function_dict.keys())}"
            )
            raise

    @staticmethod
    def write_to_temp_dbfs(df: pyspark.sql.DataFrame, table_name: str, dbfs_dir: str = "dbfs:/FileStore") -> None:
        """
        Write a dataframe to a temporary table in the database
        """
        df.write.parquet(f"{dbfs_dir}/{table_name}/")

    def run(self) -> None:
        """
        Run the task
        """

        if isinstance(self.datasets, str):
            # Get dataframe
            df = self.fetch_dataset_from_name(self.datasets)
            _logger.info(type(df))
            dataset_name = self.datasets

            # Write to temp dbfs
            # self.write_to_temp_dbfs(df, dataset_name)

            return (df,)

        else:
            # Get dataframes
            tuple_of_dataframes = tuple(self.fetch_dataset_from_name(dataset) for dataset in self.datasets)

            # Write to temp dbfs
            for df, dataset_name in zip(tuple_of_dataframes, self.datasets):
                # self.write_to_temp_dbfs(df, dataset_name)
                pass

            return tuple_of_dataframes


if __name__ == "__main__":
    # if loading from files
    task_name = "fetch_sklearn_datasets"
    env_vars = load_and_set_env_vars(env="dev")  # unused
    task_cfg = load_config(task_name)

    # if loading from notebook
    fetcher = SklearnDataFetcher(cfg=cfg)
    fetcher.run_fetch_and_write_to_db()
