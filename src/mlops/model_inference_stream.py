import pyspark.sql.dataframe
from pyspark.sql.functions import col, struct
import mlflow


from src.utils.get_spark import spark
from src.utils.logger_utils import get_logger
from src.common import MetastoreTable

_logger = get_logger()


class ModelInferenceStream:
    """
    Class to execute model inference.
    Apply the model at the specified URI for batch inference on the table with name input_table_name,
    writing results to the table with name output_table_name
    """

    def __init__(self, model_uri: str, input_table: MetastoreTable, output_table: MetastoreTable) -> None:
        """
        Parameters
        ----------
        model_uri : str
            MLflow model uri. Model model must have been logged using the Feature Store API.
        input_table : MetastoreTable
            Table to load as a Spark DataFrame to score the model on.
        output_table : str
            Output table to write results to.
        """
        self.model_uri = model_uri
        self.input_table = input_table
        self.output_table = output_table

    def score_stream(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        """
        Load and apply model from MLflow Model Registry to Spark DataFrame.

        Parameters
        ----------
        df : pyspark.sql.DataFrame
            Spark DataFrame to apply model to.

        Returns
        -------
        pyspark.sql.DataFrame
        """

        return df

    def _load_input_table(self) -> pyspark.sql.DataFrame:
        """
        Load Spark DataFrame containing data for training

        Returns
        -------
        pyspark.sql.DataFrame
        """
        return spark.table(self.input_table.ref)

    def _load_model(self) -> mlflow.pyfunc.PythonModel:
        """
        Load MLflow model from Model Registry

        Returns
        -------
        mlflow.pyfunc.PythonModel
        """
        return mlflow.pyfunc.load_model(self.model_uri)
