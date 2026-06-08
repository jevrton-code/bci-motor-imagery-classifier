"""Project configuration constants for the version 1 benchmark.

This module centralizes the fixed, documented choices for the first
reproducible benchmark so that every script, notebook, and test references a
single source of truth. These are simple module-level constants reflecting the
version 1 scope described in ``docs/`` - they are configuration, not benchmark
logic.

Design rules:
    - Values are intentionally fixed baseline choices for version 1.
    - Hyperparameters (such as the CSP component count) are NOT tuned on test
      results. If tuning is added later it must use nested cross-validation.
    - Changing any value here changes the benchmark definition and should be
      reflected in the documentation and result provenance.
"""

from __future__ import annotations

# --- Dataset and paradigm (MOABB) ----------------------------------------
# MOABB dataset wrapper for the PhysioNet EEG Motor Movement/Imagery Dataset.
DATASET_NAME: str = "PhysionetMI"

# MOABB paradigm: left-hand vs right-hand motor imagery (binary).
PARADIGM: str = "LeftRightImagery"

# Target binary classes handled by the LeftRightImagery paradigm.
CLASSES: tuple[str, str] = ("left_hand", "right_hand")

# --- Subject subset ------------------------------------------------------
# Version 1 uses a small, inspectable subset (subjects 1-10). The full
# 109-subject run is deferred to a future version.
SUBJECTS: list[int] = list(range(1, 11))

# --- Preprocessing (paradigm band-pass filter) ---------------------------
# MOABB LeftRightImagery default frequency band, in Hz.
FMIN: float = 8.0
FMAX: float = 32.0

# --- Pipeline baseline settings ------------------------------------------
# Fixed CSP component count for the version 1 CSP+LDA baseline. This is a
# documented baseline choice (commonly 6 for binary motor imagery) and is NOT
# selected by inspecting test-fold performance.
N_CSP_COMPONENTS: int = 6

# --- Evaluation ----------------------------------------------------------
# Version 1 evaluation type. PhysionetMI has a single session in the MOABB
# snapshot, so within-session is the cleanest first protocol.
EVALUATION: str = "within_session"

# Primary metric. Binary ROC-AUC has a chance level of 0.5.
PRIMARY_METRIC: str = "roc_auc"
CHANCE_LEVEL: float = 0.5

# Fixed random seed for reproducibility wherever the evaluation allows it.
RANDOM_STATE: int = 42

# --- Dataset provenance (documentation references) -----------------------
DATASET_LICENSE: str = "ODC-By 1.0"
DATASET_SOURCE_URL: str = "https://physionet.org/content/eegmmidb/1.0.0/"
MOABB_DATASET_URL: str = (
    "https://moabb.neurotechx.com/docs/generated/moabb.datasets.PhysionetMI.html"
)
MOABB_PARADIGM_URL: str = (
    "https://moabb.neurotechx.com/docs/generated/"
    "moabb.paradigms.LeftRightImagery.html"
)
