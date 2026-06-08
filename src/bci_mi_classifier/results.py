"""Result-table schema and aggregation.

Responsibility:
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

from pathlib import Path
from typing import Any

from . import config

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


# Mapping from MOABB's native result column names to the documented schema
# names. MOABB returns ``samples`` and ``channels``; the project schema uses
# ``n_samples`` and ``n_channels``.
_MOABB_COLUMN_ALIASES: dict[str, str] = {
    "samples": "n_samples",
    "channels": "n_channels",
}


def normalize_results(
    results: Any,
    random_state: int | None = None,
    metric: str | None = None,
) -> Any:
    """Return a copy of a MOABB result table conformed to the project schema.

    The native MOABB columns are preserved; this adds the documented schema
    columns that MOABB does not emit directly:
        - ``n_samples`` / ``n_channels`` mirrored from ``samples`` / ``channels``
        - ``metric`` (the primary scoring metric, e.g. ``roc_auc``)
        - ``evaluation`` (e.g. ``within_session``)
        - ``random_state`` (the fixed seed used for the run)

    Args:
        results: The raw ``pandas.DataFrame`` returned by a MOABB evaluation.
        random_state: Seed recorded in the provenance column. Defaults to
            ``config.RANDOM_STATE``.
        metric: Metric name recorded in the ``metric`` column. Defaults to
            ``config.PRIMARY_METRIC``.

    Returns:
        A new ``pandas.DataFrame`` with both native and documented columns.
    """
    df = results.copy()

    for src, dst in _MOABB_COLUMN_ALIASES.items():
        if src in df.columns and dst not in df.columns:
            df[dst] = df[src]

    df["metric"] = config.PRIMARY_METRIC if metric is None else metric
    df["evaluation"] = config.EVALUATION
    df["random_state"] = (
        config.RANDOM_STATE if random_state is None else random_state
    )
    return df


def validate_results(results: Any) -> bool:
    """Validate a per-trial result table against ``RESULT_COLUMNS``.

    Checks that all required columns are present. Raises a descriptive error if
    any are missing; optional columns are tolerated.

    Args:
        results: A ``pandas.DataFrame`` of per-trial results.

    Returns:
        ``True`` if the table conforms to the required schema.

    Raises:
        ValueError: If one or more required columns are missing.
    """
    missing = [c for c in RESULT_COLUMNS if c not in results.columns]
    if missing:
        raise ValueError(
            f"result table is missing required columns: {missing}; "
            f"present columns: {list(results.columns)}"
        )
    return True


def save_results(
    results: Any,
    path: str | Path,
    random_state: int | None = None,
    normalize: bool = True,
) -> Path:
    """Normalize (optionally) and write a per-trial result table to CSV.

    Args:
        results: The raw MOABB ``pandas.DataFrame`` of per-trial results.
        path: Destination CSV path (parent directories are created).
        random_state: Seed recorded in provenance. Defaults to
            ``config.RANDOM_STATE``.
        normalize: If ``True``, conform the table to the documented schema
            before saving (recommended).

    Returns:
        The path to the written CSV file.
    """
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = normalize_results(results, random_state=random_state) if normalize else results
    validate_results(df)
    df.to_csv(out_path, index=False)
    return out_path


def aggregate_scores(results: Any) -> Any:
    """Aggregate per-trial scores into a per-pipeline summary table.

    Groups by pipeline (and metric when present) and computes mean, median,
    std, IQR, min, max, and the number of distinct subjects, producing a table
    with ``AGGREGATE_COLUMNS``.

    Args:
        results: A per-trial result table with at least ``pipeline`` and
            ``score`` columns (and preferably ``subject`` and ``metric``).

    Returns:
        A ``pandas.DataFrame`` of aggregate statistics per pipeline.
    """
    import pandas as pd

    df = results.copy()
    if "metric" not in df.columns:
        df["metric"] = config.PRIMARY_METRIC

    rows = []
    for (pipeline, metric), group in df.groupby(["pipeline", "metric"], sort=True):
        scores = group["score"]
        q1, q3 = scores.quantile(0.25), scores.quantile(0.75)
        n_subjects = (
            group["subject"].nunique() if "subject" in group.columns else len(group)
        )
        rows.append(
            {
                "pipeline": pipeline,
                "metric": metric,
                "n_subjects": int(n_subjects),
                "mean_score": float(scores.mean()),
                "median_score": float(scores.median()),
                "std_score": float(scores.std(ddof=1)) if len(scores) > 1 else 0.0,
                "iqr_score": float(q3 - q1),
                "min_score": float(scores.min()),
                "max_score": float(scores.max()),
            }
        )

    return pd.DataFrame(rows, columns=list(AGGREGATE_COLUMNS))
