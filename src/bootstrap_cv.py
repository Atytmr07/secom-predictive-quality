"""CV tahminleri için PR-AUC bootstrap güven aralıkları (model farkları gürültü mü?)"""
import numpy as np, pandas as pd
from sklearn.metrics import average_precision_score
from data import load_secom
_, y, _ = load_secom(); y = y.values
oof = pd.read_csv("../reports/oof_preds.csv"); rng = np.random.default_rng(0); rows = []
idx = [rng.integers(0, len(y), len(y)) for _ in range(1000)]
for c in oof:
    v = [average_precision_score(y[i], oof[c].values[i]) for i in idx]
    rows.append(dict(model=c, prauc=average_precision_score(y, oof[c]), lo=np.percentile(v, 2.5), hi=np.percentile(v, 97.5)))
r = pd.DataFrame(rows).round(3); print(r.to_string(index=False)); r.to_csv("../reports/cv_bootstrap.csv", index=False)
