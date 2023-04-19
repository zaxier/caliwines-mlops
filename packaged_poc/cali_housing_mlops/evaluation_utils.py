from typing import Dict
import pandas as pd
from sklearn.metrics import roc_auc_score, r2_score


class ModelEvaluation:

    @staticmethod
    def _roc_auc_score(y_true: pd.Series, y_score: pd.Series):
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
        return roc_auc_score(y_true=y_true,
                             y_score=y_score,
                             average='weighted',
                             multi_class='ovo')

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
    

    def evaluate(self, y_true: pd.Series, y_score: pd.Series, metric_prefix: str = '') -> Dict:
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
        # return {
        #     f'{metric_prefix}roc_auc_score': self._roc_auc_score(y_true, y_score),
        # }

        return {
            f'{metric_prefix}r2_score': self._r2_score(y_true, y_score),
        }
