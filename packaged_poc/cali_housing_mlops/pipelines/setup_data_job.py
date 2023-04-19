# setup_data_job.py
#  `conf/cali_housing_mlops/pipelines/setup_data.yaml`

from packaged_poc.cali_housing_mlops.setup_data import (
    SetupCaliHousingMLops,
    SetupCaliHousingMLopsConfig,
)
from packaged_poc.common import Workload, MetastoreTable


class SetupCaliHousingMLopsJob(Workload):
    """
    1. Check if table exists
    2. If table exists, do nothing
    3. If table does not exist, fetch data and write to catalog w/ Delta format
    """

    def _get_config(self):
        catalog = self.env_vars["setup_data_catalog"]
        holdout_pct = self.conf["holdout_pct"]
        random_seed = self.conf["random_seed"]

        cfg = SetupCaliHousingMLopsConfig(
            train_table=MetastoreTable(catalog=catalog, schema="cali_housing_mlops", table="training_data"),
            holdout_table=MetastoreTable(catalog=catalog, schema="cali_housing_mlops", table="holdout_data"),
            holdout_pct=holdout_pct,
            random_seed=random_seed,
        )
        return cfg

    def launch(self):
        self.logger.info("Launching SetupCaliHousingMLopsJob job")
        cfg = self._get_config()
        SetupCaliHousingMLops(cfg=cfg).run()
        self.logger.info("SetupCaliHousingMLopsJob finished!")


# if you're using python_wheel_task, you'll need the entrypoint function to be used in setup.py '
def entrypoint():  # pragma: no cover
    task = SetupCaliHousingMLopsJob()
    task.launch()


# if you're using spark_python_task, you'll need the __main__ block to start the code execution
if __name__ == "__main__":
    entrypoint()
