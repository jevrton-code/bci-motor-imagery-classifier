"""bci_mi_classifier - reproducible EEG motor imagery classification package.

Version 0.2 (first within-session CSP+LDA benchmark).

This package provides a small, reproducible brain-computer interface (BCI)
benchmark that classifies left-hand vs right-hand motor imagery from public EEG
data using MOABB, the PhysionetMI dataset, the LeftRightImagery paradigm, and
classical machine-learning baselines (primarily CSP+LDA).

As of version 0.2 the dataset, pipeline, evaluation, and result modules are
implemented and a within-session CSP+LDA run on subjects 1-10 can be executed
via ``scripts/run_baseline.py``. The ``visualization`` module remains a
documented stub, scheduled for version 0.3 (result analysis and figures).

Modules:
    config         - version 0.2 constants and configuration.
    datasets       - MOABB PhysionetMI access and subject selection.
    pipelines      - classical scikit-learn pipelines (CSP+LDA, etc.).
    evaluation     - within-session MOABB evaluation orchestration.
    results        - result-table schema, validation, aggregation, and saving.
    visualization  - figures (per-subject, pipeline comparison, distribution);
                     deferred to version 0.3.
"""

__version__ = "0.2.0"

__all__ = [
    "__version__",
]
