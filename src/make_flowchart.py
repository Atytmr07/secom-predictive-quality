import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

steps = [
    "Problem definition\n(defect prediction under process change)",
    "Literature review & research gaps\n(Report 1)",
    "Data: UCI SECOM\n1,567 runs, 590 sensors, timestamps",
    "Preprocessing (inside training folds only)\nmissing-value imputation, constant/sparse sensor removal,\nscaling, mutual-information feature selection",
    "Models: Logistic Regression, Random Forest, XGBoost\n+ SPC baseline (PCA-based Hotelling T²)",
    "Validation protocols\nrandom CV · blocked CV · chronological split · walk-forward",
    "Drift analysis (KS test)\nstable vs drifting sensor subsets",
    "Evaluation: PR-AUC, lift, ROC-AUC, bootstrap CIs\n+ cost-based threshold analysis",
    "Results → answers to RQ1–RQ4",
    "Discussion, limitations, conclusion",
]
fig, ax = plt.subplots(figsize=(8.4, 8.2)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(-0.3, len(steps) * 1.25)
for i, t in enumerate(steps):
    y = (len(steps) - 1 - i) * 1.25
    ax.add_patch(FancyBboxPatch((0.4, y), 9.2, 0.92, boxstyle="round,pad=0.05", fc="white", ec="black", lw=1.2))
    ax.text(5, y + 0.46, t, ha="center", va="center", fontsize=10.5)
    if i < len(steps) - 1:
        ax.annotate("", xy=(5, y - 0.3), xytext=(5, y), arrowprops=dict(arrowstyle="-|>", color="black", lw=1.3))
plt.tight_layout(); plt.savefig("../reports/flowchart.png", dpi=150)
