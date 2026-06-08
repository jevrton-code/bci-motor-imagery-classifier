#!/usr/bin/env python3
"""Run the version 0.4 within-session baseline benchmark.

This script wires together datasets -> pipelines -> evaluation -> results for
the reproducible MOABB benchmark of the project:

    - Dataset:    MOABB ``PhysionetMI`` (subjects 1-10 by default).
    - Paradigm:   MOABB ``LeftRightImagery`` (left_hand vs right_hand,
                  fmin=8, fmax=32 Hz).
    - Evaluation: MOABB ``WithinSessionEvaluation`` with a fixed seed.
    - Pipelines:  CSP+LDA, Dummy (chance), LogVariance+LDA (same evaluation).
    - Metric:     ROC-AUC (binary chance level 0.5).

All pipelines are passed to a single ``WithinSessionEvaluation`` so they share
identical splits. The raw per-subject/session/pipeline result table is written
to ``results/baseline_results.csv``.

On first run MOABB downloads the PhysionetMI EEG recordings into its local
(repository-ignored) cache; this can take several minutes. Subsequent runs
reuse the cache. No clinical, diagnostic, or real-world BCI-usability claims are
made: this is a transparent within-session classification baseline only.

Usage:
    python scripts/run_baseline.py
    python scripts/run_baseline.py --subjects 1 2 3 --overwrite
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow running directly from a checkout without installing the package.
_SRC = Path(__file__).resolve().parents[1] / "src"
if _SRC.exists() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from bci_mi_classifier import config  # noqa: E402
from bci_mi_classifier import evaluation, pipelines, results  # noqa: E402

logger = logging.getLogger("run_baseline")

DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "results" / "baseline_results.csv"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--subjects",
        type=int,
        nargs="+",
        default=None,
        help=f"Subject ids (default: {config.SUBJECTS}).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT}).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Recompute results, ignoring MOABB's evaluation cache.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    args = parse_args(argv)

    subjects = args.subjects if args.subjects is not None else list(config.SUBJECTS)
    pipeline_registry = pipelines.build_pipelines()

    logger.info("=== bci-motor-imagery-classifier v0.4 baselines ===")
    logger.info("Dataset:    %s", config.DATASET_NAME)
    logger.info("Paradigm:   %s (fmin=%s, fmax=%s)", config.PARADIGM, config.FMIN, config.FMAX)
    logger.info("Classes:    %s", " vs ".join(config.CLASSES))
    logger.info("Subjects:   %s", subjects)
    logger.info("Evaluation: %s (seed=%s)", config.EVALUATION, config.RANDOM_STATE)
    logger.info("Metric:     %s (chance=%s)", config.PRIMARY_METRIC, config.CHANCE_LEVEL)
    logger.info("Pipelines:  %s", list(pipeline_registry))
    logger.info("CSP comps:  %s", config.N_CSP_COMPONENTS)

    raw_results = evaluation.run_within_session(
        subjects=subjects,
        pipelines=pipeline_registry,
        random_state=config.RANDOM_STATE,
        overwrite=args.overwrite,
    )

    if raw_results is None or len(raw_results) == 0:
        logger.error("Evaluation returned no results; nothing was saved.")
        return 1

    out_path = results.save_results(raw_results, args.output)
    logger.info("Saved %d result rows to %s", len(raw_results), out_path)

    _print_summary(raw_results)
    return 0


def _print_summary(raw_results) -> None:
    """Print a cautious, factual summary of the run (no overclaiming)."""
    summary = results.aggregate_scores(raw_results)
    subjects_run = sorted(raw_results["subject"].unique().tolist())

    print()
    print("=" * 70)
    print("Within-session baseline summary (factual, not a generalization claim)")
    print("=" * 70)
    print(f"Subjects included: {subjects_run} (n={len(subjects_run)})")
    print(f"Total result rows: {len(raw_results)}")
    print(f"Chance-level ROC-AUC: {config.CHANCE_LEVEL}")
    print()
    with_pandas_display(summary)
    print()
    print(
        "Note: scores are within-session ROC-AUC and vary across subjects; "
        "this is a classical baseline, not evidence of real-world or "
        "cross-user BCI performance."
    )


def with_pandas_display(df) -> None:
    import pandas as pd

    with pd.option_context("display.max_columns", None, "display.width", 120):
        print(df.to_string(index=False))


if __name__ == "__main__":
    raise SystemExit(main())
