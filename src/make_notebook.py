import nbformat as nbf
nb = nbf.v4.new_notebook(); c = nb.cells
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
c += [md("# SECOM ile Kestirimci Kalite – Özet Notebook\nTüm hesaplar `src/` altındaki scriptlerde yapılır; bu notebook çıktıları derler."),
 code("import pandas as pd\nfrom IPython.display import Image, display\nR='../reports/'"),
 md("## 1. EDA"), code("display(Image(R+'eda.png'))"),
 md("## 2. Model karşılaştırması (5-fold CV ×3 + zaman bazlı %70/%30)\nRastgele tahmin PR-AUC ≈ 0.066."), code("pd.read_csv(R+'model_results.csv')"),
 md("## 3. Walk-forward değerlendirme (drift)\nBlok blok ileri doğru tahmin; genişleyen/kayan pencere ve özellik sayısı karşılaştırması."), code("pd.read_csv(R+'temporal_results.csv')"),
 md("## 4. Maliyet-duyarlı eşik"), code("display(Image(R+'cost_threshold.png'))"),
 md("## 5. SHAP"), code("display(Image(R+'shap.png'))")]
nbf.write(nb, "notebooks/01_ozet.ipynb")
