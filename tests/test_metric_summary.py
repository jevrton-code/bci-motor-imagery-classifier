"""Tests for aggregate metric summaries (planned).

Will verify ``bci_mi_classifier.results.aggregate_scores``, e.g.:
    - Output contains the documented AGGREGATE_COLUMNS.
    - mean/median/std/IQR/min/max/n_subjects are computed correctly on a small
      synthetic per-trial table.
    - Aggregation is grouped by pipeline (and metric).
    - Variability statistics are never collapsed into a single headline score.
"""

import pytest


@pytest.mark.skip(reason="version 0.1 scaffold: implementation deferred")
def test_metric_summary_placeholder():
    """Placeholder so pytest collection succeeds without failures."""
    assert True
