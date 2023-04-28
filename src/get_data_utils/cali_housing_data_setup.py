from dataclasses import dataclass

from sklearn.model_selection import train_test_split
import pyspark.sql.dataframe
from typing import List, Tuple

from databricks_common.common import MetastoreTable, MetastoreCatalog, MetastoreSchema
from src.get_data_utils.fetch_sklearn_datasets import SklearnDataFetcher
from src.utils.logger_utils import get_logger

_logger = get_logger()


@dataclass
class SetupCaliHousingConfig:
    train_table: MetastoreTable
    holdout_table: MetastoreTable
    holdout_pct: int
    random_seed: int


class CaliHousingDataSetup:
    """
    Class to grab california housing data from sklearn and split into train and holdout sets.
    """

    def __init__(self, cfg: SetupCaliHousingConfig):
        self.cfg = cfg

    def _setup_metastore_objects(self) -> None:
        _logger.info("Setting up metastore objects...")
        catalogs = [self.cfg.train_table.catalog, self.cfg.holdout_table.catalog]
        schemas = [self.cfg.train_table.schema, self.cfg.holdout_table.schema]
        for catalog in catalogs:
            catalog = MetastoreCatalog(catalog)
            catalog.create_if_not_exists()

        for schema in schemas:
            schema = MetastoreSchema(catalog, schema)
            schema.create_if_not_exists()

    def _separate_holdout_set(self, df: pyspark.sql.DataFrame) -> Tuple[pyspark.sql.DataFrame, pyspark.sql.DataFrame]:
        _logger.info("Separating holdout set...")
        _logger.info(f"Using {self.cfg.holdout_pct}% of data for holdout set")
        holdout_decimal = self.cfg.holdout_pct / 100
        train_df, holdout_df = df.randomSplit([(1 - holdout_decimal), holdout_decimal], seed=self.cfg.random_seed)
        return train_df, holdout_df

    def _fetch_data(self) -> pyspark.sql.DataFrame:
        _logger.info("Fetching california housing data...")
        fetcher = SklearnDataFetcher(datasets=["california_housing"])
        _data = fetcher.run()[0]
        return _data

    def _check_fetch_needed(self, table: MetastoreTable) -> bool:
        if table.check_exists():
            _logger.info("Fetch not needed, table already exists")
            return False
        else:
            _logger.info("Fetch needed, table does not exist")
            return True

    def _setup_tables(self, df: pyspark.sql.DataFrame) -> None:
        _logger.info("Setting up train and holdout tables...")
        train_df, holdout_df = self._separate_holdout_set(df)
        train_df.write.format("delta").mode("overwrite").saveAsTable(self.cfg.train_table.ref)
        holdout_df.write.format("delta").mode("overwrite").saveAsTable(self.cfg.holdout_table.ref)

    def run(self):
        _logger.info("==========Setting up CaliHousing MLOps data assets ==========")

        self._setup_metastore_objects()

        # Check if fetch is needed
        fetch_needed = self._check_fetch_needed(self.cfg.train_table) or self._check_fetch_needed(
            self.cfg.holdout_table
        )

        if fetch_needed:
            _logger.info("Fetch needed...")

            data = self._fetch_data()
            train_data, holdout_data = self._separate_holdout_set(data)
            train_data.write.format("delta").mode("overwrite").saveAsTable(self.cfg.train_table.ref)
            holdout_data.write.format("delta").mode("overwrite").saveAsTable(self.cfg.holdout_table.ref)

        else:
            _logger.info("Fetch not needed, skipping fetch")

        _logger.info("========== Setup for CaliHousing MLOps completed==========")
