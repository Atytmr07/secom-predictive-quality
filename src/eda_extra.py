"""Report 3 için ek EDA: betimsel istatistik, aykırı değer, korelasyon yapısı, sınıfa göre kutu grafikleri."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, pandas as pd
from sklearn.feature_selection import mutual_info_classif
from data import load_secom

X, y, t = load_secom()
miss = X.isna().mean(); const = X.nunique() <= 1
Xv = X.loc[:, ~const & (miss <= 0.5)]
print(f"Toplam sensör {X.shape[1]} | sabit {const.sum()} | >%50 eksik {(miss>.5).sum()} | analizde kalan {Xv.shape[1]}")

# Betimsel istatistik (sensör bazında)
desc = Xv.describe().T; desc["cv"] = desc["std"] / desc["mean"].abs()
print("Eksik oran medyan %.3f | maksimum %.3f" % (Xv.isna().mean().median(), Xv.isna().mean().max()))

# Aykırı değer: robust z (MAD) > 3.5
med = Xv.median(); mad = (Xv - med).abs().median().replace(0, np.nan)
rz = 0.6745 * (Xv - med).abs() / mad
out_rate = (rz > 3.5).mean()
print("Aykırı oranı: sensör medyanı %.3f | >%%5 aykırılı sensör sayısı %d | genel hücre oranı %.3f" % (out_rate.median(), (out_rate > .05).sum(), (rz > 3.5).values.mean()))
# Aykırılık ile kusur ilişkisi: bir ürünün aykırı sensör sayısı
cnt = (rz > 3.5).sum(axis=1)
print("Ürün başına aykırı sensör sayısı: sağlam ort. %.1f | kusurlu ort. %.1f" % (cnt[y == 0].mean(), cnt[y == 1].mean()))

# Korelasyon yapısı
C = Xv.fillna(Xv.median()).corr().abs().values.copy(); np.fill_diagonal(C, 0)
pairs = int((np.triu(C) > 0.9).sum())
print("|r|>0.9 olan sensör çifti sayısı:", pairs, "| |r|>0.5:", int((np.triu(C) > .5).sum()))

# Sınıfa göre en bilgilendirici 6 sensör: kutu grafiği
mi = pd.Series(mutual_info_classif(Xv.fillna(Xv.median()), y, random_state=0), index=Xv.columns).nlargest(6)
fig, ax = plt.subplots(2, 3, figsize=(12, 6))
for a, c in zip(ax.ravel(), mi.index):
    a.boxplot([Xv[c][y == 0].dropna(), Xv[c][y == 1].dropna()], tick_labels=["sağlam", "kusurlu"], showfliers=False); a.set_title(c)
plt.suptitle("Sınıfa göre en bilgilendirici 6 sensör (MI), aykırılar gizli"); plt.tight_layout(); plt.savefig("../reports/boxplots_top_sensors.png", dpi=120)

fig, ax = plt.subplots(1, 3, figsize=(15, 4))
ax[0].hist(out_rate, bins=40); ax[0].set_title("Sensör başına aykırı oranı (robust z>3.5)")
ax[1].hist(C[np.triu_indices_from(C, 1)], bins=50); ax[1].set_title("Sensör çiftleri |korelasyon|"); ax[1].set_yscale("log")
ax[2].boxplot([cnt[y == 0], cnt[y == 1]], tick_labels=["sağlam", "kusurlu"], showfliers=False); ax[2].set_title("Ürün başına aykırı sensör sayısı")
plt.tight_layout(); plt.savefig("../reports/eda_extra.png", dpi=120)
pd.DataFrame({"sensor_outlier_rate": out_rate}).to_csv("../reports/sensor_outlier_rates.csv")
pd.DataFrame({"statistic": ["sensors_total", "constant", "gt50pct_missing", "analysed", "pairs_r_gt_0.9", "outlier_cell_rate", "mean_outlier_count_good", "mean_outlier_count_defect"],
              "value": [X.shape[1], int(const.sum()), int((miss > .5).sum()), Xv.shape[1], pairs, round((rz > 3.5).values.mean(), 4), round(cnt[y == 0].mean(), 2), round(cnt[y == 1].mean(), 2)]}).to_csv("../reports/eda_extra_summary.csv", index=False)
