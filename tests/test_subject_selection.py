"""Tests for subject selection logic (planned).

Will verify ``bci_mi_classifier.datasets.select_subjects``, e.g.:
    - Defaults to the version 1 subset (subjects 1-10).
    - De-duplicates and sorts requested subject ids.
    - Rejects non-positive or out-of-range subject ids.
    - Returns a list of ints suitable for the MOABB evaluation.
"""

import pytest


@pytest.mark.skip(reason="version 0.1 scaffold: implementation deferred")
def test_subject_selection_placeholder():
    """Placeholder so pytest collection succeeds without failures."""
    assert True
