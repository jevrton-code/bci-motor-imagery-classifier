"""Classical classification pipelines (planned, stub only).

Planned responsibility:
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


def build_csp_lda(n_components: int | None = None) -> Any:
    """Build the primary CSP+LDA pipeline.

    Planned behavior:
        Compose ``mne.decoding.CSP`` (with a fixed, documented component count
        from ``config.N_CSP_COMPONENTS``) followed by scikit-learn's
        ``LinearDiscriminantAnalysis`` in a single ``Pipeline``.

    Args:
        n_components: Number of CSP components. Defaults to
            ``config.N_CSP_COMPONENTS``.

    Returns:
        A scikit-learn compatible estimator/pipeline.
    """
    raise NotImplementedError("version 0.1 scaffold: CSP+LDA pipeline deferred")


def build_dummy() -> Any:
    """Build the optional chance/dummy baseline pipeline.

    Planned behavior:
        Wrap scikit-learn's ``DummyClassifier`` so that mean binary ROC-AUC is
        near the 0.5 chance level, providing a sanity-check reference.

    Returns:
        A scikit-learn compatible estimator/pipeline.
    """
    raise NotImplementedError("version 0.1 scaffold: dummy baseline deferred")


def build_logvar_lda() -> Any:
    """Build the optional LogVariance+LDA pipeline.

    Planned behavior:
        Compose a band-power / log-variance feature transform with
        ``LinearDiscriminantAnalysis`` as a simple comparison baseline.

    Returns:
        A scikit-learn compatible estimator/pipeline.
    """
    raise NotImplementedError("version 0.1 scaffold: LogVariance+LDA deferred")


def build_pipelines() -> dict[str, Any]:
    """Return the mapping of pipeline name to estimator for the benchmark.

    Planned behavior:
        Assemble the version 1 pipelines into a dict consumed by the MOABB
        evaluation. CSP+LDA is always included; dummy and LogVariance+LDA are
        optional.

    Returns:
        Mapping of pipeline name to scikit-learn compatible estimator.
    """
    raise NotImplementedError("version 0.1 scaffold: pipeline registry deferred")
