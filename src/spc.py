"""SPC (Hotelling T²) ile ML'i zaman sıralı testte kıyasla + bootstrap güven aralığı."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import average_precision_score, roc_auc_score
from data import load_secom
from models import models, X, y

cut = int(len(X) * .7)
Xtr, Xte, ytr, yte = X.iloc[:cut], X.iloc[cut:], y.iloc[:cut], y.iloc[cut:]

# --- SPC: yalnızca sağlam ürünlerle "normal" süreci öğren, T² büyükse alarm ---
imp = SimpleImputer(strategy="median").fit(Xtr[ytr == 0]); keep = Xtr.columns[~np.isnan(imp.statistics_)]
good = imp.transform(Xtr[ytr == 0]); sc = StandardScaler().fit(good)
pca = PCA(n_components=0.90).fit(sc.transform(good))
def t2(df):
    z = pca.transform(sc.transform(imp.transform(df)))
    return (z ** 2 / pca.explained_variance_).sum(1)
ucl = np.quantile(t2(Xtr[ytr == 0]), 0.99)
s_spc = t2(Xte)
alarm = s_spc > ucl
print(f"PCA bileşen sayısı: {pca.n_components_} | UCL(%99)={ucl:.1f} | test alarm oranı %{100*alarm.mean():.0f}")
print(f"SPC alarmı verilenlerde kusur oranı %{100*yte[alarm].mean():.1f} (genel %{100*yte.mean():.1f})")

# --- ML (Random Forest) aynı test ---
s_rf = models["RandomForest"].fit(Xtr, ytr).predict_proba(Xte)[:, 1]

rng = np.random.default_rng(0); yy = yte.values; n = len(yy)
def boot(s, B=1000):
    out = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        if yy[i].sum() == 0: continue
        out.append((average_precision_score(yy[i], s[i]), roc_auc_score(yy[i], s[i])))
    o = np.array(out); return np.percentile(o, [2.5, 97.5], axis=0)
rows = []
for name, s in [("Hotelling T² (SPC)", s_spc), ("Random Forest (ML)", s_rf)]:
    ci = boot(s)
    rows.append(dict(yontem=name, prauc=average_precision_score(yy, s), prauc_lo=ci[0, 0], prauc_hi=ci[1, 0],
                     roc=roc_auc_score(yy, s), roc_lo=ci[0, 1], roc_hi=ci[1, 1]))
res = pd.DataFrame(rows).round(3); res["baz"] = round(yy.mean(), 3)
print(res.to_string(index=False)); res.to_csv("../reports/spc_vs_ml.csv", index=False)
