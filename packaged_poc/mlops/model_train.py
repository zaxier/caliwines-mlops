from dataclasses import dataclass
from typing import Callable, List, Union, Dict, Any
import pprint

import pyspark.sql.dataframe
import sklearn
from sklearn.model_selection import train_test_split
import pandas as pd
import mlflow
from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient

from packaged_poc.common import MetastoreTable
from packaged_poc.utils.logger_utils import get_logger
from packaged_poc.utils.get_spark import spark
from packaged_poc.utils.notebook_utils import load_and_set_env_vars, load_config
from packaged_poc.mlops.cali_housing_model import (
    CaliHousingModelPipeline,
)
from packaged_poc.mlops.mlflow_utils import MLflowTrackingConfig

_logger = get_logger()


@dataclass
class ModelTrainConfig:
    """
    Configuration data class used to execute ModelTrain pipeline.

    Attributes:
        mlflow_tracking_cfg (MLflowTrackingConfig)
            Configuration data class used to unpack MLflow parameters during a model training run.
        pipeline_params (dict):
            Params to use in preprocessing pipeline. Read from model_train.yml
            - test_size: Proportion of input data to use as training data
            - random_state: Random state to enable reproducible train-test split
        model_params (dict):
            Dictionary of params for model. Read from model_train.yml
        conf (dict):
            [Optional] dictionary of conf file used to trigger pipeline. If provided will be tracked as a yml
            file to MLflow tracking.
        env_vars (dict):
            [Optional] dictionary of environment variables to trigger pipeline. If provided will be tracked as a yml
            file to MLflow tracking.
    """

    mlflow_tracking_cfg: MLflowTrackingConfig
    train_table: MetastoreTable
    label_col: str
    pipeline_params: Dict[str, Any]
    model_params: Dict[str, Any]
    conf: Dict[str, Any] = None
    env_vars: Dict[str, str] = None


class ModelTrain:
    """
    Class to train a model on a given dataset and log results to MLflow.

    Attributes:
        cfg (ModelTrainConfig):
            Configuration data class used to execute ModelTrain pipeline.

    Methods:
        run():
            Execute ModelTrain pipeline.
    """

    def __init__(self, cfg: ModelTrainConfig):
        self.cfg = cfg

    @staticmethod
    def _set_experiment(mlflow_tracking_cfg: MLflowTrackingConfig):
        """
        Set MLflow experiment. Use one of either experiment_id or experiment_path
        """
        if mlflow_tracking_cfg.experiment_id is not None:
            _logger.info(f"MLflow experiment_id: {mlflow_tracking_cfg.experiment_id}")
            mlflow.set_experiment(experiment_id=mlflow_tracking_cfg.experiment_id)
        elif mlflow_tracking_cfg.experiment_path is not None:
            _logger.info(f"MLflow experiment_path: {mlflow_tracking_cfg.experiment_path}")
            mlflow.set_experiment(experiment_name=mlflow_tracking_cfg.experiment_path)
        else:
            raise RuntimeError("MLflow experiment_id or experiment_path must be set in mlflow_params")

    def create_train_test_split(self, df: pyspark.sql.dataframe.DataFrame):
        """
        Create train-test split of data
        """
        label_col = self.cfg.label_col
        X = df.drop(label_col, axis=1)
        y = df[label_col]
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=self.cfg.pipeline_params["test_size"],
            random_state=self.cfg.pipeline_params["random_state"],
        )
        return X_train, X_test, y_train, y_test

    def fit_pipeline(self, X_train: pd.DataFrame, y_train: pd.Series) -> sklearn.pipeline.Pipeline:
        """
        Create sklearn pipeline and fit pipeline.

        Parameters
        ----------
        X_train : pd.DataFrame
            Training data

        y_train : pd.Series
            Training labels

        Returns
        -------
        scikit-learn pipeline with fitted steps.
        """
        _logger.info("Creating sklearn pipeline...")
        pipeline = CaliHousingModelPipeline.create_train_pipeline(self.cfg.model_params)

        _logger.info("Fitting sklearn RandomForestClassifier...")
        _logger.info(f"Model params: {pprint.pformat(self.cfg.model_params)}")
        model = pipeline.fit(X_train, y_train)

        return model

    def run(self):
        """
        Run ModelTrain pipeline. TODO: Add more details
        """

        _logger.info("Setting MLflow experiment...")
        mlflow_tracking_cfg: MLflowTrackingConfig = self.cfg.mlflow_tracking_cfg
        train_table: MetastoreTable = self.cfg.train_table

        self._set_experiment(mlflow_tracking_cfg)
        mlflow.sklearn.autolog(log_input_examples=True, silent=True)

        _logger.info("Starting MLflow run...")
        with mlflow.start_run(run_name=mlflow_tracking_cfg.run_name) as run:
            _logger.info(f"MLflow run_id: {run.info.run_id}")

            # Log config files
            if self.cfg.conf is not None:
                mlflow.log_dict(self.cfg.conf, artifact_file="model_train_conf.yml")
            if self.cfg.env_vars is not None:
                mlflow.log_dict(self.cfg.env_vars, artifact_file="model_train_env_vars.yml")

            # Load data
            _logger.info(f"Loading data from table: '{train_table.ref}'")
            data = spark.table(train_table.ref).toPandas()

            # Create train-test split
            X_train, X_test, y_train, y_test = self.create_train_test_split(data)

            # Fit pipeline
            model = self.fit_pipeline(X_train, y_train)

            # Log model
            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                input_example=X_train.iloc[:10],
                signature=infer_signature(X_train, y_train),
            )

            # Log model params
            mlflow.log_params(self.cfg.model_params)

            # Log model metrics
            mlflow.log_metrics({"test_r2": model.score(X_test, y_test)})

            # Register model to MLflow Model Registry if provided
            if self.cfg.mlflow_tracking_cfg.model_name is not None:
                _logger.info(f"Registering model as: {mlflow_tracking_cfg.model_name}")
                model_details = mlflow.register_model(
                    f"runs:/{run.info.run_id}/model",
                    name=mlflow_tracking_cfg.model_name,
                )
                client = MlflowClient()
                model_version_details = client.get_model_version(
                    name=mlflow_tracking_cfg.model_name, version=model_details.version
                )

                _logger.info(f"Transitioning model: {mlflow_tracking_cfg.model_name} to Staging")
                client.transition_model_version_stage(
                    name=mlflow_tracking_cfg.model_name,
                    version=model_details.version,
                    stage="Staging",
                )
