"""Result figures for the within-session baseline benchmark.

Responsibility:
    Generate the benchmark figures from real result tables, always showing the
    binary chance-level reference (ROC-AUC 0.5) and per-subject variability.
    Figures are written to ``figures/``.

Figures (see docs/evaluation_protocol.md):
    - per_subject_scores.png   : scores per subject and pipeline.
    - pipeline_comparison.png  : aggregate comparison across pipelines.
    - score_distribution.png   : score distribution by pipeline.

Interpretation note:
    These figures show a classical *within-session* baseline only. They are not
    evidence of real-world, real-time, or cross-user BCI performance, and carry
    no clinical, diagnostic, or cognitive interpretation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import config

# Modest DPI keeps committed PNGs small (well under ~1-2 MB) while staying
# readable in the README and on GitHub.
_FIG_DPI: int = 120


def _prepare_axes() -> tuple[Any, Any]:
    """Create a figure/axes pair with a clean, readable seaborn style."""
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_theme(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(9, 6))
    return fig, ax


def _add_chance_line(ax: Any) -> None:
    """Draw the binary ROC-AUC chance-level reference line at 0.5."""
    ax.axhline(
        config.CHANCE_LEVEL,
        color="0.35",
        linestyle="--",
        linewidth=1.5,
        label=f"chance ({config.CHANCE_LEVEL})",
        zorder=0,
    )


def _finalize(fig: Any, ax: Any, out_path: str | Path) -> Path:
    """Apply tight layout and save the figure, returning its path."""
    import matplotlib.pyplot as plt

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=_FIG_DPI, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_per_subject_scores(results: Any, out_path: str | Path) -> Path:
    """Plot per-subject scores grouped by pipeline.

    Renders a grouped bar chart of the per-subject ROC-AUC for each pipeline,
    with a dashed chance-level line at 0.5, saving it to ``out_path``.

    Args:
        results: A per-trial result table (needs ``subject``, ``pipeline``,
            ``score``, and optionally ``metric``).
        out_path: Destination PNG path.

    Returns:
        The path to the saved figure.
    """
    import seaborn as sns

    metric = _metric_label(results)
    fig, ax = _prepare_axes()
    sns.barplot(
        data=results,
        x="subject",
        y="score",
        hue="pipeline",
        ax=ax,
        edgecolor="0.2",
    )
    _add_chance_line(ax)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel("Subject")
    ax.set_ylabel(f"{metric} (within-session)")
    ax.set_title("Per-subject within-session scores by pipeline")
    ax.legend(title="Pipeline", loc="lower right", framealpha=0.9)
    return _finalize(fig, ax, out_path)


def plot_pipeline_comparison(aggregate: Any, out_path: str | Path) -> Path:
    """Plot an aggregate comparison across pipelines.

    Renders a bar chart of mean score per pipeline with standard-deviation
    error bars and a dashed chance-level line at 0.5, saving it to ``out_path``.

    Args:
        aggregate: A per-pipeline aggregate table (needs ``pipeline``,
            ``mean_score``, ``std_score``, and optionally ``metric``,
            ``n_subjects``).
        out_path: Destination PNG path.

    Returns:
        The path to the saved figure.
    """
    metric = _metric_label(aggregate)
    fig, ax = _prepare_axes()

    pipelines = list(aggregate["pipeline"])
    means = list(aggregate["mean_score"])
    stds = (
        list(aggregate["std_score"])
        if "std_score" in aggregate.columns
        else [0.0] * len(pipelines)
    )

    import numpy as np

    palette = _pipeline_palette(pipelines)
    ax.bar(
        pipelines,
        means,
        yerr=stds,
        capsize=6,
        color=[palette[p] for p in pipelines],
        edgecolor="0.2",
        error_kw={"ecolor": "0.3", "elinewidth": 1.5},
    )
    _add_chance_line(ax)

    if "n_subjects" in aggregate.columns:
        for x, (mean, n) in enumerate(zip(means, aggregate["n_subjects"])):
            ax.annotate(
                f"mean={mean:.3f}\n(n={int(n)})",
                (x, mean),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                va="bottom",
                fontsize=11,
            )

    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel("Pipeline")
    ax.set_ylabel(f"Mean {metric} (+/- std)")
    ax.set_title("Aggregate within-session comparison across pipelines")
    ax.legend(loc="lower right", framealpha=0.9)
    return _finalize(fig, ax, out_path)


def plot_score_distribution(results: Any, out_path: str | Path) -> Path:
    """Plot the score distribution per pipeline.

    Renders a box plot overlaid with individual per-subject points (strip plot)
    for each pipeline, with a dashed chance-level line at 0.5, saving it to
    ``out_path``.

    Args:
        results: A per-trial result table (needs ``pipeline``, ``score``, and
            optionally ``metric``).
        out_path: Destination PNG path.

    Returns:
        The path to the saved figure.
    """
    import seaborn as sns

    metric = _metric_label(results)
    fig, ax = _prepare_axes()
    pipelines = list(dict.fromkeys(results["pipeline"]))
    palette = _pipeline_palette(pipelines)

    sns.boxplot(
        data=results,
        x="pipeline",
        y="score",
        hue="pipeline",
        order=pipelines,
        palette=palette,
        legend=False,
        width=0.5,
        fliersize=0.0,
        ax=ax,
    )
    sns.stripplot(
        data=results,
        x="pipeline",
        y="score",
        order=pipelines,
        color="0.15",
        size=7,
        jitter=0.15,
        alpha=0.8,
        ax=ax,
    )
    _add_chance_line(ax)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel("Pipeline")
    ax.set_ylabel(f"{metric} (within-session)")
    ax.set_title("Within-session score distribution by pipeline")
    ax.legend(loc="lower right", framealpha=0.9)
    return _finalize(fig, ax, out_path)


def _metric_label(table: Any) -> str:
    """Return a human-readable metric label from a result/aggregate table."""
    if "metric" in table.columns and len(table) > 0:
        raw = str(table["metric"].iloc[0])
        return raw.replace("_", "-").upper() if raw == config.PRIMARY_METRIC else raw
    return config.PRIMARY_METRIC.replace("_", "-").upper()


def _pipeline_palette(pipelines: list[str]) -> dict[str, Any]:
    """Map pipeline names to stable colors."""
    import seaborn as sns

    colors = sns.color_palette("colorblind", n_colors=max(len(pipelines), 1))
    return {name: colors[i] for i, name in enumerate(pipelines)}
