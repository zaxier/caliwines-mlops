from sklearn.compose import make_column_selector as selector, ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


class RandomForestPipelines:
    @classmethod
    def simple_rf_classifier(cls, model_params: dict) -> Pipeline:
        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "numeric_transformer",
                    SimpleImputer(strategy="median"),
                    selector(dtype_exclude="object"),
                ),
                (
                    "categorical_transformer",
                    OneHotEncoder(handle_unknown="ignore"),
                    selector(dtype_include="object"),
                ),
            ],
            remainder="passthrough",
            sparse_threshold=0,
        )

        rf_classifier = RandomForestClassifier(**model_params)

        pipeline = Pipeline(
            [
                ("preprocessor", preprocessor),
                ("classifier", rf_classifier),
            ]
        )

        return pipeline

    @classmethod
    def simple_rf_regressor(cls, model_params: dict) -> Pipeline:
        """
        Returns a model training pipeline for training random forest regressor.
        """
        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, selector(dtype_exclude="object")),
                ("cat", categorical_transformer, selector(dtype_include="object")),
            ],
            remainder="passthrough",
            sparse_threshold=0,
        )

        rf_regressor = RandomForestRegressor(**model_params)

        pipeline = Pipeline(
            [
                ("preprocessor", preprocessor),
                ("regressor", rf_regressor),
            ]
        )
        return pipeline
