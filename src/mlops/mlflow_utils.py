from dataclasses import dataclass


@dataclass
class MLflowTrackingConfig:
    """
    Configuration data class used to unpack MLflow parameters during a model training run.

    Attributes:
        run_name (str)
            Name of MLflow run
        experiment_id (int)
            ID of the MLflow experiment to be activated. If an experiment with this ID does not exist, raise an exception.
        experiment_path (str)
            Case sensitive name of the experiment to be activated. If an experiment with this name does not exist,
            a new experiment wth this name is created.
        model_name (str)
            Name of the registered model under which to create a new model version. If a registered model with the given
            name does not exist, it will be created automatically.
    """

    run_name: str
    experiment_id: int = None
    experiment_path: str = None
    model_name: str = None
