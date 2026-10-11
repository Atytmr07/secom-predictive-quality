import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import VarianceThreshold, SelectKBest, mutual_info_classif
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict, TimeSeriesSplit
from sklearn.metrics import average_precision_score, roc_auc_score, matthews_corrcoef, f1_score
from imblearn.pipeline import Pipeline as IPipeline
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from functools import partial
from data import load_secom

X, y, t = load_secom()
X = X.loc[:, X.isna().mean() <= 0.5]  # >%50 eksik sensörleri at (gözlemden bağımsız kural)
pos_w = (y == 0).sum() / (y == 1).sum()


def prep(k=40):
    return [("imp", SimpleImputer(strategy="median")), ("var", VarianceThreshold(0)),
            ("sc", StandardScaler()), ("sel", SelectKBest(partial(mutual_info_classif, random_state=0), k=k))]


models = {
    "LogReg (class_weight)": Pipeline(prep() + [("m", LogisticRegression(C=0.05, class_weight="balanced", max_iter=2000))]),
    "LogReg + SMOTE": IPipeline(prep() + [("sm", SMOTE(random_state=0)), ("m", LogisticRegression(C=0.05, max_iter=2000))]),
    "RandomForest": Pipeline(prep() + [("m", RandomForestClassifier(300, min_samples_leaf=3, class_weight="balanced_subsample", n_jobs=-1, random_state=0))]),
    "XGBoost": Pipeline(prep() + [("m", XGBClassifier(n_estimators=300, max_depth=3, learning_rate=0.05, subsample=.8, colsample_bytree=.6, scale_pos_weight=pos_w, eval_metric="aucpr", random_state=0, n_jobs=-1))]),
}


def best_f1(y, p):
    ths = np.quantile(p, np.linspace(.5, .99, 60))
    return max(f1_score(y, p >= th) for th in ths)


if __name__ == '__main__':
    # 1) Stratified 5-fold, 3 tekrar
    # 2) Zaman bazlı: ilk %70 eğitim, son %30 test
    rows, oof = [], {}
    cut = int(len(X) * .7)
    for name, pipe in models.items():
        ps = []
        for seed in range(3):
            cv = StratifiedKFold(5, shuffle=True, random_state=seed)
            ps.append(cross_val_predict(pipe, X, y, cv=cv, method="predict_proba")[:, 1])
        pr = np.mean([average_precision_score(y, p) for p in ps]); auc = np.mean([roc_auc_score(y, p) for p in ps])
        f1 = np.mean([best_f1(y, p) for p in ps]); oof[name] = np.mean(ps, axis=0)
        pipe.fit(X.iloc[:cut], y.iloc[:cut]); pt = pipe.predict_proba(X.iloc[cut:])[:, 1]
        rows.append(dict(model=name, cv_prauc=pr, cv_roc=auc, cv_bestF1=f1,
                         time_prauc=average_precision_score(y.iloc[cut:], pt), time_roc=roc_auc_score(y.iloc[cut:], pt)))
    res = pd.DataFrame(rows).round(3)
    print("Baz PR-AUC (rastgele tahmin) = %.3f | zaman testi = %.3f" % (y.mean(), y.iloc[cut:].mean()))
    print(res.to_string(index=False))
    res.to_csv("../reports/model_results.csv", index=False)
    pd.DataFrame(oof).to_csv("../reports/oof_preds.csv", index=False)
