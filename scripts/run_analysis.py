#!/usr/bin/env python3
"""Analyze the within-session baseline results and produce summaries + figures.

This is the version 0.3 analysis entry point. It READS an existing per-trial
result table (``results/baseline_results.csv``, produced by
``scripts/run_baseline.py``) and writes:

    - results/aggregate_scores.csv      : per-pipeline aggregate summary
      (mean, median, std, IQR, min, max, n_subjects).
    - figures/per_subject_scores.png    : per-subject ROC-AUC by pipeline.
    - figures/pipeline_comparison.png   : aggregate comparison across pipelines.
    - figures/score_distribution.png    : score distribution by pipeline.

All figures show the binary chance-level reference (ROC-AUC 0.5). No data is
downloaded and no model is run: this step only summarizes and visualizes
results that already exist. The outputs are a classical within-session baseline
only and carry no real-time, cross-user, or clinical interpretation.

Usage:
    python3 scripts/run_analysis.py
    python3 scripts/run_analysis.py --results results/baseline_results.csv
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if _SRC.exists() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from bci_mi_classifier import config  # noqa: E402
from bci_mi_classifier import results as results_module  # noqa: E402
from bci_mi_classifier import visualization  # noqa: E402

logger = logging.getLogger("run_analysis")

DEFAULT_RESULTS = _ROOT / "results" / "baseline_results.csv"
DEFAULT_AGGREGATE = _ROOT / "results" / "aggregate_scores.csv"
DEFAULT_FIGURES = _ROOT / "figures"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--results",
        type=Path,
        default=DEFAULT_RESULTS,
        help=f"Per-trial result CSV to read (default: {DEFAULT_RESULTS}).",
    )
    parser.add_argument(
        "--aggregate-output",
        type=Path,
        default=DEFAULT_AGGREGATE,
        help=f"Aggregate summary CSV to write (default: {DEFAULT_AGGREGATE}).",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=DEFAULT_FIGURES,
        help=f"Directory for output figures (default: {DEFAULT_FIGURES}).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    args = parse_args(argv)

    import pandas as pd

    if not args.results.exists():
        logger.error(
            "Result file not found: %s. Run scripts/run_baseline.py first.",
            args.results,
        )
        return 1

    results = pd.read_csv(args.results)
    if len(results) == 0:
        logger.error("Result file is empty: %s", args.results)
        return 1

    results_module.validate_results(results)
    logger.info("Loaded %d result rows from %s", len(results), args.results)

    aggregate = results_module.aggregate_scores(results)
    args.aggregate_output.parent.mkdir(parents=True, exist_ok=True)
    aggregate.to_csv(args.aggregate_output, index=False)
    logger.info("Wrote aggregate summary to %s", args.aggregate_output)

    figures_dir = args.figures_dir
    figures_dir.mkdir(parents=True, exist_ok=True)
    per_subject = visualization.plot_per_subject_scores(
        results, figures_dir / "per_subject_scores.png"
    )
    comparison = visualization.plot_pipeline_comparison(
        aggregate, figures_dir / "pipeline_comparison.png"
    )
    distribution = visualization.plot_score_distribution(
        results, figures_dir / "score_distribution.png"
    )
    for fig_path in (per_subject, comparison, distribution):
        logger.info("Wrote figure %s", fig_path)

    _print_summary(results, aggregate)
    return 0


def _print_summary(results, aggregate) -> None:
    """Print a cautious, factual summary of the analysis (no overclaiming)."""
    subjects = sorted(results["subject"].unique().tolist())
    print()
    print("=" * 72)
    print("Within-session baseline analysis (factual, not a generalization claim)")
    print("=" * 72)
    print(f"Subjects included: {subjects} (n={len(subjects)})")
    print(f"Chance-level {config.PRIMARY_METRIC}: {config.CHANCE_LEVEL}")
    print()
    with pd_display():
        print(aggregate.to_string(index=False))
    print()
    print(
        "Note: scores are within-session ROC-AUC and vary across subjects; "
        "this is a classical baseline, not evidence of real-world, real-time, "
        "or cross-user BCI performance."
    )


class pd_display:
    """Context manager for wide, full-column pandas printing."""

    def __enter__(self):
        import pandas as pd

        self._ctx = pd.option_context(
            "display.max_columns", None, "display.width", 120
        )
        self._ctx.__enter__()
        return self

    def __exit__(self, *exc):
        return self._ctx.__exit__(*exc)


if __name__ == "__main__":
    raise SystemExit(main())
