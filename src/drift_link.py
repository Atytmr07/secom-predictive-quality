"""RQ2 (devam): Drift ile tahmin performansı arasındaki bağ.
Önemli: drift'li/stabil sensör ayrımı YALNIZCA eğitim dönemi (ilk %70) içinden yapılır
(eğitim dönemini ikiye böl, KS testi). Test dönemi (son %30) ayrımda kullanılmaz -> sızıntı yok."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from scipy.stats import ks_2samp
from sklearn.base import clone
from sklearn.metrics import average_precision_score, roc_auc_score
from models import models, X, y

X = X.loc[:, X.nunique() > 1]
cut = int(len(X) * .7); half = cut // 2
Xtr, ytr, Xte, yte = X.iloc[:cut], y.iloc[:cut], X.iloc[cut:], y.iloc[cut:]
pv = pd.Series({c: ks_2samp(Xtr[c].iloc[:half].dropna(), Xtr[c].iloc[half:].dropna()).pvalue for c in X.columns})
alpha = 0.05 / len(pv)
drifting = pv.index[pv < alpha]; stable = pv.index[pv >= 0.05]  # belirsiz bölgeyi (0.05/m..0.05) dışarıda bırak
print(f"Eğitim içi drift'li: {len(drifting)}, stabil: {len(stable)}, toplam: {len(pv)}")

# Test döneminde de gerçekten kaymış mı? (doğrulama amaçlı, seçimde kullanılmıyor)
ks_te = {c: ks_2samp(Xtr[c].dropna(), Xte[c].dropna()).statistic for c in X.columns}
print("Ortalama KS (eğitim vs test): drift'li %.3f | stabil %.3f" % (np.mean([ks_te[c] for c in drifting]), np.mean([ks_te[c] for c in stable])))

n = min(len(drifting), len(stable)); rng = np.random.default_rng(0)
base = yte.mean(); rows = []
pipe = models["RandomForest"]
def evaluate(cols):
    m = clone(pipe).fit(Xtr[cols], ytr); p = m.predict_proba(Xte[cols])[:, 1]
    return average_precision_score(yte, p), roc_auc_score(yte, p)
for label, pool in [("stabil sensörler", stable), ("drift'li sensörler", drifting), ("rastgele (tüm sensörler havuzu)", pd.Index(X.columns))]:
    res = [evaluate(list(rng.choice(pool, n, replace=False))) for _ in range(20)]  # eşit boyutlu 20 rastgele alt küme
    a = np.array(res)
    rows.append(dict(subset=label, n_sensors=n, prauc_mean=a[:, 0].mean(), prauc_sd=a[:, 0].std(), roc_mean=a[:, 1].mean(), roc_sd=a[:, 1].std(),
                     lift=a[:, 0].mean() / base))
    print(rows[-1], flush=True)
out = pd.DataFrame(rows).round(3); out["base_rate"] = round(base, 3)
out.to_csv("../reports/drift_performance_link.csv", index=False); print(out.to_string(index=False))
