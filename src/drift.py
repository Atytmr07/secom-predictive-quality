"""Drift: sensör dağılımları ilk %70 ile son %30 arasında değişti mi? (KS testi)"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, pandas as pd
from scipy.stats import ks_2samp
from sklearn.feature_selection import mutual_info_classif
from data import load_secom

X, y, t = load_secom()
X = X.loc[:, X.isna().mean() <= 0.5]
X = X.loc[:, X.nunique() > 1]
cut = int(len(X) * .7)
a, b = X.iloc[:cut], X.iloc[cut:]
res = pd.DataFrame({c: ks_2samp(a[c].dropna(), b[c].dropna()) for c in X.columns}, index=["ks", "p"]).T
res["drift"] = res["p"] < 0.05 / len(res)  # Bonferroni
print(f"{len(res)} sensörden {res.drift.sum()} tanesinde anlamlı kayma (%{100*res.drift.mean():.0f})")

# Modelin seçtiği sensörler (yalnızca eğitim döneminden) kaymış mı?
mi = pd.Series(mutual_info_classif(a.fillna(a.median()), y.iloc[:cut], random_state=0), index=X.columns)
top = mi.nlargest(40).index
print(f"Seçilen 40 sensörün {res.loc[top,'drift'].sum()} tanesi kaymış (%{100*res.loc[top,'drift'].mean():.0f}); tümünde %{100*res.drift.mean():.0f}")
res.sort_values("ks", ascending=False).head(10).round(3).to_csv("../reports/drift_top10.csv")
print(res.sort_values("ks", ascending=False).head(5).round(3))

worst = res["ks"].idxmax()
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].hist(a[worst].dropna(), bins=30, alpha=.6, density=True, label="ilk %70"); ax[0].hist(b[worst].dropna(), bins=30, alpha=.6, density=True, label="son %30")
ax[0].set_title(f"En çok kayan sensör: {worst}"); ax[0].legend()
X[worst].groupby(t.dt.to_period("W")).mean().plot(ax=ax[1], title=f"{worst} haftalık ortalama")
plt.tight_layout(); plt.savefig("../reports/drift.png", dpi=120)
