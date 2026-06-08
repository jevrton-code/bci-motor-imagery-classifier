"""Result figures (planned, stub only).

Planned responsibility:
    Generate the benchmark figures from real result tables, always showing the
    binary chance-level reference (ROC-AUC 0.5) and per-subject variability.
    Figures are written to ``figures/`` and are not committed as data outputs
    (only ``.gitkeep`` placeholders are tracked); see ``.gitignore``.

Planned figures (see docs/evaluation_protocol.md):
    - per_subject_scores.png   : scores per subject and pipeline.
    - pipeline_comparison.png  : aggregate comparison across pipelines.
    - score_distribution.png   : score distribution by pipeline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def plot_per_subject_scores(results: Any, out_path: str | Path) -> Path:
    """Plot per-subject scores grouped by pipeline.

    Planned behavior:
        Render a readable per-subject score figure with a chance-level line at
        ROC-AUC 0.5, saving it to ``out_path``.

    Args:
        results: A validated per-trial result table.
        out_path: Destination PNG path.

    Returns:
        The path to the saved figure.
    """
    raise NotImplementedError("version 0.1 scaffold: per-subject plot deferred")


def plot_pipeline_comparison(aggregate: Any, out_path: str | Path) -> Path:
    """Plot an aggregate comparison across pipelines.

    Planned behavior:
        Render a boxplot or bar plot comparing pipelines on the same metric,
        with cautious labeling, saving it to ``out_path``.

    Args:
        aggregate: A per-pipeline aggregate table.
        out_path: Destination PNG path.

    Returns:
        The path to the saved figure.
    """
    raise NotImplementedError("version 0.1 scaffold: comparison plot deferred")


def plot_score_distribution(results: Any, out_path: str | Path) -> Path:
    """Plot the score distribution per pipeline.

    Planned behavior:
        Render a distribution figure (e.g. violin/box/strip) per pipeline with
        the chance-level reference, saving it to ``out_path``.

    Args:
        results: A validated per-trial result table.
        out_path: Destination PNG path.

    Returns:
        The path to the saved figure.
    """
    raise NotImplementedError("version 0.1 scaffold: distribution plot deferred")
