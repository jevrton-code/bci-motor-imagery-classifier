"""bci_mi_classifier - reproducible EEG motor imagery classification package.

Version 0.1 (foundation / scaffold).

This package provides the planned structure for a small, reproducible
brain-computer interface (BCI) benchmark that classifies left-hand vs
right-hand motor imagery from public EEG data using MOABB, the PhysionetMI
dataset, the LeftRightImagery paradigm, and classical machine-learning
baselines (primarily CSP+LDA).

At version 0.1 the modules in this package are documented stubs: they
describe planned responsibilities and function/class signatures but contain
no benchmark implementation logic. No benchmark has been run and no data has
been downloaded.

Planned modules:
    config         - version 1 constants and configuration.
    datasets       - MOABB PhysionetMI access and subject selection.
    pipelines      - classical scikit-learn pipelines (CSP+LDA, etc.).
    evaluation     - within-session MOABB evaluation orchestration.
    results        - result-table schema validation and aggregation.
    visualization  - figures (per-subject, pipeline comparison, distribution).
"""

__version__ = "0.1.0"

__all__ = [
    "__version__",
]
