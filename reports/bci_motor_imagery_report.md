# BCI Motor Imagery Classifier — Benchmark Report (v1.0)

This report summarizes the version 1.0 within-session classical baseline benchmark for left-hand vs right-hand motor imagery classification on public EEG data. It is intended as a transparent, reproducible reference — **not** as evidence of real-world, real-time, cross-user, or clinical BCI performance.

## Methodology

### Dataset

- **Source:** MOABB [`PhysionetMI`](https://moabb.neurotechx.com/docs/generated/moabb.datasets.PhysionetMI.html) (PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0).
- **Subjects:** 1–10 (version 1 subset; full dataset has 109 subjects).
- **Channels:** 64 EEG channels at 160 Hz; 3.0 s trials; one session per subject in the MOABB snapshot.

### Paradigm

- **MOABB paradigm:** [`LeftRightImagery`](https://moabb.neurotechx.com/docs/generated/moabb.paradigms.LeftRightImagery.html).
- **Task:** Binary classification — left-hand vs right-hand motor imagery.
- **Frequency band:** 8–32 Hz (paradigm default).

### Evaluation

- **Protocol:** Within-session (`WithinSessionEvaluation`); all pipelines evaluated in a **single** MOABB call so they share identical train/test splits.
- **Primary metric:** ROC-AUC (binary chance level **0.5**).
- **Random seed:** 42 (`config.RANDOM_STATE`).
- **Pipelines (three):**
  1. **CSP+LDA** — Common Spatial Patterns feature extraction + Linear Discriminant Analysis (primary classical baseline).
  2. **Dummy** — Stratified chance baseline (sanity check; mean ROC-AUC expected near 0.5).
  3. **LogVariance+LDA** — Log-variance band-power features + LDA (simple transparent comparison).

No hyperparameters were tuned on held-out test folds. CSP component count is fixed at the documented baseline value.

## Results

Aggregate within-session ROC-AUC across 10 subjects (from `results/aggregate_scores.csv`):

| pipeline        | metric  | n_subjects | mean  | median | std   | IQR   | min  | max   |
|-----------------|---------|-----------:|------:|-------:|------:|------:|-----:|------:|
| CSP+LDA         | roc_auc | 10         | 0.653 | 0.665  | 0.234 | 0.283 | 0.23 | 1.00  |
| Dummy           | roc_auc | 10         | 0.530 | 0.510  | 0.076 | 0.103 | 0.46 | 0.695 |
| LogVariance+LDA | roc_auc | 10         | 0.658 | 0.670  | 0.117 | 0.173 | 0.46 | 0.80  |

Per-subject scores are in `results/baseline_results.csv` (30 rows: 10 subjects × 3 pipelines).

### Per-subject variability

Scores vary substantially across subjects. For example, CSP+LDA ranges from 0.23 (subject 9) to 1.00 (subject 7); LogVariance+LDA ranges from 0.46 to 0.80. At least one subject scored below chance for CSP+LDA. This variability is expected in motor imagery BCI and reinforces that aggregate means must not be read as universal performance.

### Dummy baseline sanity check

The Dummy pipeline averaged near the theoretical binary chance level (mean **0.530**, median **0.510**), supporting the integrity of the evaluation setup. Individual subject Dummy scores can deviate from 0.5 with small trial counts per fold.

### Cautious interpretation

These numbers are **within-session classical baselines** on a small subject subset. They do **not** demonstrate:

- real-time BCI control or online decoding;
- cross-user or cross-session generalization;
- clinical, diagnostic, or cognitive utility;
- production-ready neurotechnology performance.

On the selected subjects, CSP+LDA and LogVariance+LDA both performed above chance on average (means 0.653 and 0.658 respectively), but the wide subject spread — especially for CSP+LDA — limits any strong conclusion beyond “classical methods can work for some subjects under within-session conditions.”

## Figures

Figures (chance level dashed at 0.5) are committed under `figures/`:

- `per_subject_scores.png` — per-subject ROC-AUC by pipeline.
- `pipeline_comparison.png` — aggregate mean ± std across pipelines.
- `score_distribution.png` — distribution with per-subject points.

## Limitations

- **Subject subset:** Only subjects 1–10; not representative of the full 109-subject dataset.
- **Within-session only:** Performance on held-out trials from the same recording session does not imply generalization to new users or sessions.
- **High variability:** Subject-level scores span a wide range; headline aggregates hide failure cases.
- **Fixed baselines:** No nested hyperparameter tuning; CSP settings are documented defaults, not optimized.
- **No deep learning, real-time, or clinical scope:** Version 1 deliberately excludes DL benchmarks, online BCI, and any health-related claims.
- **Library dependence:** Exact scores may shift slightly with MOABB, MNE-Python, or scikit-learn versions.

See also `docs/limitations.md` (local working copy) and the Limitations section of `README.md`.

## Reproducibility

Requires Python 3.11+. Install dependencies (`pip install -r requirements.txt` or `pip install -e ".[dev]"`).

```bash
# 1. Run the within-session multi-pipeline benchmark
#    (MOABB downloads PhysionetMI on first use; cache is git-ignored)
python3 scripts/run_baseline.py

# 2. Generate aggregate summary and figures from saved results
python3 scripts/run_analysis.py
```

Outputs:

- `results/baseline_results.csv` — per-subject results.
- `results/aggregate_scores.csv` — aggregate summary table.
- `figures/*.png` — visualization artifacts.

Run tests: `python3 -m pytest -q` (placeholder tests; collection passes with skips).

## References

- MOABB: https://moabb.neurotechx.com/docs/index.html
- PhysioNet EEG Motor Movement/Imagery Dataset: https://physionet.org/content/eegmmidb/1.0.0/
- Full citation list: `CITATION.md`

---

*Report version: 1.0.0 — classical within-session baseline benchmark, GitHub-ready release.*
