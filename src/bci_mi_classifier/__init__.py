"""bci_mi_classifier - reproducible EEG motor imagery classification package.

Version 1.0 (GitHub-ready classical within-session baseline benchmark).

This package provides a small, reproducible brain-computer interface (BCI)
benchmark that classifies left-hand vs right-hand motor imagery from public EEG
data using MOABB, the PhysionetMI dataset, the LeftRightImagery paradigm, and
classical machine-learning baselines (CSP+LDA, Dummy, LogVariance+LDA).

As of version 1.0 all benchmark modules are implemented and documented. A
within-session run of three pipelines on subjects 1-10 can be executed via
``scripts/run_baseline.py``, and the aggregate summary table, figures, and
report artifacts can be produced via ``scripts/run_analysis.py`` and
``reports/bci_motor_imagery_report.md``.

Modules:
    config         - benchmark constants and configuration.
    datasets       - MOABB PhysionetMI access and subject selection.
    pipelines      - classical scikit-learn pipelines (CSP+LDA, etc.).
    evaluation     - within-session MOABB evaluation orchestration.
    results        - result-table schema, validation, aggregation, and saving.
    visualization  - figures (per-subject, pipeline comparison, distribution).
"""

__version__ = "1.0.0"

__all__ = [
    "__version__",
]
