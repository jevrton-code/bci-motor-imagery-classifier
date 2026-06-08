"""Benchmark evaluation orchestration (planned, stub only).

Planned responsibility:
    Drive a reproducible within-session MOABB evaluation of the configured
    pipelines on the PhysionetMI subject subset, returning a tidy result table
    that conforms to the schema in ``results`` / ``docs/evaluation_protocol.md``.

Protocol rules (see docs/evaluation_protocol.md):
    - Use MOABB's within-session evaluation utilities, not custom split logic.
    - Use the same evaluation object and subject subset for all pipelines.
    - Use a fixed random seed (``config.RANDOM_STATE``) where supported.
    - Keep supervised transforms inside the pipeline (no global pre-fitting).
    - Do not tune hyperparameters on held-out test folds.
    - Primary metric is ROC-AUC (chance level 0.5).

References:
    - MOABB within-session splitter:
      https://moabb.neurotechx.com/docs/generated/moabb.evaluations.WithinSessionSplitter.html
    - MOABB benchmarking examples:
      https://moabb.neurotechx.com/docs/auto_examples/how_to_benchmark/index.html
"""

from __future__ import annotations

from typing import Any


def run_within_session(
    subjects: list[int] | None = None,
    pipelines: dict[str, Any] | None = None,
    random_state: int | None = None,
) -> Any:
    """Run the within-session benchmark and return the per-trial result table.

    Planned behavior:
        Configure a MOABB within-session evaluation over the PhysionetMI
        subject subset with the given pipelines, run it, and return a
        ``pandas.DataFrame`` with one row per subject/session/pipeline.

    Args:
        subjects: Subject subset. Defaults to ``config.SUBJECTS``.
        pipelines: Pipeline registry. Defaults to ``pipelines.build_pipelines()``.
        random_state: Random seed. Defaults to ``config.RANDOM_STATE``.

    Returns:
        A results table (``pandas.DataFrame``) conforming to the result schema.
    """
    raise NotImplementedError("version 0.1 scaffold: evaluation deferred")
