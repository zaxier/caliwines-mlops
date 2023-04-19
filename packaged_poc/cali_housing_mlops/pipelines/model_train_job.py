from typing import Dict, Any

from packaged_poc.common import Workload, MetastoreTable
from packaged_poc.cali_housing_mlops.model_train import (
    ModelTrainConfig,
    ModelTrain,
    MLflowTrackingConfig,
    TrainTableConfig,
)


class ModelTrainJob(Workload):
    """
    TODO: Add docstring
    """

    def _get_mlflow_tracking_cfg(self) -> MLflowTrackingConfig:
        """ """
        try:
            experiment_id = self.env_vars["model_train_experiment_id"]
        except KeyError:
            experiment_id = None

        try:
            experiment_path = self.env_vars["model_train_experiment_path"]
        except KeyError:
            experiment_path = None

        return MLflowTrackingConfig(
            run_name=self.conf["mlflow_params"]["run_name"],
            experiment_id=experiment_id,
            experiment_path=experiment_path,
            model_name=self.env_vars["model_name"],
        )

    def _get_train_table_cfg(self) -> TrainTableConfig:
        """ """
        table = MetastoreTable(
            catalog=self.env_vars["catalog"],
            schema=self.conf["train_table"]["schema"],
            table=self.conf["train_table"]["table_name"],
        )
        label_col = self.conf["label_col"]
        return TrainTableConfig(table=table, label_col=label_col)

    def _get_model_params(self) -> Dict[str, Any]:
        """ """
        return self.conf["model_params"]

    def _get_pipeline_params(self) -> Dict[str, Any]:
        """ """
        return self.conf["pipeline_params"]

    def _get_train_table_cfg(self) -> MetastoreTable:
        """ """
        return MetastoreTable(
            db_name=self.conf["train_table"]["db_name"],
            table_name=self.conf["train_table"]["table_name"],
        )

    def launch(self):
        self.logger.info("Launching ModelTrainJob...")
        self.logger.info(f"Running ModelTrain pipeline in {self.env_vars['env']} environment...")

        cfg = ModelTrainConfig(
            mlflow_tracking_cfg=self._get_mlflow_tracking_cfg(),
            train_table=self._get_train_table_cfg(),
            pipeline_params=self._get_pipeline_params(),
            model_params=self._get_model_params(),
            conf=self.conf,
            env_vars=self.env_vars,
        )

        ModelTrain(cfg).run()

        self.logger.info("ModelTrainJob completed successfully.")
