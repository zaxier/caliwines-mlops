from typing import Dict
import pandas as pd
from sklearn.metrics import roc_auc_score, r2_score, f1_score, accuracy_score, mean_squared_error, mean_absolute_error


class ModelEvaluation:
    """
    Class for computing evaluation metrics for a model.
    """

    def __init__(self, model_type: str):
        """
        Parameters
        ----------
        model_type : str
            Type of model to evaluate. Supported model types are "multiclass_classification" and "regression".
        """
        self.model_type = model_type

    @staticmethod
    def _r2_score(y_true: pd.Series, y_score: pd.Series):
        """
        Compute R2 score using sklearn. Computed in same way as MLflow utils
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html

        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
            True labels or binary label indicators
        y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
            Target scores.

        Returns
        -------
        r2 : float
        """
        return r2_score(y_true=y_true, y_pred=y_score)

    @staticmethod
    def _root_mean_squared_error(y_true: pd.Series, y_score: pd.Series):
        """
        Compute MSE score using sklearn. Computed in same way as MLflow utils
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html

        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
            True labels or binary label indicators
        y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
            Target scores.

        Returns
        -------
        rmse : float
        """
        return mean_squared_error(y_true=y_true, y_pred=y_score, squared=False)

    @staticmethod
    def _mean_squared_error(y_true: pd.Series, y_score: pd.Series):
        """
        Compute MSE score using sklearn. Computed in same way as MLflow utils
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html

        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
            True labels or binary label indicators
        y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
            Target scores.

        Returns
        -------
        mse : float
        """
        return mean_squared_error(y_true=y_true, y_pred=y_score, squared=True)

    @staticmethod
    def _mean_absolute_error(y_true: pd.Series, y_score: pd.Series):
        """
        Compute MAE score using sklearn. Computed in same way as MLflow utils
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html

        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
            True labels or binary label indicators
        y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
            Target scores.

        Returns
        -------
        mae : float
        """
        return mean_absolute_error(y_true=y_true, y_pred=y_score)

    @staticmethod
    def _roc_auc_ovo_weighted(y_true: pd.Series, y_score: pd.Series):
        """
        Compute ROC AUC score using sklearn. Computed in same way as MLflow utils
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html
        By default, for roc_auc_score, we pick `average` to be `weighted`, `multi_class` to be `ovo`,
        to make the output more insensitive to dataset imbalance.

        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
            True labels or binary label indicators
        y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
            Target scores.

        Returns
        -------
        auc : float
        """
        return roc_auc_score(y_true=y_true, y_score=y_score, average="weighted", multi_class="ovo")

    @staticmethod
    def _f1_weighted(y_true: pd.Series, y_score: pd.Series):
        """
        Compute F1 score using sklearn. Computed in same way as MLflow utils
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
        By default, for f1_score, we pick `average` to be `weighted`, to make the output more insensitive to dataset imbalance.

        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
            True labels or binary label indicators
        y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
            Target scores.

        Returns
        -------
        f1 : float
        """
        return f1_score(y_true=y_true, y_pred=y_score, average="weighted")

    @staticmethod
    def _accuracy_score(y_true: pd.Series, y_score: pd.Series):
        """
        Compute accuracy score using sklearn. Computed in same way as MLflow utils
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html

        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
            True labels or binary label indicators
        y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
            Target scores.

        Returns
        -------
        accuracy : float
        """
        return accuracy_score(y_true=y_true, y_pred=y_score)

    def _evaluate_regression(self, y_true: pd.Series, y_score: pd.Series, metric_prefix: str = "") -> Dict:
        """
        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
            True labels or binary label indicators
        y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
            Target scores.
        metric_prefix : str
            Prefix for each metric key in the returned dictionary

        Returns
        -------
        Dictionary of (metric name, computed value)
        """

        return {
            f"{metric_prefix}r2_score": self._r2_score(y_true, y_score),
            f"{metric_prefix}root_mean_squared_error": self._root_mean_squared_error(y_true, y_score),
            f"{metric_prefix}mean_squared_error": self._mean_squared_error(y_true, y_score),
            f"{metric_prefix}mean_absolute_error": self._mean_absolute_error(y_true, y_score),
        }

    def _evaluate_multiclass_classification(
        self, y_true: pd.Series, y_score: pd.Series, metric_prefix: str = ""
    ) -> Dict:
        """
        Parameters
        ----------
        y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
            True labels or binary label indicators
        y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
            Target scores.
        metric_prefix : str
            Prefix for each metric key in the returned dictionary

        Returns
        -------
        Dictionary of (metric name, computed value)
        """
        return {
            f"{metric_prefix}roc_auc_score": self._roc_auc_ovo_weighted(y_true, y_score),
            f"{metric_prefix}f1_score": self._f1_weighted(y_true, y_score),
            f"{metric_prefix}accuracy_score": self._accuracy_score(y_true, y_score),
        }

    def evaluate(self, y_true: pd.Series, y_score: pd.Series, metric_prefix: str = "") -> Dict:
        """
        Evaluate model performance on validation data.

        Returns
        -------
        Dictionary of (metric name, computed value)
        """
        if self.model_type == "multiclass_classification":
            return self._evaluate_multiclass_classification(y_true, y_score, metric_prefix)

        elif self.model_type == "regression":
            return self._evaluate_regression(y_true, y_score, metric_prefix)

        else:
            raise NotImplementedError


if __name__ == "__main__":
    print("ModelEvaluation")
    print(ModelEvaluation()._evaluate_regression(pd.Series([1, 2, 3]), pd.Series([1, 2, 3])))
    print(ModelEvaluation()._evaluate_regression(pd.Series([1, 2, 3]), pd.Series([1, 2, 3]), "test_"))
