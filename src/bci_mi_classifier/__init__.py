"""bci_mi_classifier - reproducible EEG motor imagery classification package.

Version 0.4 (within-session multi-pipeline baselines with analysis + figures).

This package provides a small, reproducible brain-computer interface (BCI)
benchmark that classifies left-hand vs right-hand motor imagery from public EEG
data using MOABB, the PhysionetMI dataset, the LeftRightImagery paradigm, and
classical machine-learning baselines (primarily CSP+LDA).

As of version 0.4 all benchmark modules are implemented. A within-session run
of CSP+LDA, Dummy, and LogVariance+LDA on subjects 1-10 can be executed via
``scripts/run_baseline.py``, and the aggregate summary table and figures can be
produced from the saved results via ``scripts/run_analysis.py``.

Modules:
    config         - benchmark constants and configuration.
    datasets       - MOABB PhysionetMI access and subject selection.
    pipelines      - classical scikit-learn pipelines (CSP+LDA, etc.).
    evaluation     - within-session MOABB evaluation orchestration.
    results        - result-table schema, validation, aggregation, and saving.
    visualization  - figures (per-subject, pipeline comparison, distribution).
"""

__version__ = "0.4.0"

__all__ = [
    "__version__",
]
