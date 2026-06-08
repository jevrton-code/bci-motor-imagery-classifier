# Citation

If you use this repository, please cite the underlying dataset and tooling. This repository's own code and documentation are licensed under the MIT License (see `LICENSE`), which is **separate** from the dataset license.

## Dataset License Notice

The PhysioNet EEG Motor Movement/Imagery Dataset is distributed under **ODC-By 1.0 (Open Data Commons Attribution License v1.0)**. This is independent of this repository's MIT license. The dataset is **not** redistributed in this repository; it is accessed on demand through MOABB. When you use the data, you must comply with its ODC-By 1.0 attribution terms and cite the sources below.

## How to Cite

Please cite: (1) the PhysioNet EEG Motor Movement/Imagery Dataset and BCI2000, (2) PhysioNet, (3) MOABB, (4) MNE-Python, and (5) scikit-learn.

### PhysioNet EEG Motor Movement/Imagery Dataset (BCI2000)

- Schalk, G., McFarland, D. J., Hinterberger, T., Birbaumer, N., & Wolpaw, J. R. (2004). BCI2000: A General-Purpose Brain-Computer Interface (BCI) System. *IEEE Transactions on Biomedical Engineering*, 51(6), 1034-1043.
- Dataset URL: https://physionet.org/content/eegmmidb/1.0.0/

```bibtex
@article{schalk2004bci2000,
  title   = {{BCI2000}: A General-Purpose Brain-Computer Interface ({BCI}) System},
  author  = {Schalk, Gerwin and McFarland, Dennis J. and Hinterberger, Thilo and
             Birbaumer, Niels and Wolpaw, Jonathan R.},
  journal = {IEEE Transactions on Biomedical Engineering},
  volume  = {51},
  number  = {6},
  pages   = {1034--1043},
  year    = {2004},
  doi     = {10.1109/TBME.2004.827072}
}
```

### PhysioNet (PhysioBank, PhysioToolkit, PhysioNet)

- Goldberger, A. L., Amaral, L. A. N., Glass, L., Hausdorff, J. M., Ivanov, P. Ch., Mark, R. G., Mietus, J. E., Moody, G. B., Peng, C.-K., & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a New Research Resource for Complex Physiologic Signals. *Circulation*, 101(23), e215-e220.
- URL: https://physionet.org/

```bibtex
@article{goldberger2000physionet,
  title   = {{PhysioBank}, {PhysioToolkit}, and {PhysioNet}: Components of a New
             Research Resource for Complex Physiologic Signals},
  author  = {Goldberger, Ary L. and Amaral, Luis A. N. and Glass, Leon and
             Hausdorff, Jeffrey M. and Ivanov, Plamen Ch. and Mark, Roger G. and
             Mietus, Joseph E. and Moody, George B. and Peng, Chung-Kang and
             Stanley, H. Eugene},
  journal = {Circulation},
  volume  = {101},
  number  = {23},
  pages   = {e215--e220},
  year    = {2000},
  doi     = {10.1161/01.CIR.101.23.e215}
}
```

### MOABB (Mother of All BCI Benchmarks)

- Jayaram, V., & Barachant, A. (2018). MOABB: Trustworthy Algorithm Benchmarking for BCIs. *Journal of Neural Engineering*, 15(6), 066011.
- URL: https://moabb.neurotechx.com/

```bibtex
@article{jayaram2018moabb,
  title   = {{MOABB}: Trustworthy Algorithm Benchmarking for {BCIs}},
  author  = {Jayaram, Vinay and Barachant, Alexandre},
  journal = {Journal of Neural Engineering},
  volume  = {15},
  number  = {6},
  pages   = {066011},
  year    = {2018},
  doi     = {10.1088/1741-2552/aadea0}
}
```

### MNE-Python

- Gramfort, A., Luessi, M., Larson, E., Engemann, D. A., Strohmeier, D., Brodbeck, C., Goj, R., Jas, M., Brooks, T., Parkkonen, L., & Hamalainen, M. (2013). MEG and EEG Data Analysis with MNE-Python. *Frontiers in Neuroscience*, 7, 267.
- URL: https://mne.tools/

```bibtex
@article{gramfort2013mne,
  title   = {{MEG} and {EEG} Data Analysis with {MNE-Python}},
  author  = {Gramfort, Alexandre and Luessi, Martin and Larson, Eric and
             Engemann, Denis A. and Strohmeier, Daniel and Brodbeck, Christian and
             Goj, Roman and Jas, Mainak and Brooks, Teon and Parkkonen, Lauri and
             H{\"a}m{\"a}l{\"a}inen, Matti},
  journal = {Frontiers in Neuroscience},
  volume  = {7},
  pages   = {267},
  year    = {2013},
  doi     = {10.3389/fnins.2013.00267}
}
```

### scikit-learn

- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.
- URL: https://scikit-learn.org/

```bibtex
@article{pedregosa2011scikit,
  title   = {Scikit-learn: Machine Learning in {P}ython},
  author  = {Pedregosa, Fabian and Varoquaux, Ga{\"e}l and Gramfort, Alexandre and
             Michel, Vincent and Thirion, Bertrand and Grisel, Olivier and
             Blondel, Mathieu and Prettenhofer, Peter and Weiss, Ron and
             Dubourg, Vincent and Vanderplas, Jake and Passos, Alexandre and
             Cournapeau, David and Brucher, Matthieu and Perrot, Matthieu and
             Duchesnay, {\'E}douard},
  journal = {Journal of Machine Learning Research},
  volume  = {12},
  pages   = {2825--2830},
  year    = {2011}
}
```

## Citing This Repository

```bibtex
@software{bci_motor_imagery_classifier,
  title  = {bci-motor-imagery-classifier},
  author = {{bci-motor-imagery-classifier contributors}},
  year   = {2026},
  note   = {Version 0.1.0. Reproducible EEG motor imagery classification
            benchmark using MOABB, PhysionetMI, and classical baselines.}
}
```
