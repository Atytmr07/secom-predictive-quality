"""RQ1: Aynı model, farklı doğrulama protokolleri. Rastgele CV, blok CV, tek kronolojik bölme, walk-forward.
Protokollerin pozitif oranı farklı olduğu için PR-AUC yanında 'lift' (PR-AUC / pozitif oranı) raporlanır."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.metrics import average_precision_score, roc_auc_score
from models import models, X, y

N = len(X)
MODELS = {k: models[k] for k in ["LogReg (class_weight)", "RandomForest", "XGBoost"]}
rng = np.random.default_rng(0)


def pooled(splits, pipe):
    """splits: (train_idx, test_idx) listesi. Tüm test tahminleri birleştirilip tek PR-AUC hesaplanır."""
    idx, ps = [], []
    for tr, te in splits:
        m = clone(pipe).fit(X.iloc[tr], y.iloc[tr])
        ps.append(m.predict_proba(X.iloc[te])[:, 1]); idx.append(te)
    return np.concatenate(idx), np.concatenate(ps)


def summarize(name, proto, idx, p, rows, B=500):
    yy = y.iloc[idx].values; base = yy.mean()
    ap, roc = average_precision_score(yy, p), roc_auc_score(yy, p)
    lifts = []
    for _ in range(B):
        i = rng.integers(0, len(yy), len(yy))
        if yy[i].sum() > 0:
            lifts.append(average_precision_score(yy[i], p[i]) / yy[i].mean())
    lo, hi = np.percentile(lifts, [2.5, 97.5])
    rows.append(dict(model=name, protocol=proto, n_test=len(yy), base_rate=base, prauc=ap, lift=ap / base,
                     lift_lo=lo, lift_hi=hi, roc=roc))


def protocol_splits():
    r = {}
    r["Random stratified 5-fold"] = list(StratifiedKFold(5, shuffle=True, random_state=0).split(X, y))
    r["Blocked 5-fold (contiguous, future in train)"] = list(KFold(5, shuffle=False).split(X))
    cut = int(N * .7); r["Chronological 70/30"] = [(np.arange(cut), np.arange(cut, N))]
    wf = []
    for s in range(500, N - 1, 150):
        wf.append((np.arange(s), np.arange(s, min(s + 150, N))))
    r["Walk-forward (expanding)"] = wf
    return r


if __name__ == "__main__":
    rows = []
    for name, pipe in MODELS.items():
        for proto, sp in protocol_splits().items():
            idx, p = pooled(sp, pipe)
            summarize(name, proto, idx, p, rows)
            print(name, "|", proto, "done", flush=True)
    res = pd.DataFrame(rows)
    res.round(3).to_csv("../reports/protocol_comparison.csv", index=False)
    print(res.round(3).to_string(index=False))
