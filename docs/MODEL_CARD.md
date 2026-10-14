# Model card: Telecom customer churn

## Purpose and scope

Research baseline for the included Telco sample. Target `Churn=Yes` is mapped to positive class 1.
A score prioritizes further investigation; it does not establish that a customer will leave or that
an intervention will retain them.

## Inputs and artifact

Raw customer/service attributes in the source CSV. `customerID` and exported index columns are excluded.
Blank `TotalCharges` values are imputed. Numeric preprocessing and one-hot encoding are fitted on training
rows only. The bundle records feature names/types, labels, threshold, fingerprint and environment versions.
Unknown categorical values are accepted; missing feature columns are rejected.
Repeated non-null customer IDs must be resolved before training to avoid entity overlap across partitions.

## Evaluation

Raw exact duplicates removed before ID exclusion; other customers with identical feature values are retained.
7,043 rows are split 4,225 train / 1,409 validation / 1,409 test, stratified with seed 42.
Model selection uses validation AP and threshold selection uses validation F1.
Inspect [the current report](../reports/baseline.metrics.json) for actual scores and positive-class prevalence.

## Limits

Class-weighted scores are uncalibrated. A row-split sample does not prove future-time prediction quality,
retention uplift or profitability. Missing source collection dates and an independent source-license record
limit provenance. Retention-cost thresholds, calibration and temporal validation remain future work.

## Reproduction

```bash
python app.py train
python app.py predict --input examples/customers.csv --output artifacts/predictions.csv
```

Only load trusted serialized models. Example rows are fictional and are not test-set evidence.
