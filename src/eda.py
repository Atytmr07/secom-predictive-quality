import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from data import load_secom

OUT = Path(__file__).resolve().parent.parent / "reports"
X, y, t = load_secom()
print("shape", X.shape, "| kusurlu oranı %.3f" % y.mean(), "| tarih", t.min(), "->", t.max())
miss = X.isna().mean()
print("eksik veri: sensör>%50:", (miss > .5).sum(), "| hiç eksik olmayan:", (miss == 0).sum(), "| toplam eksik %.3f" % X.isna().values.mean())
print("sabit sütun:", (X.nunique() <= 1).sum())

fig, ax = plt.subplots(1, 3, figsize=(15, 4))
y.value_counts().sort_index().plot.bar(ax=ax[0], title="Sınıf dağılımı (1=kusurlu)")
ax[1].hist(miss, bins=40); ax[1].set_title("Sensör başına eksik oranı")
roll = y.groupby(t.dt.to_period("W")).mean()
roll.plot(ax=ax[2], title="Haftalık kusur oranı")
plt.tight_layout(); plt.savefig(OUT / "eda.png", dpi=120)
