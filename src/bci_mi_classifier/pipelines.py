"""Classical classification pipelines.

Responsibility:
    Build scikit-learn compatible pipelines for the version 1 benchmark. Every
    supervised transform (e.g. CSP) must live inside the pipeline so it is fit
    only on training folds during cross-validation, preventing leakage.

Version 1 pipelines:
    - CSP+LDA          : primary classical motor imagery baseline.
    - Dummy / chance   : optional sanity-check baseline (~0.5 ROC-AUC).
    - LogVariance+LDA  : optional simple feature baseline.

Deferred (not in version 1):
    - Riemannian geometry pipelines (e.g. Covariance+MDM, TangentSpace+LR).
    - Deep learning.

References:
    - MNE CSP: https://mne.tools/stable/generated/mne.decoding.CSP.html
    - scikit-learn LDA:
      https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html
"""

from __future__ import annotations

from typing import Any

from . import config


def build_csp_lda(n_components: int | None = None) -> Any:
    """Build the primary CSP+LDA pipeline.

    Composes ``mne.decoding.CSP`` (with a fixed, documented component count from
    ``config.N_CSP_COMPONENTS``) followed by scikit-learn's
    ``LinearDiscriminantAnalysis`` in a single ``Pipeline``. CSP is a supervised
    transform and lives inside the pipeline so it is fit only on training folds
    during cross-validation.

    Args:
        n_components: Number of CSP components. Defaults to
            ``config.N_CSP_COMPONENTS``.

    Returns:
        A scikit-learn ``Pipeline`` (CSP -> LDA).
    """
    from mne.decoding import CSP
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.pipeline import Pipeline

    if n_components is None:
        n_components = config.N_CSP_COMPONENTS

    csp = CSP(n_components=n_components, reg=None, log=True, norm_trace=False)
    lda = LinearDiscriminantAnalysis()
    return Pipeline([("CSP", csp), ("LDA", lda)])


def build_dummy() -> Any:
    """Build the optional chance/dummy baseline pipeline.

    Wraps scikit-learn's ``DummyClassifier`` (stratified strategy) so that mean
    binary ROC-AUC is near the 0.5 chance level, providing a sanity-check
    reference. The 2D ``DummyClassifier`` is fronted by a flattening step so it
    accepts the 3D ``(trials, channels, times)`` epochs arrays MOABB provides.

    Returns:
        A scikit-learn ``Pipeline`` (flatten -> DummyClassifier).
    """
    from sklearn.dummy import DummyClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import FunctionTransformer

    flatten = FunctionTransformer(
        _flatten_epochs, validate=False, feature_names_out=None
    )
    dummy = DummyClassifier(strategy="stratified", random_state=config.RANDOM_STATE)
    return Pipeline([("flatten", flatten), ("dummy", dummy)])


def _flatten_epochs(X: Any) -> Any:
    """Reshape ``(trials, channels, times)`` arrays to ``(trials, features)``."""
    import numpy as np

    arr = np.asarray(X)
    if arr.ndim <= 2:
        return arr
    return arr.reshape(arr.shape[0], -1)


def build_logvar_lda() -> Any:
    """Build the optional LogVariance+LDA pipeline.

    Composes a log-variance band-power feature transform with
    ``LinearDiscriminantAnalysis`` as a simple comparison baseline. Deferred for
    version 0.2; provided for completeness and not registered by default.

    Returns:
        A scikit-learn ``Pipeline`` (log-variance -> LDA).
    """
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import FunctionTransformer

    logvar = FunctionTransformer(
        _log_variance, validate=False, feature_names_out=None
    )
    lda = LinearDiscriminantAnalysis()
    return Pipeline([("logvar", logvar), ("LDA", lda)])


def _log_variance(X: Any) -> Any:
    """Log of per-channel temporal variance for each trial."""
    import numpy as np

    arr = np.asarray(X)
    return np.log(np.var(arr, axis=-1) + 1e-12)


def build_pipelines(include_dummy: bool = False) -> dict[str, Any]:
    """Return the mapping of pipeline name to estimator for the benchmark.

    CSP+LDA is always included as the primary version 0.2 baseline. The
    chance/dummy baseline is optional (off by default for the headline run);
    LogVariance+LDA and Riemannian pipelines are deferred.

    Args:
        include_dummy: If ``True``, also register the chance/dummy baseline.

    Returns:
        Mapping of pipeline name to scikit-learn compatible estimator.
    """
    pipelines: dict[str, Any] = {"CSP+LDA": build_csp_lda()}
    if include_dummy:
        pipelines["Dummy"] = build_dummy()
    return pipelines
