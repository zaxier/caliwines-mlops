from dataclasses import dataclass
from typing import Dict, Any, Union, List

import pyspark.sql.dataframe
import pandas as pd
from sklearn.datasets import fetch_california_housing

from packaged_poc.utils.get_spark import spark
from packaged_poc.utils.logger_utils import get_logger

_logger = get_logger()


@dataclass
class CaliforniaHousingETLConfig:
    """
    Configuration for CaliforniaHousingETL
    """

    attr_string1: str = "default"
    attr_str_or_list_of_str: Union[str, List[str]] = "default"
    attr_int1: int = 1


class CaliforniaHousing:
    """
    A stylistic change to the charming_afro SampleETL(Task)
    """

    def __init__(self, cfg: CaliforniaHousingETLConfig) -> None:
        self.cfg = cfg

    @staticmethod
    def setup(database_name: str) -> None:
        """
        Set up database to use. Create the database {database_name} if it doesn't exist

        Parameters
        ----------
        database_name : str
            Database to create if it doesn't exist. Otherwise use database of the name provided
        """
        _logger.info(f"Creating database {database_name} if not exists")
        spark.sql(f"CREATE DATABASE IF NOT EXISTS {database_name};")
        spark.sql(f"USE {database_name};")

    @staticmethod
    def get_calif_housing_df() -> pyspark.sql.DataFrame:
        try:
            # Try to fetch the dataset from the database
            # import TableReference TODO:
            table_ref = TableReference("catalog", "xaviertest", "tablename1")
            df = spark.sql("SELECT * FROM california_housing")
        except:
            # If it doesn't exist, fetch it from sklearn
            _data: pd.DataFrame = fetch_california_housing(as_frame=True).frame
            df = spark.createDataFrame(_data)
            _logger.info("Returning California Housing dataframe via Sklearn")
        return df

    def _overwrite_table_hardcoded(self, df: pyspark.sql.DataFrame) -> None:
        db = "xaviertest"
        table = "tablename1"
        df.write.format("delta").mode("overwrite").saveAsTable(f"{db}.{table}")

    def _example_resolve_config(self) -> None:
        attr_string1 = self.cfg.attr_string1
        attr_str_or_list_of_str = self.cfg.attr_str_or_list_of_str
        attr_int1 = self.cfg.attr_int1

        if isinstance(attr_str_or_list_of_str, str):
            pass
        elif isinstance(attr_str_or_list_of_str, list):
            pass
        else:
            raise RuntimeError(" of either str of list type")

        pass

    def _example_write_data_to_dbfs(self, df: pyspark.sql.DataFrame) -> None:
        """
        Write a dataframe to dbfs
        """
        pass

    def run(self):
        """
        Run Housing ETL
        """
        _logger.info("=========== First Step ===========")
        df = self.get_calif_housing_df()
        _logger.info("=========== Second Step ===========")
        self._overwrite_table_hardcoded(df)
        _logger.info("=========== Third Step ===========")

        _logger.info("=========== Fourth Step ===========")

        pass


if __name__ == "__main__":
    task_name = ""
