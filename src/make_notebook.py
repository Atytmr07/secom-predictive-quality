import nbformat as nbf
nb = nbf.v4.new_notebook(); c = nb.cells
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
c += [md("# SECOM ile Kestirimci Kalite – Özet Notebook\nTüm hesaplar `src/` altındaki scriptlerde yapılır; bu notebook çıktıları derler."),
 code("import pandas as pd\nfrom IPython.display import Image, display\nR='../reports/'"),
 md("## 1. EDA"), code("display(Image(R+'eda.png'))"),
 md("## 2. Model karşılaştırması (5-fold CV ×3 + zaman bazlı %70/%30)\nRastgele tahmin PR-AUC ≈ 0.066."), code("pd.read_csv(R+'model_results.csv')"),
 md("## 3. Walk-forward değerlendirme (drift)\nBlok blok ileri doğru tahmin; genişleyen/kayan pencere ve özellik sayısı karşılaştırması."), code("pd.read_csv(R+'temporal_results.csv')"),
 md("## 4. Maliyet-duyarlı eşik"), code("display(Image(R+'cost_threshold.png'))"),
 md("## 4b. Güven aralıkları"), code("pd.read_csv(R+'cv_bootstrap.csv')"),
 md("## 4c. Drift (dağılım kayması)"), code("display(Image(R+'drift.png'))"),
 md("## 4d. SPC (Hotelling T²) vs ML – zaman sıralı test"), code("pd.read_csv(R+'spc_vs_ml.csv')"),
 md("## 4e. Doğrulama protokolü karşılaştırması (RQ1)"), code("pd.read_csv(R+'protocol_comparison.csv')"),
 md("## 4f. Drift ile performans bağı (RQ2)"), code("pd.read_csv(R+'drift_performance_link.csv')"),
 md("## 4g. Maliyet analizi, kronolojik (RQ4)"), code("pd.read_csv(R+'cost_chronological.csv')"),
 md("## 4h. Ek EDA"), code("display(Image(R+'eda_extra.png')); display(Image(R+'boxplots_top_sensors.png')); pd.read_csv(R+'eda_extra_summary.csv')"),
 md("## 5. SHAP"), code("display(Image(R+'shap.png'))")]
nbf.write(nb, "notebooks/01_ozet.ipynb")
