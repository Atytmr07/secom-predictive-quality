# Predictive Quality on SECOM: Does a Defect Model Survive Time?

Machine-learning study of defect prediction on the public [UCI SECOM](https://archive.ics.uci.edu/dataset/179/secom) semiconductor manufacturing dataset (1,567 production runs, 590 anonymised sensors, 6.6% defects).

The main question is not only *which model is best*, but *whether the result holds when the model has to predict the future*.

## Key findings

| Evaluation | Best model | PR-AUC | Random-guess PR-AUC |
|---|---|---|---|
| Stratified 5-fold CV (x3) | Random Forest | 0.187 | 0.066 |
| Chronological 70/30 split | Logistic Regression + SMOTE | 0.073 | 0.055 |
| Walk-forward (expanding window) | Random Forest, all features | 0.067 | 0.042 |

- **Validation protocol matters.** For the same Random Forest, the lift over random guessing falls from 2.7 (random stratified CV) to 1.6 (blocked CV) to ~1.0 (chronological 70/30) and ~1.1 (walk-forward). See `reports/protocol_comparison.csv`.
- **Sensors do drift:** 61% of usable sensors differ significantly between the first 70% and last 30% of the timeline (KS test, Bonferroni), and 78% of the 40 sensors selected by mutual information.
- **But drift alone does not explain the collapse.** Sensors flagged as drifting using only the training period do shift more on the test period (mean KS 0.21 vs 0.11), yet a Random Forest trained on stable sensors performs no better than one trained on drifting or random sensors of the same size (all near chance). The weak out-of-time performance is probably due to a weak/non-stationary signal and few positives rather than to a few drifting sensors.
- A classical SPC chart (PCA-based Hotelling T²) is also at chance level on the chronological test; bootstrap 95% CIs include the random baseline for both SPC and ML.
- Cost-sensitive thresholds look useful under random CV (with a missed-defect cost 10x the false-alarm cost, total cost drops ~35% versus "no inspection"), but **this does not hold out of time**: when the threshold is chosen on the training period and applied to the later 30% of runs, models do not beat the best trivial strategy (no inspection / full inspection) for any tested cost ratio (`reports/cost_chronological.csv`). Cost ratios are assumptions, not plant data.

## Pipeline

median imputation -> variance filter -> scaling -> mutual-information selection (k=40) -> class weights or SMOTE -> Logistic Regression / Random Forest / XGBoost. All steps are fitted inside CV folds (no leakage). Metrics: PR-AUC, ROC-AUC, best-threshold F1, MCC; accuracy is deliberately not used.

## Structure

```
src/data.py          load SECOM, time-ordered
src/eda.py           exploratory plots
src/models.py        model comparison (CV + chronological split)
src/temporal.py      walk-forward evaluation
src/drift.py         KS-test drift analysis
src/drift_link.py    drift vs predictive performance (stable/drifting/random sensor subsets)
src/protocols.py     random vs blocked vs chronological vs walk-forward validation
src/eda_extra.py     outliers, correlation structure, boxplots
src/spc.py           Hotelling T2 vs Random Forest + bootstrap CIs
src/bootstrap_cv.py  bootstrap CIs for CV results
src/cost_time.py      cost analysis with threshold chosen on training period, tested on later runs
src/cost_shap.py     cost-sensitive threshold + SHAP
notebooks/01_ozet.ipynb   summary of all outputs
reports/             figures and result tables
```

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# download https://archive.ics.uci.edu/static/public/179/secom.zip and unzip into data/raw/
cd src && python eda.py && python models.py && python temporal.py && python drift.py && python drift_link.py && python protocols.py && python eda_extra.py && python spc.py && python bootstrap_cv.py && python cost_shap.py
```

## Limitations

Only 104 defective samples; anonymised sensors (no domain feature engineering); drift across the 3-month window; cost ratios assumed.
