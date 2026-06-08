"""Tests for the result-table schema (planned).

Will verify ``bci_mi_classifier.results.validate_results`` and the declared
schema constants, e.g.:
    - All required RESULT_COLUMNS are enforced on a per-trial table.
    - Tables missing required columns are rejected.
    - Optional columns (evaluation, random_state) are tolerated.
    - The schema matches docs/evaluation_protocol.md.
"""

import pytest


@pytest.mark.skip(reason="version 0.1 scaffold: implementation deferred")
def test_result_schema_placeholder():
    """Placeholder so pytest collection succeeds without failures."""
    assert True
