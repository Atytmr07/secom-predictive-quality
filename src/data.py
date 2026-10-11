import numpy as np
import pandas as pd
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


def load_secom():
    """X (sensörler), y (1=kusurlu, 0=sağlam), zaman damgası (sıralı)."""
    X = pd.read_csv(RAW / "secom.data", sep=r"\s+", header=None)
    X.columns = [f"s{i}" for i in range(X.shape[1])]
    lab = pd.read_csv(RAW / "secom_labels.data", sep=r"\s+", header=None,
                      names=["label", "date"], quotechar='"')
    lab["date"] = pd.to_datetime(lab["date"], format="%d/%m/%Y %H:%M:%S")
    y = (lab["label"] == 1).astype(int)  # orijinalde 1=fail, -1=pass
    order = lab["date"].argsort().values
    X, y, t = X.iloc[order].reset_index(drop=True), y.iloc[order].reset_index(drop=True), lab["date"].iloc[order].reset_index(drop=True)
    return X, y, t
