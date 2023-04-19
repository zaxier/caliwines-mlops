
 # TODO: Decide if this is the way you want to do it. Otherwise saving for future use. 
import pyspark.sql.dataframe

class CalifHousinFeatureEngineering:

    def __init__(self, data):

        self.data = data

    def _drop_features(self):

        self.data = self.data.drop(['total_rooms', 'total_bedrooms', 'population', 'households'], axis=1)

        return self.data

    
    def _rename_california_housing_columns(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        dic = {
            "MedInc": "median_income",
            "HouseAge": "median_house_age",
            "housing_median_age": "median_house_age",
            "AveRooms": "average_rooms",
            "AveBedrms": "average_bedrooms",
            "Population": "population",
            "AveOccup": "average_occupancy",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "MedHouseVal": "median_house_value",
        }
        return self.rename_columns_with_dict(df=df, column_mapping=dic)

    def _add_features(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        df = df.pandas_api()

        df['average_rooms'] = df['total_rooms'] / df['households']
        df['average_bedrooms'] = df['total_bedrooms'] / df['households']
        df['average_occupancy'] = df['population'] / df['households']
        df['median_house_value'] = df['median_house_value'] / 100000

        return df.to_spark()

    def _california_housing_csv_pipeline(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        _logger.info("Running 'california_housing_csv' transformation pipeline")
        _logger.info("Renaming columns for 'california_housing_csv'")
        df = self._rename_california_housing_columns(df=df)
        _logger.info("Engineering new features for 'california_housing_csv'")
        df = self._add_features(df=df)
        _logger.info("Creating unique identifier for 'california_housing_csv'")
        # df = self.__create_row_sha(df=df, cols=['median_income', 'median_house_age', 'average_rooms', 'average_bedrooms', 'population', 'average_occupancy', 'latitude', 'longitude', 'median_house_value'])
        df = self.create_row_hash(df=df, cols=['median_income', 'median_house_age', 'population', 'latitude', 'longitude', 'median_house_value'])
        return df

    def _california_housing_pipeline(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        _logger.info("Running 'california_housing' transformation pipeline")
        _logger.info("Renaming columns for 'california_housing'")
        df = self._rename_california_housing_columns(df=df)
        _logger.info("Creating unique identifier for 'california_housing'")
        # df = self.__create_row_sha(df=df, cols=['median_income', 'median_house_age', 'average_rooms', 'average_bedrooms', 'population', 'average_occupancy', 'latitude', 'longitude', 'median_house_value'])
        df = self.create_row_hash(df=df, cols=['median_income', 'median_house_age', 'population', 'latitude', 'longitude', 'median_house_value'])
        return df

    def _transform_pipeline(self, df: pyspark.sql.DataFrame, dataset_name: str) -> pyspark.sql.DataFrame:
        """
        Run the dataset specific pipeline

        Parameters
        ----------
        df : pyspark.sql.DataFrame
            The dataframe to run the pipeline on
        dataset_name : str
            The name of the dataset to run the pipeline for

        Returns
        -------
        pyspark.sql.DataFrame
            The dataframe after running the pipeline
        """
        if dataset_name == 'california_housing':
            df = self._california_housing_pipeline(df=df)
        elif dataset_name == 'california_housing_csv':
            df = self._california_housing_csv_pipeline(df=df)
        
        return df

    def transform(self):

        self.data = self._add_features()

        self.data = self._drop_features()

        return self.data


