![Customer Churn](docs/assets/banner.svg)

[![CI](https://github.com/Preritsangwan17/Churn-ml-model-project/actions/workflows/ci.yml/badge.svg)](https://github.com/Preritsangwan17/Churn-ml-model-project/actions/workflows/ci.yml)

# Customer Churn Prediction

A reproducible machine-learning baseline that scores telecom customer churn from customer and service
attributes. It compares Logistic Regression and Random Forest, selects using validation Average Precision,
and tunes a validation F1 threshold before evaluating an untouched test partition.


**Project status:** evaluated research baseline with reproducible training and batch prediction.

[Quick start](#quick-start) · [Results](#reproduced-baseline) · [Model card](docs/MODEL_CARD.md) · [Tests](#tests) · [Contributing](CONTRIBUTING.md)

## Engineering highlights

- One saved pipeline includes imputation, scaling, categorical encoding and the classifier.
- Customer IDs and exported CSV index columns are excluded from features.
- Blank `TotalCharges` values are treated as missing; malformed numbers fail clearly.
- Unknown categories are supported at prediction time.
- Stratified 60/20/20 partitions separate training, selection and final evaluation.
- The saved bundle records features, label mapping, threshold and evaluation metadata.

## Quick start

```bash
git clone https://github.com/Preritsangwan17/Churn-ml-model-project.git
cd Churn-ml-model-project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py train
python app.py predict --input examples/customers.csv --output artifacts/predictions.csv
```

Windows: activate with `.venv\Scripts\Activate.ps1` in PowerShell. Python 3.11 or 3.12 is recommended.

## Data and workflow

The included `WA_Fn-UseC_-Telco-Customer-Churn.csv` is the Telco customer-churn sample.
Target: `Churn`, mapped as `No=0`, `Yes=1`. Record the original dataset source and its redistribution
terms before republishing these sample files elsewhere; the repository has no independently verified
dataset source/license record.

Data → remove exact raw duplicate records → stratified split → train-only preprocessing → validation
model and threshold selection → final test metrics → artifact and batch predictions.

## Reproduced baseline

Executed on the repository's raw CSV with seed 42 and scikit-learn 1.6.1. The 7,043 customer rows are
split into 4,225 train / 1,409 validation / 1,409 test. Exact raw duplicate records are removed before
excluding customer IDs; distinct customers with identical feature values remain separate observations.
Selected model: **Logistic Regression**.

| Held-out metric | Value |
|---|---:|
| Precision | 0.5479 |
| Recall | 0.7032 |
| F1 | 0.6159 |
| Average Precision | 0.6332 |
| ROC AUC | 0.8426 |

Confusion matrix: `[[818, 217], [111, 263]]` (rows actual No/Yes; columns predicted No/Yes).
Threshold: `0.609812`. Inspect the full [evaluation record](reports/baseline.metrics.json).
Scores reflect this split of a sample dataset, not measured business retention impact.

## Repository guide

| Path | Purpose |
|---|---|
| `churn/pipeline.py` | Data validation, training, evaluation and inference |
| `app.py` | Train/predict CLI |
| `tests/` | Artifact round-trip and schema regression tests |
| `reports/` | Reproduced evaluation record |
| `artifacts/` | Generated local model and prediction outputs, ignored by Git |
| `model.sav`, `tel_churn.csv` | Preserved legacy artifact and transformed data; new pipeline does not use them |

## Limitations and next improvements

Class-weighted scores are not calibrated churn probabilities. A validation F1 threshold does not encode
retention cost or campaign capacity. Add temporal validation, cost-based threshold selection and
calibration before operational use. The original `model.sav` has no verified training environment;
train a fresh bundle with this pipeline instead of relying on it.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Synthetic fixtures check software behavior; the evaluation above uses the real repository CSV.
Only load serialized models you trust. See [contribution guidance](CONTRIBUTING.md).

Built by [Prerit Sangwan](https://github.com/Preritsangwan17), B.Tech CSE (AI/ML).

## Model documentation

See the [model card](docs/MODEL_CARD.md) for the intended use, input contract, evaluation method and limitations.
For the recorded numerical environment, install `requirements-repro.txt` in a fresh virtual environment.
