# BCI Motor Imagery Classifier

Reproducible EEG motor imagery classification using public BCI data, MOABB, and classical machine learning baselines.

This repository benchmarks left-hand vs right-hand motor imagery classification on the PhysionetMI dataset using a transparent evaluation protocol. The goal is to build a credible foundation for future BCI and neurotechnology work, not to claim a production-ready brain-computer interface.

> **Status: version 0.1 - foundation / scaffold.**
> This release contains the repository structure, documentation, and documented module stubs only. **No benchmark has been run yet, and no data has been downloaded.** The files under `results/` and `figures/` are *planned* outputs and have not been generated. The modules in `src/bci_mi_classifier/` are documented stubs (planned signatures with `NotImplementedError`), not working implementations.

## Why This Project

Motor imagery classification is a classic Brain-Computer Interface (BCI) task: a model attempts to distinguish imagined movement classes from EEG signals.

This project focuses on doing that carefully:

- public dataset;
- established benchmark tooling;
- classical baselines first;
- per-subject results;
- explicit evaluation protocol;
- clear limitations.

## Dataset and Paradigm

Primary dataset:

- MOABB `PhysionetMI`.
- Source data: PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0.
- 109 subjects, 1 session, 64 EEG channels, 160 Hz sampling rate, 3.0 s trials.
- Class labels in the dataset: `left_hand`, `right_hand`, `feet`, `hands`, `rest`.
- Dataset license: ODC-By 1.0 (separate from this repository's code license).

Primary paradigm:

- MOABB `LeftRightImagery`.
- Task: left-hand vs right-hand motor imagery (binary).
- Default frequency band: 8-32 Hz.
- Primary metric: ROC-AUC (binary chance level 0.5).

Raw EEG data and MOABB cache files are **not** stored in this repository (see `.gitignore`).

## Version 1 Scope

Version 1 uses a small, reproducible subject subset:

- Subjects: 1-10.
- Evaluation: within-session.
- Primary pipeline: CSP+LDA.
- Primary metric: ROC-AUC.

Version 1 is intentionally **not**:

- a deep learning benchmark;
- a real-time BCI;
- a clinical, diagnostic, or cognitive tool;
- a cross-user generalization claim;
- a production neurotechnology system.

## Planned Pipelines

### CSP+LDA (primary)

Classical motor imagery baseline.

- CSP extracts supervised spatial features from EEG epochs (fit inside cross-validation to prevent leakage).
- LDA performs linear classification on the extracted features.
- A fixed, documented CSP component count is used as a baseline; it is **not** tuned on test results.

### Dummy / Chance Baseline (optional)

Sanity check against chance-level performance (~0.5 ROC-AUC).

### LogVariance+LDA (optional)

Simple feature baseline for comparison.

### Future Riemannian Baseline (deferred)

Optional later comparison using covariance-based methods.

## Evaluation Protocol

The benchmark is designed to report:

- per-subject scores;
- aggregate score summaries (mean, median, std, IQR, min, max, n_subjects);
- score variability;
- chance-level reference;
- pipeline comparison figures.

The first release uses within-session evaluation because the selected MOABB dataset snapshot has one session. Cross-subject evaluation is deferred and will be interpreted separately if added later. See `docs/evaluation_protocol.md` for the full protocol.

## Repository Structure

```text
bci-motor-imagery-classifier/
  README.md
  LICENSE
  CITATION.md
  ROADMAP.md
  pyproject.toml
  requirements.txt
  .gitignore
  docs/                 # project, dataset, evaluation, model-card, limitations docs
  notebooks/            # planned benchmark + analysis notebooks
  reports/              # planned methodology/results report
  results/              # planned result CSVs (generated outputs not committed)
  figures/              # planned figures (generated outputs not committed)
  src/bci_mi_classifier/  # documented module stubs (config, datasets, pipelines, ...)
  tests/                # placeholder tests (pytest collection passes)
```

## Installation / Setup

Requires **Python 3.11+**.

```bash
# create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install runtime dependencies
pip install -r requirements.txt

# or install the package (editable) with dev tools (pytest)
pip install -e ".[dev]"
```

Core dependencies (planned): `moabb`, `mne`, `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`; `pytest` for development. See `requirements.txt` and `pyproject.toml`.

> Installing dependencies and running the benchmark will cause MOABB to download EEG data into a local cache on first use. That cache is git-ignored and must never be committed. Version 0.1 does not download any data.

### Running the tests

At version 0.1 the tests are placeholders that confirm collection works:

```bash
pytest
# or, to inspect collection only:
python -m pytest --collect-only -q
```

## Expected Outputs (planned, not yet generated)

- `results/baseline_results.csv`
- `results/aggregate_scores.csv`
- `figures/per_subject_scores.png`
- `figures/pipeline_comparison.png`
- `figures/score_distribution.png`
- a reproducible notebook or script
- a short methodology/results/limitations report

## What This Project Shows

- EEG motor imagery classification.
- BCI benchmark literacy.
- MOABB-based evaluation.
- Classical ML baselines.
- Careful interpretation of model scores.
- Reproducible AI / neurotechnology workflow.

## Limitations

- Version 1 uses only subjects 1-10.
- Within-session performance does **not** imply cross-user generalization.
- Scores can vary strongly by subject.
- No clinical, diagnostic, or cognitive interpretation is provided.
- No real-time BCI control is implemented.
- Deep learning is deferred until classical baselines are stable.

See `docs/limitations.md` for details.

## Roadmap

- Version 0.1: repository structure and documentation (this release).
- Version 0.2: first MOABB within-session CSP+LDA benchmark on subjects 1-10.
- Version 0.3: result tables and aggregate summaries, figures.
- Version 0.4: dummy and LogVariance+LDA baselines.
- Version 1.0: polished report, stable docs, GitHub-ready release.

Future: full 109-subject benchmark; cross-subject evaluation; Riemannian geometry pipeline; deep learning benchmark; real-time biosignal dashboard (separate project). See `ROADMAP.md`.

## License and Citation

This repository's code and documentation are released under the MIT License (see `LICENSE`). The underlying **dataset** is licensed separately under **ODC-By 1.0** and is not redistributed here. Please cite PhysioNet, the EEG Motor Movement/Imagery Dataset, MOABB, MNE-Python, and scikit-learn when using this work; see `CITATION.md`.

## References

- MOABB documentation: https://moabb.neurotechx.com/docs/index.html
- MOABB PhysionetMI: https://moabb.neurotechx.com/docs/generated/moabb.datasets.PhysionetMI.html
- MOABB LeftRightImagery: https://moabb.neurotechx.com/docs/generated/moabb.paradigms.LeftRightImagery.html
- MOABB evaluation concepts: https://moabb.neurotechx.com/docs/api.html
- PhysioNet EEG Motor Movement/Imagery Dataset: https://physionet.org/content/eegmmidb/1.0.0/
- MNE CSP: https://mne.tools/stable/generated/mne.decoding.CSP.html
- scikit-learn LDA: https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html
