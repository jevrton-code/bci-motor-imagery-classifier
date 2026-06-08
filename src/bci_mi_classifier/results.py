"""Result-table schema and aggregation (planned, stub only).

Planned responsibility:
    Validate that benchmark result tables contain the required columns and
    compute aggregate summaries that report variability across subjects (not a
    single headline number).

Per-trial result schema (see docs/evaluation_protocol.md):
    dataset, subject, session, pipeline, score, metric, n_samples,
    n_channels, time, and optionally evaluation, random_state.

Aggregate schema:
    pipeline, metric, n_subjects, mean_score, median_score, std_score,
    iqr_score, min_score, max_score.
"""

from __future__ import annotations

from typing import Any

RESULT_COLUMNS: tuple[str, ...] = (
    "dataset",
    "subject",
    "session",
    "pipeline",
    "score",
    "metric",
    "n_samples",
    "n_channels",
    "time",
)

OPTIONAL_RESULT_COLUMNS: tuple[str, ...] = (
    "evaluation",
    "random_state",
)

AGGREGATE_COLUMNS: tuple[str, ...] = (
    "pipeline",
    "metric",
    "n_subjects",
    "mean_score",
    "median_score",
    "std_score",
    "iqr_score",
    "min_score",
    "max_score",
)


def validate_results(results: Any) -> bool:
    """Validate a per-trial result table against ``RESULT_COLUMNS``.

    Planned behavior:
        Check that all required columns are present and have plausible dtypes;
        raise a descriptive error (or return ``False``) otherwise.

    Args:
        results: A ``pandas.DataFrame`` of per-trial results.

    Returns:
        ``True`` if the table conforms to the required schema.
    """
    raise NotImplementedError("version 0.1 scaffold: result validation deferred")


def aggregate_scores(results: Any) -> Any:
    """Aggregate per-trial scores into a per-pipeline summary table.

    Planned behavior:
        Group by pipeline (and metric) and compute mean, median, std, IQR, min,
        max, and subject count, producing a table with ``AGGREGATE_COLUMNS``.

    Args:
        results: A validated per-trial result table.

    Returns:
        A ``pandas.DataFrame`` of aggregate statistics per pipeline.
    """
    raise NotImplementedError("version 0.1 scaffold: aggregation deferred")
