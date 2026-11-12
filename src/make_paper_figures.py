"""Makale için figürler (yalnızca reports/*.csv içindeki gerçek sonuçlardan)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, pandas as pd

R = "../reports/"
p = pd.read_csv(R + "protocol_comparison.csv")
order = ["Random stratified 5-fold", "Blocked 5-fold (contiguous, future in train)", "Chronological 70/30", "Walk-forward (expanding)"]
short = ["Random\nstratified CV", "Blocked CV", "Chronological\n70/30", "Walk-forward"]
models = [("LogReg (class_weight)", "Logistic Regression", "#7a8aa0"), ("RandomForest", "Random Forest", "#2f5fd0"), ("XGBoost", "XGBoost", "#d9822b")]
fig, ax = plt.subplots(figsize=(8.2, 4.4)); w = 0.26
for j, (m, lab, c) in enumerate(models):
    d = p[p.model == m].set_index("protocol").loc[order]
    x = np.arange(4) + (j - 1) * w
    ax.bar(x, d["lift"], w, color=c, label=lab, yerr=[d["lift"] - d["lift_lo"], d["lift_hi"] - d["lift"]], capsize=2.5, error_kw=dict(lw=1))
ax.axhline(1, color="k", ls="--", lw=1, label="Random guessing (lift = 1)")
ax.set_xticks(range(4)); ax.set_xticklabels(short); ax.set_ylabel("Lift (PR-AUC / defect rate)")
ax.set_title("Lift over random guessing by validation protocol (95% bootstrap CI)", fontsize=10); ax.legend(frameon=False, fontsize=8)
for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(R + "fig_protocol_lift.png", dpi=200)

d = pd.read_csv(R + "drift_performance_link.csv")
fig, ax = plt.subplots(figsize=(6.2, 3.8))
lab = ["Stable\nsensors", "Drifting\nsensors", "Random\nsensors"]
ax.bar(lab, d["prauc_mean"], yerr=d["prauc_sd"], capsize=4, color=["#7a8aa0", "#2f5fd0", "#b0b8c4"])
ax.axhline(d["base_rate"].iloc[0], color="k", ls="--", lw=1, label="Defect rate (random guessing)"); ax.legend(frameon=False, fontsize=8, loc="upper left")
ax.set_ylabel("PR-AUC on last 30% of runs"); ax.set_title("Random Forest on equal-sized sensor subsets (mean ± SD, 20 draws)", fontsize=9.5)
for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(R + "fig_drift_link.png", dpi=200)
print("ok")

# ---------- English versions of EDA, drift and cost figures ----------
from data import load_secom
from scipy.stats import ks_2samp
X, y, t = load_secom()
miss = X.isna().mean()
fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.6))
ax[0].bar(["Pass", "Fail"], [int((y == 0).sum()), int((y == 1).sum())], color=["#7a8aa0", "#2f5fd0"]); ax[0].set_title("(a) Class distribution", fontsize=10); ax[0].set_ylabel("Production runs")
ax[1].hist(miss, bins=40, color="#7a8aa0"); ax[1].set_title("(b) Missing-value share per sensor", fontsize=10); ax[1].set_xlabel("Share of missing values"); ax[1].set_ylabel("Number of sensors")
wk = y.groupby(t.dt.to_period("W")).agg(["mean", "size"]); wk = wk[wk["size"] >= 20]
ax[2].plot(wk.index.to_timestamp(), wk["mean"], marker="o", ms=3, color="#2f5fd0"); ax[2].set_title("(c) Weekly defect rate (weeks with ≥20 runs)", fontsize=10); ax[2].set_ylabel("Share of failed runs"); ax[2].tick_params(axis="x", rotation=30)
for a in ax:
    for s in ("top", "right"): a.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(R + "fig_eda.png", dpi=200)

cut = int(len(X) * .7); Xv = X.loc[:, (X.isna().mean() <= .5) & (X.nunique() > 1)]
ks = pd.Series({c: ks_2samp(Xv[c].iloc[:cut].dropna(), Xv[c].iloc[cut:].dropna()).statistic for c in Xv.columns})
worst = ks.idxmax()
fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
ax[0].hist(Xv[worst].iloc[:cut].dropna(), bins=30, alpha=.65, density=True, label="First 70% of runs", color="#2f5fd0")
ax[0].hist(Xv[worst].iloc[cut:].dropna(), bins=30, alpha=.65, density=True, label="Last 30% of runs", color="#d9822b")
ax[0].set_title(f"(a) Most shifted sensor ({worst}, KS = {ks[worst]:.2f})", fontsize=10); ax[0].legend(frameon=False, fontsize=8)
ax[1].hist(ks, bins=40, color="#7a8aa0"); ax[1].set_title("(b) KS distance between periods, all 446 sensors", fontsize=10); ax[1].set_xlabel("KS statistic"); ax[1].set_ylabel("Number of sensors")
for a in ax:
    for s in ("top", "right"): a.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(R + "fig_drift.png", dpi=200)

oof = pd.read_csv(R + "oof_preds.csv")["RandomForest"].values; yy = y.values; ths = np.linspace(0, 1, 200)
fig, ax = plt.subplots(figsize=(6.6, 3.8))
for c_fn in (5, 10, 20, 50):
    ax.plot(ths, [((oof < th) & (yy == 1)).sum() * c_fn + ((oof >= th) & (yy == 0)).sum() for th in ths], label=f"C_FN / C_FP = {c_fn}")
ax.set_xlabel("Decision threshold"); ax.set_ylabel("Total cost (false-alarm units)"); ax.set_title("Cost versus threshold, cross-validated Random Forest scores", fontsize=10); ax.legend(frameon=False, fontsize=8)
for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(R + "fig_cost_cv.png", dpi=200)
print("english figures ok", worst, round(ks[worst], 3))
