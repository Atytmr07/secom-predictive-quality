"""RQ4 (katı kontrol): Eşik YALNIZCA eğitim dönemi OOF tahminlerinden seçilir, kronolojik test döneminde uygulanır."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from models import models, X, y

cut = int(len(X) * .7)
Xtr, ytr, Xte, yte = X.iloc[:cut], y.iloc[:cut], X.iloc[cut:], y.iloc[cut:]
ths = np.linspace(0, 1, 201); rows = []
def cost(p, yy, th, c_fn): return ((p < th) & (yy == 1)).sum() * c_fn + ((p >= th) & (yy == 0)).sum()
for name in ["LogReg (class_weight)", "RandomForest", "XGBoost"]:
    pipe = models[name]
    oof = cross_val_predict(clone(pipe), Xtr, ytr, cv=StratifiedKFold(5, shuffle=True, random_state=0), method="predict_proba")[:, 1]
    pte = clone(pipe).fit(Xtr, ytr).predict_proba(Xte)[:, 1]
    for c_fn in (5, 10, 20, 50):
        th = ths[int(np.argmin([cost(oof, ytr.values, t, c_fn) for t in ths]))]
        rows.append(dict(model=name, c_fn=c_fn, threshold_from_train=th, test_cost_model=cost(pte, yte.values, th, c_fn),
                         test_cost_no_inspection=int(yte.sum() * c_fn), test_cost_full_inspection=int((yte == 0).sum()),
                         train_cost_model=cost(oof, ytr.values, th, c_fn), train_cost_no_inspection=int(ytr.sum() * c_fn)))
r = pd.DataFrame(rows); r["test_best_trivial"] = r[["test_cost_no_inspection", "test_cost_full_inspection"]].min(axis=1)
r["test_saving_pct_vs_best_trivial"] = (100 * (1 - r.test_cost_model / r.test_best_trivial)).round(1)
r.round(3).to_csv("../reports/cost_chronological.csv", index=False); print(r.round(2).to_string(index=False))
