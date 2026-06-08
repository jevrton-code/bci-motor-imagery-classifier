"""Tests for project configuration constants (planned).

Will verify that ``bci_mi_classifier.config`` exposes the documented version 1
choices and that they are internally consistent, e.g.:
    - DATASET_NAME == "PhysionetMI" and PARADIGM == "LeftRightImagery".
    - SUBJECTS == [1..10] (10 positive, unique, sorted subject ids).
    - FMIN < FMAX and the band is the documented 8-32 Hz.
    - PRIMARY_METRIC == "roc_auc" with CHANCE_LEVEL == 0.5.
    - N_CSP_COMPONENTS is a positive integer baseline value.
    - RANDOM_STATE is a fixed integer seed.
"""

import pytest


@pytest.mark.skip(reason="version 0.1 scaffold: implementation deferred")
def test_config_constants_placeholder():
    """Placeholder so pytest collection succeeds without failures."""
    assert True
