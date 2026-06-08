# Roadmap

This roadmap maps the backlog (`docs/04_BACKLOG.md`, milestones M0-M6 / `BCI-xxx`) and the versioning plan (`docs/01_TECHNICAL_SPEC.md`) to releases. The guiding principle is to establish a credible, transparent evaluation before running any model, and to defer deep learning and cross-user claims.

## Version 0.1 - Foundation / Scaffold (this release)

Repository structure, documentation, and documented module stubs. **No benchmark run; no data downloaded.**

- [x] **BCI-001** Lock version 1 scope (classical baselines; deep learning + real-time deferred).
- [x] **BCI-002** Define public narrative (BCI / motor imagery / EEG / reproducible evaluation).
- [x] **BCI-101** Document MOABB and PhysionetMI facts (`docs/dataset_notes.md`).
- [x] **BCI-102** Define subject subset (subjects 1-10, rationale documented).
- [x] **BCI-103** Document LeftRightImagery paradigm (classes, ROC-AUC, 8-32 Hz band).
- [x] **BCI-201** Create repository skeleton (README, docs, notebooks, results, figures, reports, src, tests).
- [x] **BCI-202** Create dependency plan (`requirements.txt`, `pyproject.toml`, Python 3.11+).
- [x] **BCI-203** Add citation and license files (`CITATION.md`, MIT `LICENSE`; dataset license kept separate).
- [x] **BCI-301** Write evaluation protocol (`docs/evaluation_protocol.md`).
- [x] **BCI-302** Define result schema (per-trial + aggregate columns; tests planned).
- [x] `.gitignore` excludes raw EEG data and MOABB/MNE caches.
- [x] Module stubs (`config`, `datasets`, `pipelines`, `evaluation`, `results`, `visualization`).
- [x] Placeholder tests so `pytest` collection passes.

## Version 0.2 - First Benchmark

First reproducible MOABB within-session run on PhysionetMI subjects 1-10 with CSP+LDA.

- [ ] **BCI-401** Implement first MOABB within-session benchmark (PhysionetMI, subjects 1-10, ROC-AUC, saves results CSV).
- [ ] **BCI-402** Implement CSP+LDA baseline (scikit-learn compatible; documented CSP settings; no test-set tuning).

## Version 0.3 - Results and Visualization

Result tables, aggregate summaries, and figures from real results.

- [ ] **BCI-501** Create aggregate summaries (mean, median, std, IQR, min, max, n_subjects, by pipeline).
- [ ] **BCI-502** Create per-subject score figure (with chance level shown).
- [ ] **BCI-503** Create pipeline comparison figure (same metric; cautious interpretation).

## Version 0.4 - Additional Baselines

Add the simple baselines and broaden comparison.

- [ ] **BCI-403** Add chance / dummy baseline (chance level visible in results/figures).
- [ ] **BCI-404** Add LogVariance+LDA baseline (same evaluation protocol).

## Version 1.0 - Documentation and GitHub Polish

Polished report, stable docs, and a GitHub-ready release.

- [ ] **BCI-601** Write final README (purpose, dataset, paradigm, protocol, pipelines, results, limitations, roadmap).
- [ ] **BCI-602** Write model cards (CSP+LDA and any additional pipeline).
- [ ] **BCI-603** Write limitations page (subset, within-session, no real-time, no clinical, no deep learning in v1).
- [ ] **BCI-604** Final QA (no raw data / cache in Git; citations; polished README; results + figures; reproducibility tested).

## Future (deferred)

Intentionally out of scope until version 1 is stable:

- Full 109-subject benchmark.
- Cross-subject evaluation (as a separate experiment with separate interpretation).
- Nested hyperparameter tuning.
- Riemannian geometry pipelines (e.g. Covariance+MDM, TangentSpace+LR).
- Deep learning baselines (e.g. EEGNet, Braindecode).
- Real-time biosignal dashboard / BrainFlow integration (likely a separate project).
