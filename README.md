# Predictive Quality on SECOM: Does a Defect Model Survive Time?

Machine-learning study of defect prediction on the public [UCI SECOM](https://archive.ics.uci.edu/dataset/179/secom) semiconductor manufacturing dataset (1,567 production runs, 590 anonymised sensors, 6.6% defects).

The main question is not only *which model is best*, but *whether the result holds when the model has to predict the future*.

## Key findings

| Evaluation | Best model | PR-AUC | Random-guess PR-AUC |
|---|---|---|---|
| Stratified 5-fold CV (x3) | Random Forest | 0.187 | 0.066 |
| Chronological 70/30 split | Logistic Regression + SMOTE | 0.073 | 0.055 |
| Walk-forward (expanding window) | Random Forest, all features | 0.067 | 0.042 |

- Random cross-validation looks promising; time-aware validation removes most of that advantage (concept drift, few positives).
- Even a weak model can pay off with a cost-sensitive threshold: with a missed-defect cost 10x the false-alarm cost, total cost drops ~35% versus "no inspection" (cost ratios are assumptions, not plant data).

## Pipeline

median imputation -> variance filter -> scaling -> mutual-information selection (k=40) -> class weights or SMOTE -> Logistic Regression / Random Forest / XGBoost. All steps are fitted inside CV folds (no leakage). Metrics: PR-AUC, ROC-AUC, best-threshold F1, MCC; accuracy is deliberately not used.

## Structure

```
src/data.py          load SECOM, time-ordered
src/eda.py           exploratory plots
src/models.py        model comparison (CV + chronological split)
src/temporal.py      walk-forward evaluation
src/cost_shap.py     cost-sensitive threshold + SHAP
notebooks/01_ozet.ipynb   summary of all outputs
reports/             figures and result tables
```

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# download https://archive.ics.uci.edu/static/public/179/secom.zip and unzip into data/raw/
cd src && python eda.py && python models.py && python temporal.py && python cost_shap.py
```

## Limitations

Only 104 defective samples; anonymised sensors (no domain feature engineering); drift across the 3-month window; cost ratios assumed.
