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
fig, ax = plt.subplots(figsize=(7.5, 11)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(-0.3, len(steps) * 1.6)
for i, t in enumerate(steps):
    y = (len(steps) - 1 - i) * 1.6
    ax.add_patch(FancyBboxPatch((0.7, y), 8.6, 1.05, boxstyle="round,pad=0.05", fc="#e8f0fe", ec="#3b5bdb", lw=1.4))
    ax.text(5, y + 0.52, t, ha="center", va="center", fontsize=10)
    if i < len(steps) - 1:
        ax.annotate("", xy=(5, y - 0.45), xytext=(5, y), arrowprops=dict(arrowstyle="-|>", color="#3b5bdb", lw=1.6))
plt.tight_layout(); plt.savefig("../reports/flowchart.png", dpi=150)
