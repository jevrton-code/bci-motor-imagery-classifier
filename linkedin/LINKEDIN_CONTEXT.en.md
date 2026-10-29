# BCI Motor Imagery Classifier: LinkedIn context document

> **Language:** English · Versão em português: [`CONTEXTO_LINKEDIN.pt-BR.md`](CONTEXTO_LINKEDIN.pt-BR.md)
> **Last updated:** 2026-10-29
> **Project version covered:** v1.0.0 (commit `beba3ba`, 2026-06-08)
> **Repository:** https://github.com/jevrton-code/bci-motor-imagery-classifier

---

## 0. What this document is for

This file is the **single source of context** for everything published about
this project on LinkedIn: posts, carousels (PDF document posts), comments,
release updates and the profile's "Projects" section. Use it yourself or hand
the whole file to an AI assistant.

Everything here was checked against the repository (code, result CSVs, report,
figures and git history) on 2026-10-29. Where a number was computed from the
data and is not written in the README, that is stated.

**How to use it**

- **To write a post:** read §1 (ready-made summaries), §5 (what the results
  mean) and §6 (what not to claim), then pick an angle from §12.
- **To brief an AI assistant:** give it this file and say which §12 angle you
  want, the language and the length. Tell it to use **only** the numbers in §4
  and to respect §6.
- **When the project changes:** update §4 (fact sheet), §8 (timeline) and §20
  (changelog) first. Everything else follows from them.

**Non-negotiable rules for any public text**

1. Numbers come only from the fact sheet (§4), always with the context
   "within-session evaluation, subjects 1–10".
2. Never suggest clinical use, diagnosis, "mind reading" or real-time control.
3. Whenever you quote a mean, also quote the spread across subjects.
4. Credit the dataset and the tools (§15).
5. Do not say the project "has automated tests": today the 4 tests are skipped
   placeholders (§18).

---

## 1. Ready-made summaries (shortest to longest)

**One line (bio, image caption, carousel title)**

> A reproducible brain-computer interface (BCI) benchmark: EEG motor imagery
> classification with classical baselines and transparent evaluation.

**Hook (fits before "see more", about 140 characters)**

> A mean ROC-AUC of 0.65 looks decent for a BCI. Until you look subject by
> subject: in the same benchmark, one scored 1.00 and another 0.23.

**Short summary (about 480 characters, for a quick post or a comment)**

> I built a reproducible brain-computer interface (BCI) benchmark that
> classifies motor imagery (imagining moving the left or the right hand) from
> public EEG data (PhysioNet, 10 subjects, 64 channels). I compared three
> pipelines under the same MOABB protocol: CSP+LDA, a simple log-variance + LDA
> baseline, and a random classifier as the chance reference. Both real methods
> beat chance on average (ROC-AUC 0.653 and 0.658), but the spread across
> subjects was huge: from 0.23 to 1.00.

**Description for the profile's "Projects" section (about 1,400 characters;
LinkedIn limit: 2,000)**

```text
A reproducible benchmark for classifying motor imagery (left hand vs right hand) from EEG, a classic brain-computer interface (BCI) task.

What I did
• Used public data from the PhysioNet EEG Motor Movement/Imagery Dataset through MOABB (subjects 1–10, 64 channels, 160 Hz, 8–32 Hz band).
• Compared three pipelines in a single within-session evaluation, with identical train/test splits and a fixed seed: CSP+LDA, LogVariance+LDA, and a random (Dummy) baseline as the chance reference.
• Kept CSP inside the cross-validation pipeline to prevent data leakage, and never tuned hyperparameters on test data.
• Produced per-subject results, aggregate statistics (mean, median, std, IQR), three figures and a methodology report.

Results (ROC-AUC; chance = 0.5)
• CSP+LDA: mean 0.653, ranging from 0.23 to 1.00 across subjects
• LogVariance+LDA: mean 0.658, ranging from 0.46 to 0.80
• Dummy: mean 0.530, confirming the evaluation behaves as expected

The main lesson: the average hides the people a system fails. Three of ten subjects scored below chance with CSP+LDA, and the simple baseline tied the classical method on average, with half the spread.

Honest scope: an offline, within-session benchmark on 10 subjects. It is not a real-time BCI, it does not test cross-user generalization, and it has no clinical purpose.

Stack: Python, MOABB, MNE-Python, scikit-learn, pandas, Matplotlib, seaborn.
```

**Suggested "Projects" fields**

| Field | Suggestion |
| --- | --- |
| Project name | BCI Motor Imagery Classifier: a reproducible EEG motor imagery benchmark |
| Date | Jun 2026 (v1.0 released 2026-06-08) |
| Skills | Python · Machine Learning · Signal Processing · Electroencephalography (EEG) · scikit-learn |
| Media | Repository link + `figures/score_distribution.png` (see §10) |
| Associated with | [TO FILL IN: role, course or "personal project"] |

---

## 2. The problem and the motivation

### In plain words

A **brain-computer interface (BCI)** tries to turn brain activity into
commands for a machine. One of the most studied paradigms is **motor
imagery**: a person only *imagines* moving their left or right hand, and that
changes the rhythms recorded over the motor cortex. A classifier tries to tell,
from the EEG alone, which hand was imagined.

### Why doing it "carefully" matters

BCI attracts inflated headlines. In practice, results depend on details that
rarely make it into a post:

- **How the evaluation was done.** Testing on held-out trials from the same
  session (within-session) is much easier than working on a new person
  (cross-subject).
- **Data leakage.** Supervised steps such as CSP inflate results if they are
  fitted on test data.
- **Chance reference.** With few trials per person, a random classifier can
  look good by luck.
- **Variation between people.** A nice average can hide people for whom the
  system simply does not work.

The project was designed to address each of these explicitly, using public
data and established benchmark tooling, and putting transparency ahead of a
headline number.

### Author's personal motivation

[TO FILL IN: why you wanted to build this, where your interest in
BCI/neurotechnology comes from, what you wanted to prove or learn. See §19.]

---

## 3. What was built

### Flow overview

```text
PhysioNet EEG Motor Movement/Imagery Dataset (109 subjects)
  └─ MOABB PhysionetMI — subjects 1–10, 64 channels, 160 Hz
      └─ LeftRightImagery paradigm — left vs right hand, 8–32 Hz filter, 3 s trials
          └─ 3 pipelines evaluated in ONE WithinSessionEvaluation call
             (identical train/test splits, seed 42, ROC-AUC metric)
               ├─ CSP+LDA          (primary)
               ├─ Dummy            (chance reference)
               └─ LogVariance+LDA  (simple baseline)
          └─ results/baseline_results.csv  (30 rows = 10 subjects × 3 pipelines)
              └─ scripts/run_analysis.py
                  ├─ results/aggregate_scores.csv
                  ├─ figures/per_subject_scores.png
                  ├─ figures/pipeline_comparison.png
                  └─ figures/score_distribution.png
                      └─ reports/bci_motor_imagery_report.md
```

### The three pipelines

| Pipeline | What it does | Role in the benchmark |
| --- | --- | --- |
| **CSP+LDA** | *Common Spatial Patterns* (6 components, log-variance output, no regularization) learns supervised spatial filters; *Linear Discriminant Analysis* classifies. | The classical motor imagery reference. |
| **Dummy** | scikit-learn's stratified `DummyClassifier` (after flattening the epochs). Ignores the signal. | Sanity check: should sit near 0.5. |
| **LogVariance+LDA** | Log of each channel's variance (band power) + LDA. No learned spatial filters. | Transparent baseline to compare against CSP. |

### Code layout

- `src/bci_mi_classifier/`: package with `config` (single source of truth for
  fixed choices), `datasets`, `pipelines`, `evaluation`, `results` and
  `visualization`.
- `scripts/run_baseline.py`: runs the benchmark (downloads the data the first
  time).
- `scripts/run_analysis.py`: reads the saved CSV and produces statistics and
  figures (downloads nothing).
- `reports/bci_motor_imagery_report.md`: methodology, results, limitations and
  reproduction steps.

### Reproduction in two commands

```bash
python3 scripts/run_baseline.py   # benchmark (MOABB downloads PhysionetMI on first use)
python3 scripts/run_analysis.py   # aggregate tables + figures
```

---

## 4. Fact sheet (verified numbers)

### Dataset, protocol and configuration

| Item | Value | Source in the repository |
| --- | --- | --- |
| Dataset | PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0, through MOABB `PhysionetMI` | `README.md`, `config.py` |
| Full dataset size | 109 subjects, 1 session, 64 EEG channels, 160 Hz, 3.0 s trials | `README.md` |
| Subjects used in v1 | 1 to 10 | `config.SUBJECTS` |
| Task | Binary: left vs right hand (imagery) | `config.PARADIGM` |
| Frequency band | 8–32 Hz | `config.FMIN/FMAX` |
| Evaluation | Within-session (`WithinSessionEvaluation`), all pipelines in one call | `README.md`, report |
| Trials per subject | 45 (about 9 in the test set per fold) | `samples` and `samples_test` CSV columns |
| Primary metric | ROC-AUC (chance = 0.5) | `config.PRIMARY_METRIC` |
| Seed | 42 | `config.RANDOM_STATE` |
| CSP components | 6 (fixed, not tuned on test data) | `config.N_CSP_COMPONENTS` |
| Code license | MIT | `LICENSE` |
| Dataset license | ODC-By 1.0 (separate; data not redistributed) | `CITATION.md` |

### Aggregate results (ROC-AUC, 10 subjects)

| Pipeline | Mean | Median | Std | IQR | Min | Max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CSP+LDA | 0.653 | 0.665 | 0.234 | 0.283 | 0.23 | 1.00 |
| Dummy | 0.530 | 0.510 | 0.076 | 0.103 | 0.46 | 0.695 |
| LogVariance+LDA | 0.658 | 0.670 | 0.117 | 0.173 | 0.46 | 0.80 |

Source: `results/aggregate_scores.csv`.

### Per-subject results (ROC-AUC)

| Subject | CSP+LDA | LogVariance+LDA | Dummy |
| ---: | ---: | ---: | ---: |
| 1 | 0.81 | 0.80 | 0.46 |
| 2 | 0.95 | 0.79 | 0.595 |
| 3 | 0.57 | 0.58 | 0.46 |
| 4 | 0.67 | 0.66 | 0.55 |
| 5 | 0.45 | 0.77 | 0.47 |
| 6 | 0.48 | 0.60 | 0.515 |
| 7 | 1.00 | 0.68 | 0.505 |
| 8 | 0.66 | 0.52 | 0.58 |
| 9 | 0.23 | 0.46 | 0.695 |
| 10 | 0.71 | 0.72 | 0.47 |

Source: `results/baseline_results.csv`.

### Derived facts (computed from the CSV on 2026-10-29)

These numbers are not written in the README, but they come straight from the
versioned data. They are safe to use in posts.

- **CSP+LDA scored below chance for 3 of 10 subjects** (5: 0.45; 6: 0.48;
  9: 0.23). The README says "at least one"; the exact count is 3.
- **LogVariance+LDA scored below chance for 1 of 10** (subject 9: 0.46).
- **Head to head, CSP+LDA vs LogVariance+LDA: 5–5.** Each method was better on
  five subjects.
- **Subjects with ROC-AUC ≥ 0.70:** 4 for CSP+LDA (1, 2, 7, 10) and 4 for
  LogVariance+LDA (1, 2, 5, 10).
- **Dummy beat CSP+LDA on 3 subjects** (5, 6 and 9).
- **Dummy reached 0.695** (subject 9): with about 9 test trials per fold,
  chance fluctuates a lot.
- **LogVariance+LDA's standard deviation (0.117) is half of CSP+LDA's (0.234).**
- MOABB's `time` column records about 0.49 s for CSP+LDA, 0.016 s for
  LogVariance+LDA and 0.004 s for Dummy (mean across subjects). It depends on
  the machine, so **do not use it as a performance claim**.

### Project size

- About 1,200 lines of Python (package, scripts and tests).
- 6 package modules, 2 scripts, 3 figures, 2 result CSVs and 1 report.
- 4 test files, all placeholders marked `skip` (checked on 2026-10-29:
  `4 skipped`).

---

## 5. Results and interpretation (the stories the numbers tell)

### 5.1 Above chance on average, but only on average

Both real methods averaged above 0.5 (0.653 and 0.658), and Dummy sat near
chance (0.530). That shows **classical methods can work for some subjects under
within-session conditions**, and the report claims nothing beyond that.

### 5.2 The average hides the people the system fails

CSP+LDA ranged from 0.23 to 1.00. Three subjects scored below chance. This is
a concrete example of a phenomenon known in the BCI literature (sometimes
called *BCI inefficiency*): some people do not reach good performance with the
standard approaches. **This is the project's strongest LinkedIn message**,
because it applies to any AI system judged only by its average.

### 5.3 The simple baseline tied the classical method

LogVariance+LDA, which learns no spatial filter at all, had practically the
same mean as CSP+LDA (0.658 vs 0.653), half the spread, and a 5–5 head-to-head
record. With only 10 subjects and no statistical test, **there is no winner**.
The lesson is methodological: without the simple baseline, CSP would look like
"the method that works".

*Hypothesis (not tested in the project):* with 64 channels, about 36 training
trials per fold and unregularized CSP, the covariance matrices are estimated
from little data, which may explain CSP's instability on some subjects. Testing
regularized CSP or Riemannian methods would be the natural next step. If you
use this in a post, present it as a hypothesis.

### 5.4 Dummy as a sanity check, and as a warning

Dummy's mean (0.530) confirms the evaluation is sound. But the same Dummy
reached 0.695 on one subject. With so few test trials, **a single 0.70 proves
nothing**. That is why the chance line is dashed on every figure.

### 5.5 Subject 7's 1.00 is not a headline

A perfect ROC-AUC with about 9 test trials per fold is possible and does not
generalize. Never quote it on its own.

---

## 6. What you can and cannot say

| ✅ OK to say | ❌ Do not say | Why |
| --- | --- | --- |
| "An offline, within-session benchmark on 10 subjects from a public dataset" | "My model reads minds" / "decodes thoughts" | It is offline binary classification of motor imagery. |
| "Mean ROC-AUC of 0.653 (CSP+LDA) and 0.658 (LogVariance+LDA), with large variation across subjects" | "65% accuracy" | The metric is ROC-AUC, not accuracy. |
| "Above chance on average for the selected subjects" | "Works for anyone" / "generalizes" | No cross-subject or cross-session test was run. |
| "A foundation for future BCI work" | "Production-ready BCI" / "real-time control" | No online decoding, no hardware integration. |
| "An educational, research-oriented project with no clinical purpose" | Any mention of diagnosis, rehabilitation or treatment as an outcome of the project | The README explicitly excludes clinical use. |
| "LogVariance+LDA had a comparable mean and half the spread" | "LogVariance+LDA is better than CSP" | n = 10, no statistical test. |
| "Reproducible with two commands, data downloaded on demand" | "Covered by an automated test suite" | Current tests are placeholders. |
| "Open source under the MIT license" | "My own dataset" / "I collected the data" | The data comes from PhysioNet (ODC-By 1.0). |

---

## 7. Engineering decisions (behind-the-scenes material)

Each decision below can become a short post in the format "problem → decision
→ why it matters".

1. **Classical baselines before deep learning.** v1 deliberately excludes deep
   learning. First establish a trustworthy evaluation; then compare any new
   model against it.
2. **Within-session first, cross-subject later.** The MOABB snapshot has one
   session per subject, so within-session is the cleanest protocol for v1.
   Cross-subject is a separate experiment with a separate interpretation.
3. **CSP inside the pipeline.** CSP is supervised; keeping it inside the
   scikit-learn `Pipeline` ensures it is fitted only on training folds. That
   prevents data leakage.
4. **Fixed, documented hyperparameters.** Six CSP components, chosen before
   seeing any results. Any future tuning will use nested cross-validation.
5. **A single evaluation call for every pipeline.** Guarantees the three are
   compared on exactly the same train/test splits.
6. **A random classifier as a mandatory reference.** Dummy shows where chance
   sits *for this dataset* and *this number of trials*.
7. **ROC-AUC as the primary metric.** Threshold-independent, with a well-defined
   chance level (0.5) for binary tasks.
8. **Data hygiene.** Raw EEG and MOABB/MNE caches never enter git; only curated
   CSVs and figures are versioned. The code license (MIT) is kept separate from
   the data license (ODC-By 1.0).
9. **A deliberately small subset.** Ten subjects make every result inspectable
   and the whole run quick to reproduce.
10. **A single source of truth.** Every fixed choice lives in `config.py`, with
    comments explaining why.
11. **Incremental releases.** v0.1 (structure and protocol, nothing run) → v0.2
    (first benchmark) → v0.3 (analysis and figures) → v0.4 (extra baselines) →
    v1.0 (report and polish), with `BCI-xxx` backlog items in `ROADMAP.md`.

---

## 8. Timeline

| Date | Version | Commit | What shipped |
| --- | --- | --- | --- |
| 2026-06-08 | v0.1 | `a64fbd7` | Repository structure, evaluation protocol, scope, citations, license |
| 2026-06-08 | v0.2 | `4321add` | First MOABB within-session benchmark with CSP+LDA |
| 2026-06-08 | v0.3 | `8e9ef25` | Result analysis, aggregate summary and figures |
| 2026-06-08 | v0.4 | `d604e9f` | Dummy and LogVariance+LDA baselines |
| 2026-06-08 | v1.0 | `beba3ba` | Final report, README and documentation |

No git tag or GitHub release exists yet (see §18).

---

## 9. Stack and skills

**Technologies:** Python 3.11+, MOABB (≥ 1.0), MNE-Python (≥ 1.6),
scikit-learn (≥ 1.3), pandas, NumPy, Matplotlib, seaborn, pytest.

**Skills to tag on LinkedIn** (pick the ones most relevant to the role you are
targeting):

- Python
- Machine Learning
- Signal Processing
- Electroencephalography (EEG)
- Brain-Computer Interfaces
- scikit-learn
- Model Evaluation / Cross-Validation
- Data Science
- Reproducible Research
- Neurotechnology

**Skills shown, in recruiter language**

- Designing the experimental protocol before writing the model.
- Preventing data leakage and comparing models fairly.
- Reporting results honestly, failure cases included.
- Structuring a scientific project as software (package, scripts, central
  configuration, licensing).

---

## 10. Available visual assets

| File | What it shows | Best use | Caveats |
| --- | --- | --- | --- |
| `figures/score_distribution.png` (1039×680) | Box plot per pipeline with every subject's point and the chance line | **Main image.** Shows mean and spread at once. | Explain that each dot is one person. |
| `figures/per_subject_scores.png` (1039×680) | Bars per subject and pipeline, chance dashed | Posts about variation between people | **The legend covers the bars for subjects 7 to 10** (the CSP bar for subject 9 is partly hidden). Regenerate with the legend outside the plot before using it as a main image. |
| `figures/pipeline_comparison.png` (1039×680) | Mean ± std per pipeline | Overall comparison | On its own it reinforces "the average". Pair it with one of the other two. |

**LinkedIn format:** the figures are landscape (about 3:2). In the feed,
portrait images (1080×1350, 4:5) take up more screen. For a multi-image post,
the best format is a **carousel** (PDF document post).

**Suggested carousel outline (7 slides, 1080×1350)**

1. Cover: "A 0.65 average hides a 0.23" + project name.
2. What motor imagery and BCI are, in two sentences.
3. The protocol: public dataset, 10 subjects, within-session, 3 pipelines,
   identical splits.
4. Aggregate result (`pipeline_comparison.png`).
5. The twist: every dot is a person (`score_distribution.png`).
6. What this project does NOT prove (list from §6).
7. Next steps + GitHub link + dataset credits.

**Missing asset:** a repository cover image (GitHub *social preview*,
1280×640), which shows up when the link is shared on LinkedIn.

---

## 11. Audience, positioning and tone

### Who the posts speak to

| Audience | What they look for | What to highlight |
| --- | --- | --- |
| Recruiters and engineering managers | Signs of rigor, ownership and communication | Well-defined scope, incremental releases, explicit limitations |
| ML and data science people | Methodology | Data leakage, baselines, ROC-AUC, per-subject variation |
| Neurotech and BCI community | Domain depth | MOABB, CSP, within-session vs cross-subject, PhysionetMI |
| Students and academia | Learning material | Two-command reproduction, methodology report |
| Curious general public | Understanding what a BCI is | Simple explanations without hype |

### Suggested positioning

> Software engineering applied to neurotechnology: projects built on real
> public data, with transparent evaluation and limitations written down before
> the results.

### Tone of voice

- First person, direct, technical but accessible.
- Showing what did **not** work is part of the message, not a problem.
- Avoid words like "revolutionary", "mind reading" or "the future is here".
- Short paragraphs, one idea each, at most 2 or 3 functional emojis (for
  example → or ✅) if any.

### LinkedIn format notes (check them, limits change)

- Post: up to 3,000 characters. Only the first lines (about 200 characters)
  show before "see more", so the hook has to live there.
- "Projects" section description: up to 2,000 characters.
- Profile headline: up to 220 characters. "About" section: up to 2,600
  characters.
- Carousel: PDF document post, portrait (1080×1350) or square slides.
- Hashtags: 3 to 5 relevant ones work better than long lists.

---

## 12. Bank of post angles

Each angle has a hook, key points, a visual and a call to action. They are
outlines, not finished posts.

### A. Project launch (overview)
- **Hook:** "I built a brain-computer interface benchmark. The most important
  result wasn't the average."
- **Points:** what motor imagery is; public dataset; 3 pipelines; means 0.653
  and 0.658; spread from 0.23 to 1.00; what the project is not.
- **Visual:** `score_distribution.png` or the §10 carousel.
- **CTA:** GitHub link; "what would you check first in a BCI benchmark?"

### B. The average hides people
- **Hook:** "Mean of 0.65. Three out of ten people below chance."
- **Points:** per-subject table; *BCI inefficiency*; the parallel with any AI
  system judged only by its average.
- **Visual:** `per_subject_scores.png` (with the legend fixed).
- **Audience:** ML in general, recruiters.

### C. The simple baseline tied
- **Hook:** "The 'classical' method and the 'simple' method tied. 5–5."
- **Points:** CSP+LDA vs LogVariance+LDA; half the spread; n = 10, no winner;
  the small-sample covariance hypothesis (as a hypothesis).
- **Audience:** ML and neurotech.

### D. Why I trained a random classifier
- **Hook:** "The most important model in my benchmark never looks at the data."
- **Points:** Dummy mean 0.530; it reached 0.695 on one subject; why few trials
  make chance unstable; chance line on every figure.

### E. Within-session is not the same as working on someone else
- **Hook:** "When you read '90% accuracy' for a BCI, ask: tested on whom?"
- **Points:** within-session vs cross-session vs cross-subject; why this
  project states its protocol; cross-subject on the roadmap.
- **Audience:** general public and recruiters (educational).

### F. Data leakage in EEG
- **Hook:** "A one-line detail that inflates BCI results."
- **Points:** CSP is supervised; it must be fitted on training data only;
  scikit-learn `Pipeline`; hyperparameters fixed before seeing the test set.
- **Audience:** ML.

### G. What my project does NOT do
- **Hook:** "I wrote the limitations before the results."
- **Points:** list from §6; why explicit scope builds credibility.

### H. Behind the scenes: from v0.1 to v1.0
- **Hook:** "v0.1 of my benchmark didn't run a single model, on purpose."
- **Points:** v0.1 with only protocol and structure; `BCI-xxx` backlog;
  incremental releases.

### I. Open science and licenses
- **Hook:** "My code is MIT. The data isn't mine."
- **Points:** ODC-By 1.0; data not redistributed; attribution; caches kept
  out of git.

### J. A series with the other projects
- **Hook:** "Before classifying EEG, I had to understand the signal."
- **Points:** link to the EEG Signal Processing Lab (§17).

---

## 13. Glossary for plain-language posts

| Term | Plain explanation |
| --- | --- |
| **EEG** | A recording of the brain's electrical activity through electrodes on the scalp. |
| **BCI (brain-computer interface)** | A system that tries to turn brain signals into commands. |
| **Motor imagery** | Imagining a movement without performing it. It changes EEG rhythms over the motor cortex. |
| **CSP (Common Spatial Patterns)** | A technique that learns electrode combinations that best separate two classes. |
| **LDA** | A simple linear classifier that separates two classes with a line (or plane). |
| **Log-variance** | A measure of the signal's "energy" in each channel, used as a feature. |
| **ROC-AUC** | A 0-to-1 score of how well the model ranks examples; 0.5 is chance, 1.0 is perfect. |
| **Chance level** | The result you would expect from guessing. Here, 0.5. |
| **Within-session** | Training and testing on data from the same session of the same person. |
| **Cross-subject** | Training on some people and testing on someone else. Much harder. |
| **Data leakage** | When information from the test set leaks into training and inflates results. |
| **Cross-validation (fold)** | Splitting the data into parts and rotating which part is the test set. |
| **MOABB** | A BCI benchmarking library that standardizes datasets, paradigms and evaluations. |
| **Baseline** | A reference model, usually simple, to compare the others against. |

---

## 14. Hashtags and keywords

**Hashtags (pick 3 to 5 per post)**

- Core: `#BCI` `#EEG` `#Neurotechnology` `#MachineLearning` `#Python`
- Reach: `#BrainComputerInterface` `#SignalProcessing` `#OpenScience`
  `#ReproducibleResearch` `#Neuroscience` `#DataScience`
- Portuguese-speaking reach: `#Neurotecnologia` `#InterfaceCérebroComputador`
  `#CiênciaDeDados`

**Keywords for search and profile SEO:** brain-computer interface, BCI, EEG,
motor imagery, CSP, LDA, MOABB, MNE-Python, scikit-learn, PhysioNet,
reproducible evaluation, neurotechnology.

---

## 15. Credits and citations

**Short line for the end of a post**

> Data: PhysioNet EEG Motor Movement/Imagery Dataset (Schalk et al., 2004;
> Goldberger et al., 2000), ODC-By 1.0. Tools: MOABB, MNE-Python and
> scikit-learn.

**Full references** (details and BibTeX in `CITATION.md`)

- Schalk, G. et al. (2004). BCI2000: A General-Purpose Brain-Computer
  Interface (BCI) System. *IEEE Trans. Biomed. Eng.*, 51(6), 1034–1043.
- Goldberger, A. L. et al. (2000). PhysioBank, PhysioToolkit, and PhysioNet.
  *Circulation*, 101(23), e215–e220.
- Jayaram, V. & Barachant, A. (2018). MOABB: Trustworthy Algorithm
  Benchmarking for BCIs. *J. Neural Eng.*, 15(6), 066011.
- Gramfort, A. et al. (2013). MEG and EEG Data Analysis with MNE-Python.
  *Front. Neurosci.*, 7, 267.
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python.
  *JMLR*, 12, 2825–2830.

**Useful links**

- Dataset: https://physionet.org/content/eegmmidb/1.0.0/
- MOABB: https://moabb.neurotechx.com/docs/index.html

---

## 16. Roadmap and update triggers

What is planned (`ROADMAP.md`, "Future" section) and the post each delivery
would enable:

| Future delivery | Post it enables |
| --- | --- |
| Full 109-subject benchmark | "Does the variation between people hold at scale?" (compare with the v1 numbers) |
| Cross-subject evaluation | "What happens when the model meets a new person" (likely the strongest post in the series) |
| Nested cross-validation tuning | "How to tune hyperparameters without cheating" |
| Riemannian pipelines (Covariance+MDM, TangentSpace+LR) | "Covariance-matrix geometry in BCI": tests the §5.3 hypothesis |
| Deep learning (EEGNet, Braindecode) | "Deep learning vs honest baselines" |
| Real-time biosignal dashboard / BrainFlow (separate project) | A change of scope: from offline benchmark to online system |

**Rule:** every update should compare against the v1 numbers (§4) under the
same protocol, or state clearly what changed.

---

## 17. How it fits the portfolio

This is one of three public projects that form a coherent story:

| Project | Question it answers | Date |
| --- | --- | --- |
| [EEG Signal Processing Lab](https://github.com/jevrton-code/eeg-signal-processing-lab) | How do you load, inspect, preprocess and analyze EEG responsibly? | Jun 2026 |
| **BCI Motor Imagery Classifier** (this one) | Can motor imagery be classified, and how do you evaluate that honestly? | Jun 2026 |
| [FlyWire Propagation Sim](https://github.com/jevrton-code/flywire-propagation-sim) | How does activity spread through a real neural circuit, mapped synapse by synapse? | Aug 2026 |

**The common thread:** real public data, reproducibility, disciplined software
engineering and honesty about limits. The EEG Lab and this project use the
**same dataset** (PhysioNet EEGMMIDB): the first one understands the signal,
the second builds classifiers on top of it. FlyWire moves from the signal
measured on the scalp to the brain's wiring diagram, with a full-stack app.

**Possible portfolio post:** "Three projects, one rule: write down what the
model doesn't do before showing what it does."

---

## 18. Issues to fix before promoting the project

Things in the repository that a visitor coming from LinkedIn might notice.
Worth fixing before a launch post.

1. **Placeholder URLs in `pyproject.toml`:** `Homepage` and `Repository` point
   to `github.com/your-org/...`. Change them to `jevrton-code`.
2. **Outdated version in `CITATION.md`:** the repository citation says
   "Version 0.1.0"; the package is at 1.0.0.
3. **Tests are placeholders:** all 4 tests are marked `skip` (checked:
   `4 skipped`). Implementing real tests for configuration, result schema and
   metric summary would make a good "v1.1" post.
4. **Links to `docs/`, which is not in the repository:** the README points to
   `docs/evaluation_protocol.md` and the report to `docs/limitations.md`, but
   `docs/` is in `.gitignore` (local documents). For visitors these are broken
   links.
5. **Overlapping legend** in `figures/per_subject_scores.png` (§10).
6. **Empty `notebooks/` folder** (notebooks marked as planned).
7. **No tag or GitHub release.** Creating a `v1.0.0` release gives a stable
   link and a milestone to announce.
8. **No *social preview* image** set on GitHub (§10).

---

## 19. Personal context to fill in (what the repository can't know)

Posts with personal context tend to sound more authentic. Fill in what makes
sense:

- **Why this project:** [TO FILL IN]
- **Your background and path so far:** [TO FILL IN]
- **Time invested and context** (personal project, course, career change):
  [TO FILL IN]
- **What was hardest or most surprising:** [TO FILL IN]
- **Tools used along the way**, including AI assistants if you want to mention
  them: [TO FILL IN]
- **Career goal** (type of role, field, companies of interest): [TO FILL IN]
- **People or communities to thank or tag:** [TO FILL IN]
- **Your LinkedIn profile URL:** [TO FILL IN]

---

## 20. Document changelog

| Date | Change |
| --- | --- |
| 2026-10-29 | First version, covering the project at v1.0.0 (`beba3ba`). Numbers checked against `results/*.csv`; tests run locally (`4 skipped`). |
