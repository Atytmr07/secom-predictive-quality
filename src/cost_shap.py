import warnings; warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, pandas as pd, shap
from data import load_secom
from models import models, X, y

oof = pd.read_csv("../reports/oof_preds.csv")["RandomForest"].values
# Varsayım: kaçırılan kusurlu = C_FN, yanlış ayıklanan sağlam = 1 birim
fig, ax = plt.subplots(figsize=(7, 4)); ths = np.linspace(0, 1, 200)
for c_fn in (5, 10, 20, 50):
    cost = [((oof < th) & (y == 1)).sum() * c_fn + ((oof >= th) & (y == 0)).sum() for th in ths]
    i = int(np.argmin(cost)); base = (y == 1).sum() * c_fn  # hiç kontrol yapmama
    print(f"C_FN={c_fn:>2}: en iyi eşik={ths[i]:.2f} maliyet={cost[i]:.0f} | hepsini geçir={base:.0f} | hepsini ayıkla={(y==0).sum()}")
    ax.plot(ths, cost, label=f"C_FN={c_fn}")
ax.set_xlabel("Eşik"); ax.set_ylabel("Toplam maliyet"); ax.legend(); ax.set_title("Maliyet-eşik eğrisi (RF, OOF)")
plt.tight_layout(); plt.savefig("../reports/cost_threshold.png", dpi=120)

pipe = models["RandomForest"].fit(X, y)
Xt = pipe[:-1].transform(X); names = X.columns[pipe.named_steps["var"].get_support(indices=True)][pipe.named_steps["sel"].get_support()]
sv = shap.TreeExplainer(pipe.named_steps["m"]).shap_values(Xt)
sv = sv[..., 1] if getattr(sv, "ndim", 2) == 3 else sv[1] if isinstance(sv, list) else sv
shap.summary_plot(sv, Xt, feature_names=list(names), show=False, max_display=15)
plt.tight_layout(); plt.savefig("../reports/shap.png", dpi=120)
print("En etkili sensörler:", list(names[np.argsort(-np.abs(sv).mean(0))[:8]]))
