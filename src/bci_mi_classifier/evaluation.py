"""Benchmark evaluation orchestration.

Responsibility:
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

import logging
from typing import Any

from . import config
from . import datasets as datasets_module
from . import pipelines as pipelines_module

logger = logging.getLogger(__name__)


def run_within_session(
    subjects: list[int] | None = None,
    pipelines: dict[str, Any] | None = None,
    random_state: int | None = None,
    overwrite: bool = False,
) -> Any:
    """Run the within-session benchmark and return the per-trial result table.

    Configures a MOABB ``WithinSessionEvaluation`` over the PhysionetMI subject
    subset with the given pipelines, runs it, and returns the native MOABB
    ``pandas.DataFrame`` with one row per subject/session/pipeline. MOABB owns
    the cross-validation splitting; no custom split logic is used, and the
    supervised CSP transform is fit only on training folds because it lives
    inside the pipeline.

    Args:
        subjects: Subject subset. Defaults to ``config.SUBJECTS``.
        pipelines: Pipeline registry. Defaults to
            ``pipelines.build_pipelines()`` (CSP+LDA).
        random_state: Random seed. Defaults to ``config.RANDOM_STATE``.
        overwrite: If ``True``, MOABB recomputes rather than reusing any cached
            evaluation results.

    Returns:
        A results table (``pandas.DataFrame``) with MOABB's native columns.
    """
    from moabb.evaluations import WithinSessionEvaluation

    if random_state is None:
        random_state = config.RANDOM_STATE
    if pipelines is None:
        pipelines = pipelines_module.build_pipelines()

    requested = datasets_module.select_subjects(subjects)
    dataset = datasets_module.get_dataset(requested)
    paradigm = datasets_module.get_paradigm()

    logger.info(
        "Running WithinSessionEvaluation on %s subjects %s with pipelines %s "
        "(metric=%s, seed=%s)",
        config.DATASET_NAME,
        requested,
        list(pipelines),
        config.PRIMARY_METRIC,
        random_state,
    )

    evaluation = WithinSessionEvaluation(
        paradigm=paradigm,
        datasets=[dataset],
        random_state=random_state,
        overwrite=overwrite,
        suffix="v0_4_baselines",
    )

    results = evaluation.process(pipelines)
    return results
