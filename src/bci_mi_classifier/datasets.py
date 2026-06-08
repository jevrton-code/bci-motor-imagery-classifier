"""Dataset access and subject selection.

Responsibility:
    Provide a thin, documented wrapper around the MOABB ``PhysionetMI``
    dataset and the ``LeftRightImagery`` paradigm so that the rest of the
    benchmark can request a consistent subject subset without duplicating
    MOABB configuration.

Raw-data policy:
    Raw EEG files and MOABB cache directories are never committed to the
    repository (see ``.gitignore`` and ``docs/dataset_notes.md``). Data is
    fetched on demand by MOABB into a local, ignored cache.

References:
    - MOABB PhysionetMI:
      https://moabb.neurotechx.com/docs/generated/moabb.datasets.PhysionetMI.html
    - MOABB LeftRightImagery:
      https://moabb.neurotechx.com/docs/generated/moabb.paradigms.LeftRightImagery.html
"""

from __future__ import annotations

from typing import Any

from . import config


def select_subjects(subjects: list[int] | None = None) -> list[int]:
    """Validate and return the subject subset for the benchmark.

    Defaults to ``config.SUBJECTS`` (subjects 1-10), validates that requested
    subjects are positive integers, and returns a sorted, de-duplicated list.

    Args:
        subjects: Optional explicit subject ids. Defaults to ``config.SUBJECTS``.

    Returns:
        The validated, sorted, de-duplicated list of subject ids.

    Raises:
        ValueError: If the resulting subset is empty or contains a non-positive
            or non-integer id.
    """
    if subjects is None:
        subjects = list(config.SUBJECTS)

    validated: set[int] = set()
    for subject in subjects:
        if isinstance(subject, bool) or not isinstance(subject, int):
            raise ValueError(f"subject ids must be integers, got {subject!r}")
        if subject < 1:
            raise ValueError(f"subject ids must be positive, got {subject!r}")
        validated.add(subject)

    if not validated:
        raise ValueError("subject subset must not be empty")

    return sorted(validated)


def get_dataset(subjects: list[int] | None = None) -> Any:
    """Return a configured MOABB ``PhysionetMI`` dataset instance.

    Instantiates ``moabb.datasets.PhysionetMI`` and restricts its
    ``subject_list`` to the validated subset. No data is downloaded by
    construction; MOABB fetches lazily during evaluation.

    Args:
        subjects: Optional subject subset. Defaults to ``config.SUBJECTS``.

    Returns:
        A MOABB ``PhysionetMI`` dataset object limited to the chosen subjects.

    Raises:
        ValueError: If any requested subject id is not available in the dataset.
    """
    from moabb.datasets import PhysionetMI

    requested = select_subjects(subjects)
    dataset = PhysionetMI()

    available = set(dataset.subject_list)
    missing = [s for s in requested if s not in available]
    if missing:
        raise ValueError(
            f"requested subjects not available in PhysionetMI: {missing}"
        )

    dataset.subject_list = requested
    return dataset


def get_paradigm() -> Any:
    """Return a configured MOABB ``LeftRightImagery`` paradigm instance.

    Instantiates ``moabb.paradigms.LeftRightImagery`` using the documented
    frequency band (``config.FMIN`` / ``config.FMAX``). The paradigm restricts
    events to the binary ``left_hand`` vs ``right_hand`` classes and scores with
    ROC-AUC by default.

    Returns:
        A MOABB ``LeftRightImagery`` paradigm object.
    """
    from moabb.paradigms import LeftRightImagery

    return LeftRightImagery(fmin=config.FMIN, fmax=config.FMAX)
