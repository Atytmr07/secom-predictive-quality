# Research Notebook (Araştırma Defteri)

Dersin kural 6'sı gereği tutulan kayıt. Her çalışma oturumunda buraya tarih ve not ekleyin.

## 1. Okunan makaleler ve doğrulama durumu
Durum: **Özet** = sadece özet/yayıncı sayfası görüldü (AI ile tarandı). **Tam metin** = bir öğrenci PDF'i okudu. Rapor teslim edilmeden önce tüm satırların "Tam metin" olması hedeflenir.

| Makale | Durum | Tam metinde teyit edilecek | Okuyan / Tarih |
|---|---|---|---|
| Tercan & Meisen (2022), J. Intell. Manuf. 33(7) | Özet | Kapsam, "overall view eksik" ifadesi | |
| Kang, Catal & Tekinerdogan (2020), Comput. Ind. Eng. | Özet | 271 -> 39 sayıları, cilt/sayfa | |
| Kerdprasop & Kerdprasop (2011), IMECS | Özet | Doğrulama yöntemi, sonuç sayıları | |
| Salem, Taheri & Yuan (2018), BDCC 2(4):30 | Özet | Doğrulama zaman bazlı mı? | |
| Nuhu et al. (2023), J. Supercomput. | Özet | **%99,5–100 doğruluk nasıl elde edilmiş? SMOTE bölmeden önce mi?** | |
| Park et al. (2024), Sensors 24(17):5461 | Özet | Hangi model/ön işleme en iyi, doğrulama nasıl | |
| Zheng et al. (2025), APEM 20(4) | Özet | **AUPRC 0,97 hangi sınıf pozitif? Zaman bazlı test var mı?** | |
| Kourti & MacGregor (1995), Chemom. Intell. Lab. Syst. 28 | Özet | T² ve PCA anlatımı | |
| He & Wang (2007), IEEE TSM 20(4) | Sadece künye/arama özeti | Yöntem ve veri, yazar adları | |
| Gama et al. (2014), ACM Comput. Surv. 46(4) | Özet | Drift türleri tanımı | |
| Jourdan et al. (2021), arXiv | Özet (arXiv sayfası) | Hakem denetimli yayına dönüşmüş mü? | |
| Hinder, Vaquet & Hammer (2024), Front. AI | Özet | Cilt/sayfa bilgisi | |

**Önemli:** Research Gap 1 ("SECOM çalışmaları zaman bazlı doğrulama yapmıyor") şu an sadece özetlere dayanıyor. Tam metinde biri yapıyorsa gap ifadesi yumuşatılmalı.

## 2. Veri kaynağı
- UCI SECOM: https://archive.ics.uci.edu/dataset/179/secom (McCann & Johnston, 2008). Dosyalar: `secom.data`, `secom_labels.data`, `secom.names`. İndirme tarihi: 2026-10-05.
- 1567 gözlem, 590 sensör, 104 kusurlu (%6,6), 19.07.2008 – 17.10.2008.
- Etiket kodu orijinalde 1 = fail, -1 = pass; kodda kusurlu = 1 olarak çevrildi.

## 3. Denenen yöntemler ve sonuçlar (gerçek çıktılar, `reports/*.csv`)
- Rastgele 5-fold CV x3: Random Forest PR-AUC 0,187; XGBoost 0,153; LogReg ~0,12 (rastgele tahmin 0,066).
- Zaman bazlı %70/%30: tüm modeller rastgele düzeyine yakın (PR-AUC 0,05–0,07; baz 0,055).
- Walk-forward (6 konfigürasyon): en iyi RF, tüm özellikler, PR-AUC 0,067 (baz 0,042). Özellik sayısı azaltmak ve kayan pencere **işe yaramadı** (olumsuz sonuç, rapora yazılacak).
- SMOTE, class_weight'e göre belirgin bir kazanç sağlamadı.
- Drift (KS testi, Bonferroni): 446 sensörün 270'i (%61) kaymış; seçilen 40 sensörün 31'i (%78).
- SPC (PCA tabanlı Hotelling T², UCL %99): zaman testinde PR-AUC 0,066, ML 0,053; ikisinin de %95 bootstrap aralığı baz oranı (0,055) kapsıyor.
- Maliyet analizi: C_FN/C_FP oranları **varsayımdır**, gerçek fabrika verisi değil.

## 4. Kararlar ve metodoloji değişiklikleri
- %50'den fazla eksik sensörler çıkarıldı (hedef etiketine bakmadan verilen kural).
- Tüm ön işleme/seçim/SMOTE adımları Pipeline içinde, yalnızca eğitim katmanında öğreniliyor (sızıntı önleme).
- Mutual information seçimine `random_state=0` verildi; öncesinde sonuçlar her çalıştırmada biraz değişiyordu.
- Hiperparametre ayarı bilinçli olarak yapılmadı (104 pozitif örnekle gürültüye uyum riski). Nested CV Report 2/3'te değerlendirilebilir.
- Zaman bazlı değerlendirme eklendi, çünkü rastgele CV'nin iyimser olabileceği düşünüldü (drift literatürü).

## 5. Karşılaşılan sorunlar
- `models.py` import edilince tüm modelleri yeniden çalıştırıyordu -> `if __name__ == '__main__'` eklendi.
- `oof_preds.csv` 3 CV tekrarının ortalaması; bu yüzden `cv_bootstrap.csv` değerleri (RF 0,206) `model_results.csv`'den (0,187) biraz yüksek. Raporda not düşüldü.
- Bazı makale sayfaları (PMC, Springer, MDPI) otomatik erişimi engelledi; bunlar elle okunmalı.

## 6. Yapay zekâ kullanımı (kural 4 gereği şeffaf kayıt)
- Claude Code (AI asistan): kod iskeleti ve analiz scriptleri, rapor taslakları, literatür aramasında makale bulma ve özet çıkarma.
- **Öğrencilerin sorumluluğu:** kodun anlaşılması ve çalıştırılması, referansların tam metinden doğrulanması, raporun kendi cümleleriyle yeniden yazılması, sonuçların savunulması.
- Hocaya sorulacak: AI kullanımının raporda nasıl belirtilmesi isteniyor (örn. "Acknowledgements" bölümünde bir cümle).

## 7. Yapılacaklar
- [ ] Tablodaki 12 makalenin tam metin okunması (yukarıdaki tablo)
- [ ] Künyelerin tamamlanması (cilt/sayfa/DOI)
- [ ] Report 1'in kendi cümlelerimizle gözden geçirilmesi
- [ ] Report 2: yöntem tasarımı (nested CV, drift eşikleri, maliyet oranı gerekçesi)
- [ ] İsteğe bağlı: ikinci veri seti ile doğrulama
