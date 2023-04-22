from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import Dict, Any
import yaml
import pathlib
from pyspark.sql import SparkSession
import sys
from logging import Logger
import dotenv
import os

from src.utils.logger_utils import get_logger
from src.utils.get_spark import spark

# TODO: Establish logging standard
_logger = get_logger()


class MetastoreTable:
    """
    Class representing a table in the Unity Catalog Metastore. This class is used to reference tables,
    and perform operations on them. It is not a Spark DataFrame, a PySpark DataFrame, or a Pandas DataFrame.
    It offers functionality such as:
    - Checking that the table exists
    - Describing the table
    - Describing the table history
    - Describing the table extended
    - Read the table as a Spark DataFrame
    """

    def __init__(self, catalog: str, schema: str, table: str) -> None:
        self.catalog = catalog
        self.schema = schema
        self.name = table
        self.table = table
        self.ref = self._get_ref()
        self.short_ref = self._get_short_ref()

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}({self.ref})"

    @classmethod
    def from_string(cls, ref: str) -> "MetastoreTable":
        """
        Alternative constructor to initialise a TableReference object from a string.
        """
        cat, schema, table = ref.split(".")
        return cls(cat, schema, table)

    def check_exists(self) -> bool:
        MetastoreCatalog(self.catalog).set()
        return spark.catalog.tableExists(self.short_ref)

    def drop(self) -> None:
        try:
            spark.sql(f"DROP TABLE {self.ref}")
            print(f"NOTE: Dropped table '{self.ref}' from Unity Metastore\n-----")
        except Exception as e:
            print(f"NOTE: Could not drop table '{self.ref}' from Unity Metastore\n-----")

    def _create_basic_table(self, comment: str = "") -> None:
        """
        Function to create a basic table at self.ref
        """
        spark.sql(
            f"""
        CREATE TABLE {self.ref}  
            (id INT, name STRING, value DOUBLE);  
        """
        )

        spark.sql(
            f"""
        INSERT INTO {self.ref}
            VALUES (1, "Yve", 1.0), 
                (2, "Omar", 2.5), 
                (3, "Elia", 3.3)
        """
        )

    def _create(self, comment: str = "") -> None:
        """
        Function to create a table in the catalog. Not intended to be used other than to create a table with the name.
        Most of the time you'll be creating tables directly in your code and won't need this function.
        """
        spark.sql(
            f"""
            CREATE TABLE {self.ref}
            USING DELTA
            COMMENT '{comment}'
            """
        )

    def describe(self) -> None:
        """
        Function to describe a table in Unity Metastore.
        """
        spark.sql(f"DESC TABLE {self.ref}").display()

    def describe_extended(self) -> None:
        """
        Function to describe a table in Unity Metastore.
        """
        spark.sql(f"DESC EXTENDED {self.ref}").display()

    def describe_history(self) -> None:
        """
        Function to describe a schema in Unity Metastore.
        """
        spark.sql(f"DESC HISTORY {self.ref}").display()

    def read(self):  # noqa
        """
        Function to read a table from the catalog.
        """
        return spark.read.table(self.ref)

    def _get_ref(self) -> str:
        return f"{self.catalog}.{self.schema}.{self.name}"

    def _get_short_ref(self) -> str:
        return f"{self.schema}.{self.name}"

    def _get_checkpoint_location(self) -> str:
        try:
            return self.checkpoint_location
        except AttributeError:
            return f"{self.catalog}.chkpts/{self.schema}/{self.name}"


class MetastoreCatalog:
    """
    Class representing a catalog in the Unity Catalog Metastore. This class is used to reference catalogs
    and perform operations on them. It offers functionality such as:
    - Checking that the catalog exists
    - Creating a catalog
    - Creating a catalog in a managed location
    - Creating a schema in a catalog
    - Describing a catalog
    - Describing a catalog in extended format
    - Dropping a catalog
    - Showing the available schemas in a catalog
    - For demo purposes, creating a catalog in a managed location
    """

    def __init__(self, name) -> None:
        """
        Parameters
        ----------
        name : str
            Name of the catalog
        """
        self.name = name

    def check_exists(self) -> bool:
        """
        Function to check if a catalog exists in Unity Metastore.
        """
        try:
            spark.sql(f"DESC CATALOG {self.name}")
            return True
        except Exception as e:
            return False

    def create(self, comment: str = "") -> None:
        """
        Function to create a catalog in Unity Metastore.
        """
        if self.check_exists():
            _logger.warn(f"Catalog '{self.name}' already exists")
            return
        else:
            _logger.info(f"Creating catalog '{self.name}'")
            spark.sql(f"CREATE CATALOG {self.name} COMMENT '{comment}'")

    def create_schema(self, schema_name: str, comment: str = "") -> None:
        """
        Function to create a schema in the catalog.
        """
        self.set()
        _logger.info(f"Creating schema '{schema_name}' in catalog '{self.name}'")
        spark.sql(f"CREATE SCHEMA {schema_name} COMMENT '{comment}'")

    def create_managed_external(self, container_uri: str = None, container_dir: str = None, comment: str = "") -> None:
        """
        Function to create a catalog in a managed location in Unity Metastore.
        """
        if self.check_exists():
            _logger.info(f"Catalog '{self.name}' already exists")
            return
        else:
            _logger.info(
                f"Creating catalog '{self.name}' in managed location '{container_uri}/{container_dir}' with comment '{comment}'"
            )

            spark.sql(
                f"""
                CREATE CATALOG IF NOT EXISTS {self.name}
                MANAGED LOCATION '{container_uri}/{container_dir}/'
                COMMENT '{comment}' 
                """
            )

    def demo_create_managed_external_catalog(self) -> None:
        """
        Function for demo purposes.
        """
        self.create_managed_external(
            container_uri="abfss://xavierarmitage-container@oneenvadls.dfs.core.windows.net",
            container_dir="lake23",
            comment="Demo comment",
        )

    def describe(self) -> None:
        """
        Function to describe a catalog in Unity Metastore.
        """
        spark.sql(f"DESC CATALOG {self.name}").display()

    def describe_extended(self) -> None:
        """
        Function to describe a catalog in Unity Metastore.
        """
        spark.sql(f"DESC CATALOG EXTENDED {self.name}").display()

    def drop(self) -> None:
        """
        Function to drop a catalog in Unity Catalog.
        """
        _logger.info(f"Dropping catalog '{self.name}'")
        spark.sql(f"DROP CATALOG IF EXISTS {self.name}")

    def drop_cascade(self) -> None:
        """
        Function to drop a catalog in Unity Catalog.
        """
        _logger.info(f"Dropping catalog '{self.name}'")
        self.drop(cascade=True)

    def drop_schema(self, cascade: bool = False):
        """
        Function to drop a schema in the catalog.
        """
        self.set()
        _logger.info(f"Dropping schema '{self.name}'")
        if cascade:
            spark.sql(f"DROP SCHEMA IF EXISTS {self.name} CASCADE")
        else:
            spark.sql(f"DROP SCHEMA IF EXISTS {self.name}")

    def set(self) -> None:
        """
        Function to set the current catalog.
        """
        spark.sql(f"SET CATALOG {self.name}")

    def show_schemas(self) -> None:
        """
        Function to show schemas in catalog.
        """
        self.set()
        spark.sql("SHOW SCHEMAS").display()


class MetastoreSchema:
    """
    Class to represent a schema in Unity Metastore.
    """

    def __init__(self, catalog: str | MetastoreCatalog, name: str) -> None:
        if isinstance(catalog, MetastoreCatalog):
            self.catalog = catalog.name
        else:
            self.catalog = catalog
        self.name = name
        self.ref = self._get_ref()

    def _set_catalog(self) -> None:
        """
        Function to set the current catalog.
        """
        MetastoreCatalog(self.catalog).set()

    def check_exists(self) -> bool:
        """
        Function to check if a schema exists in Unity Metastore.
        """
        # TODO: There might be a more direct way to do this
        self._set_catalog()
        try:
            spark.sql(f"DESC SCHEMA {self.name}")
            return True
        except Exception as e:
            return False

    def create(self, comment: str = "") -> None:
        """
        Function to create a schema in Unity Metastore.
        """
        self._set_catalog()
        if self.check_exists():
            _logger.warn(f"Schema '{self.name}' already exists")
            return
        else:
            _logger.info(f"Creating schema '{self.name}'")
            spark.sql(f"CREATE SCHEMA {self.name} COMMENT '{comment}'")

    def describe(self) -> None:
        """
        Function to describe a schema in Unity Metastore.
        """
        self._set_catalog()
        spark.sql(f"DESC SCHEMA {self.name}").display()

    def describe_extended(self) -> None:
        """
        Function to describe a schema in Unity Metastore.
        """
        self._set_catalog()
        spark.sql(f"DESC SCHEMA EXTENDED {self.name}").display()

    def drop(self, cascade: bool = False) -> None:
        """
        Function to drop a schema in Unity Metastore.
        """
        self._set_catalog()
        _logger.info(f"Dropping schema '{self.name}'")
        if cascade:
            spark.sql(f"DROP SCHEMA IF EXISTS {self.name} CASCADE")
        else:
            spark.sql(f"DROP SCHEMA IF EXISTS {self.name}")

    def show_tables(self) -> None:
        """
        Function to show tables in schema.
        """
        self._set_catalog()
        spark.sql(f"SHOW TABLES IN {self.name}").display()

    def set(self) -> None:
        """
        Function to set the current schema.
        """
        self._set_catalog()
        _logger.info(f"Setting schema '{self.name}' as current schema")
        spark.sql(f"SET SCHEMA {self.name}")

    def _get_ref(self) -> str:
        return f"{self.catalog}.{self.name}"


class Workload(ABC):
    """
    This is an abstract class that provides handy interfaces to implement workloads (e.g. pipelines or job tasks).
    Create a child from this class and implement the abstract launch method.
    Class provides access to the following useful objects:
    * self.spark is a SparkSession
    * self.dbutils provides access to the DBUtils
    * self.logger provides access to the Spark-compatible logger
    * self.conf provides access to the parsed configuration of the job
    * self.env_vars provides access to the parsed environment variables of the job
    """

    def __init__(self, spark=None, init_conf=None):
        self.spark = self._prepare_spark(spark)
        self.logger = self._prepare_logger()
        self.dbutils = self.get_dbutils()
        if init_conf:
            self.conf = init_conf
        else:
            self.conf = self._provide_config()
        self._log_conf()
        self.env_vars = self.get_env_vars_as_dict()
        self._log_env_vars()

    @staticmethod
    def _prepare_spark(spark) -> SparkSession:
        if not spark:
            return SparkSession.builder.getOrCreate()
        else:
            return spark

    @staticmethod
    def _get_dbutils(spark: SparkSession):
        try:
            from pyspark.dbutils import DBUtils  # noqa

            if "dbutils" not in locals():
                utils = DBUtils(spark)
                return utils
            else:
                return locals().get("dbutils")
        except ImportError:
            return None

    def get_dbutils(self):
        utils = self._get_dbutils(self.spark)

        if not utils:
            self.logger.warn("No DBUtils defined in the runtime")
        else:
            self.logger.info("DBUtils class initialized")

        return utils

    def _provide_config(self):
        self.logger.info("Reading configuration from --conf-file job option")
        conf_file = self._get_conf_file()
        if not conf_file:
            self.logger.info(
                "No conf file was provided, setting configuration to empty dict."
                "Please override configuration in subclass init method"
            )
            return {}
        else:
            self.logger.info(f"Conf file was provided, reading configuration from {conf_file}")
            return self._read_config(conf_file)

    @staticmethod
    def _get_conf_file():
        p = ArgumentParser()
        p.add_argument("--conf-file", required=False, type=str)
        namespace = p.parse_known_args(sys.argv[1:])[0]
        return namespace.conf_file

    @staticmethod
    def _read_config(conf_file) -> Dict[str, Any]:
        config = yaml.safe_load(pathlib.Path(conf_file).read_text())
        return config

    @staticmethod
    def _get_base_data_params():
        p = ArgumentParser()
        p.add_argument("--base-data-params", required=False, type=str)
        namespace = p.parse_known_args(sys.argv[1:])[0]
        return namespace.base_data_params

    @staticmethod
    def _get_env():
        p = ArgumentParser()
        p.add_argument("--env", required=False, type=str)
        namespace = p.parse_known_args(sys.argv[1:])[0]
        return namespace.env

    @staticmethod
    def _set_environ(env_vars):
        dotenv.load_dotenv(env_vars)

    def get_env_vars_as_dict(self):
        base_data_params = self._get_base_data_params()
        self._set_environ(base_data_params)

        env = self._get_env()
        _logger.info(f"Using environment variables from {env}")
        self._set_environ(env)

        return dict(os.environ)

    def _prepare_logger(self) -> Logger:
        log4j_logger = self.spark._jvm.org.apache.log4j  # noqa
        return log4j_logger.LogManager.getLogger(self.__class__.__name__)

    def _log_conf(self):
        # log parameters
        self.logger.info("Launching job with configuration parameters:")
        for key, item in self.conf.items():
            self.logger.info("\t Parameter: %-30s with value => %-30s" % (key, item))

    def _log_env_vars(self):
        # log parameters
        self.logger.info("Using environment variables:")
        for key, item in self.env_vars.items():
            self.logger.info("\t Parameter: %-30s with value => %-30s" % (key, item))

    @abstractmethod
    def launch(self):
        """
        Main method of the job.
        :return:
        """
        pass


def get_dbutils(
    spark: SparkSession,
):  # please note that this function is used in mocking by its name
    try:
        from pyspark.dbutils import DBUtils  # noqa

        if "dbutils" not in locals():
            utils = DBUtils(spark)
            return utils
        else:
            return locals().get("dbutils")
    except ImportError:
        return None
