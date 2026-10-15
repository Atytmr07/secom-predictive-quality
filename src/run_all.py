"""Tüm analizleri sırayla çalıştırır (sabit seed). Çıktılar ../reports içine yazılır."""
import subprocess, sys
for s in ["eda.py", "eda_extra.py", "models.py", "temporal.py", "protocols.py", "drift.py", "drift_link.py", "spc.py", "bootstrap_cv.py", "cost_shap.py"]:
    print("==>", s, flush=True)
    subprocess.run([sys.executable, s], check=True)
