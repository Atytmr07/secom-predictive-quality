"""Walk-forward (zaman ileri) değerlendirme: drift'e karşı özellik sayısı ve pencere stratejisi."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import VarianceThreshold, SelectKBest, mutual_info_classif
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, roc_auc_score
from functools import partial
from data import load_secom

X, y, t = load_secom()
X = X.loc[:, X.isna().mean() <= 0.5]
N, FIRST, BLOCK = len(X), 500, 150  # ilk 500 gözlemle başla, 150'şerlik bloklarla ilerle


def make(model, k):
    steps = [("imp", SimpleImputer(strategy="median")), ("var", VarianceThreshold(0)), ("sc", StandardScaler())]
    if k: steps.append(("sel", SelectKBest(partial(mutual_info_classif, random_state=0), k=k)))
    return Pipeline(steps + [("m", model)])


rf = lambda: RandomForestClassifier(300, min_samples_leaf=5, max_features="sqrt", class_weight="balanced_subsample", n_jobs=-1, random_state=0)
lr = lambda: LogisticRegression(C=0.01, class_weight="balanced", max_iter=2000)
configs = {  # ad: (model, k, pencere: None=genişleyen, int=kayan)
    "RF k=40 genişleyen": (rf, 40, None), "RF k=10 genişleyen": (rf, 10, None), "RF tüm özellik genişleyen": (rf, 0, None),
    "RF k=10 kayan(500)": (rf, 10, 500), "LogReg k=10 genişleyen": (lr, 10, None), "LogReg k=20 kayan(500)": (lr, 20, 500),
}
rows = []
for name, (mk, k, win) in configs.items():
    ps, ys = [], []
    for s in range(FIRST, N - 1, BLOCK):
        e = min(s + BLOCK, N); lo = 0 if win is None else max(0, s - win)
        ytr = y.iloc[lo:s]
        if ytr.sum() < 5: continue
        p = make(mk(), k).fit(X.iloc[lo:s], ytr).predict_proba(X.iloc[s:e])[:, 1]
        ps.append(p); ys.append(y.iloc[s:e].values)
    p, yy = np.concatenate(ps), np.concatenate(ys)
    rows.append(dict(config=name, prauc=average_precision_score(yy, p), roc=roc_auc_score(yy, p), base=yy.mean()))
res = pd.DataFrame(rows).round(3).sort_values("prauc", ascending=False)
print(res.to_string(index=False)); res.to_csv("../reports/temporal_results.csv", index=False)
