# Makine Öğrenmesi ile Kalite Tahmini – SECOM Vaka Çalışması

1. **Giriş:** Kestirimci kalite, problem tanımı, amaç.
2. **Veri:** SECOM (1567 gözlem, 590 sensör, %6,6 kusurlu, Tem–Eki 2008). Eksik veri ve sabit sütunlar. (reports/eda.png)
3. **Yöntem:** Pipeline (median imputer → varyans filtresi → ölçekleme → mutual information k=40 → model); tüm adımlar fold içinde. Dengesizlik: sınıf ağırlığı / SMOTE. Modeller: LogReg, RF, XGBoost.
4. **Değerlendirme tasarımı:** Stratified 5-fold ×3, zaman bazlı %70/%30, walk-forward. Metrik: PR-AUC, ROC-AUC, F1 (accuracy kullanılmadı).
5. **Bulgular:** Rastgele CV: RF PR-AUC 0,187 (baz 0,066). Zaman bazlı: performans rastgele düzeyine yakın -> drift / örneklem azlığı. Walk-forward: en iyi RF tüm özellik 0,067 (baz 0,042).
6. **Maliyet analizi:** C_FN/C_FP oranlarına göre eşik; oran 10'da maliyet 672 (kontrolsüz 1040, hepsini ayıkla 1463). Oranlar varsayımdır.
7. **Yorumlama:** SHAP – s477, s33, s510, s65, s130 (sensör anlamları anonim).
8. **Sınırlılıklar:** Anonim sensörler, 104 kusurlu örnek, zamansal kayma, maliyet varsayımları.
9. **Sonuç ve öneriler.**
