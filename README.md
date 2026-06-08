# BCI Motor Imagery Classifier

Reproducible EEG motor imagery classification using public BCI data, MOABB, and classical machine learning baselines.

This repository benchmarks left-hand vs right-hand motor imagery classification on the PhysionetMI dataset using a transparent evaluation protocol. The goal is to build a credible foundation for future BCI and neurotechnology work, not to claim a production-ready brain-computer interface.

> **Status: v1.0 release — GitHub-ready classical within-session baseline benchmark.**
> Three pipelines (CSP+LDA, Dummy, LogVariance+LDA) were evaluated on PhysionetMI subjects 1-10 under a single MOABB within-session protocol. Curated results, figures, and a methodology report are committed. Raw EEG recordings and MOABB/MNE caches remain git-ignored and are never committed.

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
- Pipelines: CSP+LDA, Dummy (chance), LogVariance+LDA.
- Primary metric: ROC-AUC.

Version 1 is intentionally **not**:

- a deep learning benchmark;
- a real-time BCI;
- a clinical, diagnostic, or cognitive tool;
- a cross-user generalization claim;
- a production neurotechnology system.

## Pipelines

### CSP+LDA (primary)

Classical motor imagery baseline.

- CSP extracts supervised spatial features from EEG epochs (fit inside cross-validation to prevent leakage).
- LDA performs linear classification on the extracted features.
- A fixed, documented CSP component count is used as a baseline; it is **not** tuned on test results.

### Dummy / Chance Baseline

Sanity check against chance-level performance. Mean binary ROC-AUC should be near 0.5 on average; per-subject scores can deviate with small trial counts.

### LogVariance+LDA

Simple log-variance band-power features followed by LDA. Included as a transparent feature baseline for comparison with CSP+LDA.

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

## Results (v1.0)

These results come from a single within-session MOABB run of three pipelines (CSP+LDA, Dummy, LogVariance+LDA) on PhysionetMI subjects 1-10 (`LeftRightImagery`, 8-32 Hz, fixed random seed 42, ROC-AUC primary metric). All pipelines were evaluated in one `WithinSessionEvaluation` call so they share identical splits. Full methodology and interpretation: [`reports/bci_motor_imagery_report.md`](reports/bci_motor_imagery_report.md). Reproduce via `scripts/run_baseline.py` followed by `scripts/run_analysis.py`.

Aggregate within-session ROC-AUC across the 10 subjects:

| pipeline        | metric  | n_subjects | mean  | median | std   | IQR   | min  | max   |
|-----------------|---------|-----------:|------:|-------:|------:|------:|-----:|------:|
| CSP+LDA         | roc_auc | 10         | 0.653 | 0.665  | 0.234 | 0.283 | 0.23 | 1.00  |
| Dummy           | roc_auc | 10         | 0.530 | 0.510  | 0.076 | 0.103 | 0.46 | 0.695 |
| LogVariance+LDA | roc_auc | 10         | 0.658 | 0.670  | 0.117 | 0.173 | 0.46 | 0.80  |

**Interpretation (cautious).** The Dummy baseline averaged near the binary chance-level ROC-AUC of 0.5 (mean 0.530, median 0.510), which supports the sanity of the evaluation setup, though individual subjects can deviate from 0.5 with small trial counts. On the selected subjects, CSP+LDA and LogVariance+LDA both performed above chance on average (means 0.653 and 0.658 respectively), but scores varied substantially across subjects (CSP+LDA std 0.234, range 0.23-1.00; LogVariance+LDA std 0.117, range 0.46-0.80). At least one subject fell below chance for CSP+LDA. These numbers should be read as classical *within-session* baselines on a small subject subset, **not** as evidence of real-world, real-time, or cross-user BCI reliability, and they carry no clinical, diagnostic, or cognitive interpretation. The full per-subject table is in `results/baseline_results.csv` and the aggregate summary in `results/aggregate_scores.csv`.

Per-subject scores (chance level dashed at 0.5):

![Per-subject within-session ROC-AUC by pipeline](figures/per_subject_scores.png)

Aggregate comparison across pipelines (mean +/- std, chance at 0.5):

![Aggregate within-session comparison across pipelines](figures/pipeline_comparison.png)

Score distribution across subjects (box plot with per-subject points, chance at 0.5):

![Within-session score distribution by pipeline](figures/score_distribution.png)

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
  docs/                 # project, dataset, evaluation, model-card, limitations docs (local only)
  scripts/              # run_baseline.py (benchmark) and run_analysis.py (summary + figures)
  notebooks/            # planned benchmark + analysis notebooks
  reports/              # methodology/results report (bci_motor_imagery_report.md)
  results/              # curated result CSVs committed; raw data ignored
  figures/              # curated figures committed; other outputs ignored
  src/bci_mi_classifier/  # implemented modules (config, datasets, pipelines, evaluation, results, visualization)
  tests/                # config/schema tests (pytest; placeholders skipped)
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

Core dependencies: `moabb`, `mne`, `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`; `pytest` for development. See `requirements.txt` and `pyproject.toml`.

> Installing dependencies and running `scripts/run_baseline.py` will cause MOABB to download EEG data into a local cache on first use (this can take several minutes). That cache is git-ignored and must never be committed. The analysis step (`scripts/run_analysis.py`) only reads the saved result CSV and downloads nothing.

### Reproducing the results

```bash
# 1. run the within-session multi-pipeline benchmark (downloads data on first use)
python3 scripts/run_baseline.py

# 2. generate the aggregate summary table and figures from the saved results
python3 scripts/run_analysis.py
```

### Running the tests

```bash
python3 -m pytest -q
# verify package version after install:
python3 -c "import bci_mi_classifier; print(bci_mi_classifier.__version__)"
```

## Outputs

Generated and committed (curated, reproducible artifacts):

- `results/baseline_results.csv` - per-subject within-session results.
- `results/aggregate_scores.csv` - per-pipeline aggregate summary.
- `figures/per_subject_scores.png`
- `figures/pipeline_comparison.png`
- `figures/score_distribution.png`
- `scripts/run_baseline.py` - reproducible benchmark runner.
- `scripts/run_analysis.py` - aggregate summary + figure generation.
- `reports/bci_motor_imagery_report.md` - methodology, results, limitations, reproducibility.

## What This Project Shows

- EEG motor imagery classification.
- BCI benchmark literacy.
- MOABB-based evaluation.
- Classical ML baselines.
- Careful interpretation of model scores.
- Reproducible AI / neurotechnology workflow.

## Limitations

**Read these before interpreting any scores.**

- Version 1 uses only **subjects 1-10** of PhysionetMI (not the full 109-subject dataset).
- **Within-session performance does not imply cross-user generalization** — models were not tested on unseen users or sessions.
- **Subject variability is high** — CSP+LDA ROC-AUC ranged from 0.23 to 1.00 across subjects; aggregate means hide failure cases.
- **No clinical, diagnostic, or cognitive claims** — this is a research baseline, not a medical or cognitive assessment tool.
- **No real-time BCI control** — offline benchmark only; no online decoding or hardware integration.
- **Deep learning deferred** — version 1 is classical baselines only; fixed hyperparameters, no test-set tuning.
- **Library-dependent** — exact scores may vary slightly with MOABB/MNE/scikit-learn versions.

See [`reports/bci_motor_imagery_report.md`](reports/bci_motor_imagery_report.md) (Limitations section) for the full v1.0 write-up.

## Roadmap

- Version 0.1: repository structure and documentation. (**done**)
- Version 0.2: first MOABB within-session CSP+LDA benchmark on subjects 1-10. (**done**)
- Version 0.3: result tables, aggregate summaries, and figures. (**done**)
- Version 0.4: Dummy and LogVariance+LDA baselines. (**done**)
- Version 1.0: polished report, stable docs, GitHub-ready release. (**done — current release**)

**Future (deferred):** full 109-subject benchmark; cross-subject evaluation; Riemannian geometry pipeline; deep learning benchmark; real-time biosignal dashboard (separate project). See [`ROADMAP.md`](ROADMAP.md).

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
