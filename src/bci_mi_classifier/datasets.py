"""Dataset access and subject selection (planned, stub only).

Planned responsibility:
    Provide a thin, documented wrapper around the MOABB ``PhysionetMI``
    dataset and the ``LeftRightImagery`` paradigm so that the rest of the
    benchmark can request a consistent subject subset without duplicating
    MOABB configuration.

Raw-data policy:
    Raw EEG files and MOABB cache directories are never committed to the
    repository (see ``.gitignore`` and ``docs/dataset_notes.md``). Data is
    fetched on demand by MOABB into a local, ignored cache. Version 0.1 does
    NOT download any data.

References:
    - MOABB PhysionetMI:
      https://moabb.neurotechx.com/docs/generated/moabb.datasets.PhysionetMI.html
    - MOABB LeftRightImagery:
      https://moabb.neurotechx.com/docs/generated/moabb.paradigms.LeftRightImagery.html
"""

from __future__ import annotations

from typing import Any


def get_dataset() -> Any:
    """Return a configured MOABB ``PhysionetMI`` dataset instance.

    Planned behavior:
        Instantiate ``moabb.datasets.PhysionetMI`` and return it. No data is
        downloaded by construction; MOABB fetches lazily during evaluation.

    Returns:
        A MOABB dataset object.
    """
    raise NotImplementedError("version 0.1 scaffold: dataset access deferred")


def get_paradigm() -> Any:
    """Return a configured MOABB ``LeftRightImagery`` paradigm instance.

    Planned behavior:
        Instantiate ``moabb.paradigms.LeftRightImagery`` using the documented
        frequency band (``config.FMIN`` / ``config.FMAX``) and the default
        ROC-AUC metric.

    Returns:
        A MOABB paradigm object.
    """
    raise NotImplementedError("version 0.1 scaffold: paradigm access deferred")


def select_subjects(subjects: list[int] | None = None) -> list[int]:
    """Validate and return the subject subset for the benchmark.

    Planned behavior:
        Default to ``config.SUBJECTS`` (subjects 1-10), validate that requested
        subjects are positive integers within the dataset range, and return a
        sorted, de-duplicated list.

    Args:
        subjects: Optional explicit subject ids. Defaults to ``config.SUBJECTS``.

    Returns:
        The validated list of subject ids.
    """
    raise NotImplementedError("version 0.1 scaffold: subject selection deferred")
