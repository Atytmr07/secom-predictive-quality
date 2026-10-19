# Projenin Detaylı Anlatımı

Bu dosya, projede **tam olarak ne yaptığımızı, neden yaptığımızı ve sonuçların ne anlama geldiğini** sıfırdan anlatır. Sunumda veya hoca karşısında her soruya cevap verebilmek için hazırlandı. Önce kavramlar, sonra kod, sonra sonuçlar, en sonda jüri soruları var.

İçindekiler
1. Büyük resim
2. Kavramlar sıfırdan
3. Veri
4. Kurduğumuz sistem (pipeline) ve neden öyle
5. Kod dosyaları: hangisi ne yapıyor
6. Sonuçlar tablo tablo
7. Araştırma sorularının cevapları
8. Neyi iddia edebiliriz, neyi edemeyiz
9. Raporlarla ilişkisi
10. Olası jüri soruları ve cevapları
11. Kendinizi test edin

---

## 1. Büyük resim

**Problem.** Bir fabrikada ürünler üretim bandında ilerlerken sensörler ölçüm alır. Ürün bitince bir test yapılır ve ürün "geçti" veya "kaldı" olur. Testten önce, sadece sensör verilerine bakarak ürünün kalacağını tahmin edebilirsek hurda ve iş gücü maliyetinden tasarruf ederiz. Buna **kestirimci kalite (predictive quality)** denir.

**Bizim asıl sorumuz** modelin ne kadar iyi olduğu değil, **o iyiliğin gerçek mi, yoksa test yöntemimizin bir yanılsaması mı** olduğu.

Bir benzetme: Bir öğrenci geçen yılın sınav sorularını ezberleyip aynı soruları içeren bir deneme sınavında 100 alıyor. Ama gerçek sınavda yeni sorular çıkınca 40 alıyor. Deneme sınavı yanıltıcıydı. Bizim projede "deneme sınavı", veriyi **rastgele** bölüp test etmek; "gerçek sınav" ise **geçmişle öğrenip geleceği tahmin etmek**.

**Bulduğumuz şey, tek paragrafta:** Aynı model, rastgele bölünmüş test verisinde rastgeleden yaklaşık 2,7 kat iyi görünüyor; ama gerçek hayata benzeyen zaman sıralı testte rastgele tahminden ayırt edilemiyor. Bu kaybı sadece sensör kaymasına bağlayamıyoruz, klasik kalite kontrol yöntemi (SPC) de kurtarmıyor, ve maliyet açısından da model faydalı çıkmıyor.

---

## 2. Kavramlar sıfırdan

### 2.1 Sınıflandırma, eğitim ve test
- **Sınıflandırma:** Her gözleme bir kategori (burada: kusurlu / sağlam) atamak.
- **Eğitim verisi:** Modelin "öğrendiği" kısım. **Test verisi:** Modelin hiç görmediği, sonradan notlandırdığımız kısım.
- **Aşırı öğrenme (overfitting):** Model eğitim verisini ezberler, yeni veride kötü çıkar. Çok sensör (590), az kusurlu örnek (104) olduğu için bizde bu risk çok yüksek.

### 2.2 Veri sızıntısı (data leakage)
Test verisinin bilgisinin, farkında olmadan eğitime karışması. Örnek: Tüm veriyle "en iyi 40 sensörü seçtim", sonra veriyi eğitim/test diye böldüm. Seçim yaparken test verisine zaten bakmışım, bu yüzden sonuç şişer.
**Bizim önlemimiz:** Eksik değer doldurma, ölçekleme, sensör seçimi, SMOTE gibi her adım bir **pipeline** içinde ve sadece o an eğitim verisi olan kısımda öğreniliyor.

### 2.3 Sınıf dengesizliği
Kusurlu oranı %6,6. "Hepsi sağlam" diyen aptal bir model %93,4 *doğru* çıkar ama hiçbir işe yaramaz. Bu yüzden **accuracy (doğruluk) kullanmıyoruz.**
Dengesizlikle başa çıkma yolları:
- **Class weight:** Kusurlu örnekleri hatalı tahmin etmenin cezasını artırmak.
- **SMOTE:** Mevcut kusurluların arasında yapay yeni kusurlu örnekler üretmek.

### 2.4 Precision, recall, PR-AUC
- **Recall (duyarlılık):** Gerçek kusurluların kaçını yakaladım? (104 kusurludan 40'ını → %38)
- **Precision (kesinlik):** "Kusurlu" dediklerimin kaçı gerçekten kusurlu?
- Eşiği düşürürsen daha çok yakalarsın (recall ↑) ama daha çok yanlış alarm (precision ↓). Bu bir takas.
- **PR-AUC:** Tüm eşikler için precision-recall eğrisinin altındaki alan. Tek sayı. **Rastgele tahminin PR-AUC'si = kusur oranı** (yaklaşık 0,066). Bu yüzden 0,12 görünce "az" demeyiz, "rastgelenin iki katı" deriz.
- **ROC-AUC:** Kusurlu ürüne, sağlam üründen daha yüksek skor verme olasılığı. 0,5 rastgele, 1,0 mükemmel. Dengesiz veride iyimser olabildiği için yardımcı metrik.
- **Lift = PR-AUC ÷ kusur oranı:** "Rastgeleden kaç kat iyiyim?" Lift 1 = rastgele. Farklı test yöntemlerinin kusur oranı farklı olduğu için PR-AUC'leri doğrudan kıyaslayamayız, lift'i kıyaslarız.

### 2.5 Çapraz doğrulama (CV) ve türleri
Veriyi 5 parçaya böl, 4'üyle eğit 1'iyle test et, 5 kez tekrarla.
- **Rastgele (stratified) CV:** Gözlemler karıştırılarak bölünür. Test parçasındaki bir ürünün komşusu (aynı hafta, benzer koşul) eğitimdedir. Model geleceği değil "benzerini" tahmin eder. İyimser.
- **Blok CV:** Karıştırmadan ardışık 5 parça. Yine de test parçası dışında kalan *gelecek* eğitimde olabilir.
- **Kronolojik bölme:** İlk %70 eğitim, son %30 test. Gerçek hayat gibi.
- **Walk-forward:** İlk 500 gözlemle eğit, sonraki 150'yi tahmin et; sonra 650 ile eğit, sonraki 150'yi tahmin et... Üretim hattında modeli düzenli güncellemek gibi.

### 2.6 Bootstrap güven aralığı
Elimizde 104 kusurlu var; farklı bir 104'lük örnek çıksaydı sonuç ne kadar oynardı? Veriyi yeniden örnekleyerek (bootstrap) 500-1000 kez hesaplayıp %95 aralık çıkarırız. Aralık "1,0"ı (rastgele) kapsıyorsa model rastgeleden *istatistiksel olarak ayırt edilemiyor* demektir.

### 2.7 Drift (kayma)
Verinin davranışının zamanla değişmesi. Örnek: bir sensör Temmuz'da ortalama 100 iken Ekim'de 130 okuyor (makine aşındı, hammadde değişti). Model Temmuz'u öğrendiyse Ekim'de yanılır.
- **KS testi (Kolmogorov–Smirnov):** İki dönemdeki dağılımlar aynı mı? Sonuç 0–1 arası bir mesafe (KS) ve bir p-değeri. KS büyükse dağılımlar çok farklı.
- **Bonferroni düzeltmesi:** 446 sensörü aynı anda test ettiğimiz için şans eseri "anlamlı" çıkanları elemek üzere eşik 0,05 yerine 0,05/446'ya çekilir.

### 2.8 SPC ve Hotelling T²
- **SPC (Statistical Process Control):** Sağlam çalışan sürecin "normal" davranışını öğren; ondan çok sapma olursa alarm ver. Klasik kontrol kartları (X-bar) tek değişkenlidir.
- **Çok değişkenli SPC:** Yüzlerce sensör birbiriyle ilişkili olduğu için tek tek değil birlikte izlenir. **Hotelling T²** bir ürünün "normal ürünlerin merkezine uzaklığını" (ilişkileri hesaba katarak) tek sayıya çevirir. Büyükse alarm.
- **PCA:** Birbiriyle ilişkili çok sensörü, az sayıda bağımsız "bileşene" indirger. Biz verideki değişkenliğin %90'unu koruyan 123 bileşen kullandık.
- **UCL (üst kontrol sınırı):** Alarm eşiği. Biz eğitim dönemindeki sağlam ürünlerin T² değerlerinin %99'unu seçtik.

### 2.9 Modeller
- **Logistic Regression:** Basit, doğrusal. Yorumlaması kolay. Baz model.
- **Random Forest:** Yüzlerce karar ağacının oyunu. Gürültüye dayanıklı. Biz 300 ağaç kullandık.
- **XGBoost:** Ağaçları sırayla, öncekinin hatasını düzelterek kuran güçlü yöntem.
- Bilerek **basit ve standart** modeller seçtik: odak model yeniliği değil, doğrulama yöntemi.

### 2.10 Özellik seçimi: Mutual Information
Her sensörün kusur ile ilişkisini ölçer (doğrusal olmayan ilişkileri de yakalar). En yüksek 40 sensörü tutuyoruz. Bu seçim her eğitim kısmında *yeniden* yapılır (sızıntı olmasın diye).

### 2.11 SHAP
Bir modelin tahmininde hangi sensörün ne kadar katkı yaptığını gösterir. Bizim sensörler anonim olduğu için "hangisi önemli" diyebiliriz ama "neden" diyemeyiz (s477, s33, s510, s65, s130 öne çıktı).

---

## 3. Veri

| Özellik | Değer |
|---|---|
| Kaynak | UCI Machine Learning Repository, SECOM (McCann & Johnston, 2008) |
| Gözlem | 1567 üretim |
| Sensör | 590 (anonim, sayısal) |
| Dönem | 19.07.2008 – 17.10.2008 |
| Etiket | 104 kusurlu (%6,6), 1463 sağlam |
| Eksik hücre | ~%4,5 |
| >%50 eksik sensör | 28 → çıkarıldı |
| Sabit sensör | 116 → çıkarıldı |
| **Kullanılan sensör** | **446** |
| Kullanılan sensörlerde eksik oranı | medyan %0,2; en fazla %46 |
| Aykırı değer (robust z>3,5) | hücrelerin %3'ü; 74 sensörde %5'ten fazla |
| Çok korele sensör çifti (\|r\|>0,9) | 347 |
| Ürün başına ortalama aykırı sensör | kusurlu: 16,2; sağlam: 13,2 (betimsel fark) |

**Aykırıları neden silmedik?** Kusur arayan bir çalışmada uç değerler sinyalin kendisi olabilir.
**Çok korele sensör çok mu?** Evet; bu yüzden sensör seçimi ve PCA anlamlı.

**Kritik bir detay:** Kronolojik test kümesinde (son %30) yaklaşık **471 ürün ve sadece ~26 kusurlu** var. Bu yüzden zaman sıralı sonuçların güven aralıkları geniş. Bu bir zayıflık; raporda açıkça belirtilmeli.

---

## 4. Kurduğumuz sistem (pipeline)

Her model aynı hattan geçiyor:

```
Ham sensörler (446)
   → medyan ile eksik doldurma
   → sabit sütun eleme (varyans filtresi)
   → standartlaştırma (ort=0, std=1)
   → Mutual Information ile en iyi 40 sensör
   → [isteğe bağlı: SMOTE]
   → model (LogReg / Random Forest / XGBoost)
```

Modellerin ayarları (bilinçli olarak sade, ağır ayar yok):
- **Logistic Regression:** C=0,05, class_weight="balanced"
- **Random Forest:** 300 ağaç, min yaprak 3, class_weight="balanced_subsample"
- **XGBoost:** 300 ağaç, derinlik 3, öğrenme oranı 0,05, scale_pos_weight ≈ sağlam/kusurlu oranı

**Neden ağır hiperparametre ayarı yapmadık?** 104 örnekle ayar yaparsan modeli gürültüye uydurma riskin yüksek. Bu bir karar, kayıtlı (RESEARCH_LOG.md).

---

## 5. Kod dosyaları: hangisi ne yapıyor

Hepsi `src/` içinde. Çıktıları `reports/` içine yazılır.

| Dosya | Ne yapar? | Hangi soruya cevap? |
|---|---|---|
| `data.py` | Veriyi okur, **zamana göre sıralar**, etiketi 1=kusurlu yapar | Tüm analizler |
| `eda.py` | Sınıf dağılımı, eksik oranları, haftalık kusur oranı grafiği (`eda.png`) | Veriyi tanıma |
| `eda_extra.py` | Aykırı değer, korelasyon yapısı, kutu grafikleri (`eda_extra.png`, `boxplots_top_sensors.png`) | Report 3 EDA |
| `models.py` | Pipeline ve 4 model (LogReg, LogReg+SMOTE, RF, XGB). 5-fold CV ×3 tekrar + kronolojik %70/%30 | Genel model karşılaştırma |
| `temporal.py` | Walk-forward: 6 konfigürasyon (RF/LogReg, 10/20/40/tüm sensör, genişleyen/kayan pencere) | Zaman içinde işe yarar mı? |
| `protocols.py` | Aynı modeller, **4 test yöntemi**, lift ve bootstrap aralığıyla | **RQ1** |
| `drift.py` | 446 sensör için ilk %70 vs son %30 KS testi (`drift.png`) | **RQ2 (drift var mı)** |
| `drift_link.py` | Eğitim içinden drift'li/stabil sensör ayır, ayrı ayrı model kur, son %30'da test et | **RQ2 (drift açıklıyor mu)** |
| `spc.py` | PCA + Hotelling T² ile kontrol kartı; RF ile kronolojik kıyas | **RQ3** |
| `bootstrap_cv.py` | CV tahminleri için PR-AUC güven aralıkları | Model farkları gürültü mü? |
| `cost_shap.py` | Maliyet–eşik analizi (CV'de) + SHAP | **RQ4 (iyimser kısım)**, yorumlama |
| `cost_time.py` | Eşiği **sadece eğitim döneminden** seç, sonraki dönemde uygula | **RQ4 (katı kontrol)** |
| `run_all.py` | Hepsini sırayla çalıştırır | Sonuçları dondurmak |
| `make_report*.py` | Word raporlarını üretir | Raporlar |

**Sabit tohum (seed):** Tüm rastgele işlemlerde `random_state=0` (mutual information dahil). Bu yüzden sonuçlar tekrarlanabilir.

---

## 6. Sonuçlar tablo tablo

### 6.1 Genel model karşılaştırması (`model_results.csv`)
Rastgele tahminin PR-AUC'si ≈ 0,066 (CV), 0,055 (kronolojik test).

| Model | CV PR-AUC | CV ROC-AUC | Kronolojik PR-AUC | Kronolojik ROC-AUC |
|---|---|---|---|---|
| LogReg (class weight) | 0,120 | 0,661 | 0,065 | 0,568 |
| LogReg + SMOTE | 0,120 | 0,657 | 0,073 | 0,557 |
| Random Forest | **0,187** | **0,749** | 0,053 | 0,483 |
| XGBoost | 0,153 | 0,714 | 0,058 | 0,543 |

**Okuma:** CV'de Random Forest açık ara önde. Kronolojik testte hepsi çökmüş; RF'nin ROC-AUC'si 0,483 (rastgeleden bile biraz kötü). SMOTE, class weight'e göre belirgin bir kazanç sağlamadı.

### 6.2 Test yöntemi karşılaştırması: **ana bulgu** (`protocol_comparison.csv`)
Değerler **lift** (rastgeleden kaç kat iyi). Parantez içi %95 bootstrap aralığı.

| Model | Rastgele CV | Blok CV | Kronolojik 70/30 | Walk-forward |
|---|---|---|---|---|
| Logistic Regression | 1,81 (1,42–2,69) | 1,36 (1,11–1,86) | 1,18 (0,97–1,86) | 1,25 (0,97–2,12) |
| Random Forest | **2,69 (2,06–3,54)** | 1,60 (1,24–2,26) | **0,95 (0,81–1,39)** | 1,12 (0,89–1,82) |
| XGBoost | 2,09 (1,69–2,76) | 1,53 (1,27–2,12) | 1,05 (0,91–1,44) | 1,30 (1,06–1,86) |

**Okuma:**
- Her modelde sıra aynı: rastgele CV en yüksek, zaman sıralı yöntemler en düşük.
- Random Forest rastgele CV'de rastgeleden açıkça iyi (aralığın alt ucu 2,06 > 1). Kronolojik testte aralık 1'i kapsıyor, yani rastgeleden ayırt edilemiyor.
- Aralıklar geniş (özellikle kronolojik testte ~26 kusurlu var). "Kesin 0,95" demeyiz; "1 civarı, rastgeleden ayırt edilemiyor" deriz.
- Basit model (LogReg) zaman sıralı testte biraz daha az düşüyor ama onun da aralığı çoğunlukla 1'i kapsıyor.

### 6.3 Walk-forward varyasyonları (`temporal_results.csv`)
En iyi: Random Forest + tüm sensörler, PR-AUC 0,067 (baz 0,042). Özellik sayısını azaltmak (10, 40) veya kayan pencere kullanmak **düzeltmedi**, hatta bazıları rastgelenin altında kaldı. Bu **olumsuz bir sonuç**, rapora yazılacak.

### 6.4 Drift analizi (`drift.py`, `drift_top10.csv`, `drift.png`)
- 446 sensörün **270'i (%61)** ilk %70 ve son %30 arasında anlamlı farklı (Bonferroni düzeltmeli).
- Mutual Information ile seçilen 40 sensörün **31'i (%78)** kaymış → modelin güvendiği sensörler ortalamadan daha çok kaymış.
- En çok kayan sensörler: s116 (KS=0,61), s542, s543, s545, s78...

### 6.5 Drift performansı açıklıyor mu? (`drift_link.py`, `drift_performance_link.csv`)
Deney tasarımı (sızıntı yok):
1. Sadece **eğitim dönemini** (ilk %70) ikiye böl. İlk yarı vs ikinci yarı için KS testi yap.
2. Anlamlı kayanları "drift'li", p ≥ 0,05 olanları "stabil" ilan et.
3. Doğrulama: Bu ayrım gerçekten işe yarıyor mu? Evet: drift'li sensörlerin eğitim-test arası ortalama KS'si 0,213, stabil olanlarınki 0,107. Yani eğitim içinden "kayıyor" dediklerimiz test döneminde de daha çok kaydı.
4. Küçük grup 101 sensör olduğu için her gruptan **eşit sayıda (101)** rastgele sensör seçip Random Forest eğittik (20 farklı rastgele alt küme), son %30'da test ettik.

| Sensör alt kümesi | PR-AUC (ort ± sd) | ROC-AUC | Lift |
|---|---|---|---|
| Stabil | 0,068 ± 0,015 | 0,484 | 1,23 |
| Drift'li | 0,076 ± 0,015 | 0,553 | 1,38 |
| Rastgele (tüm havuz) | 0,065 ± 0,017 | 0,499 | 1,18 |
| (Rastgele tahmin) | 0,055 | 0,5 | 1,0 |

**Okuma:** Stabil sensörler drift'li sensörlerden **daha iyi değil**. Üçü de rastgele seviyesinin yakınında; farklar tekrarlar arası oynaklık (sd) içinde. Yani "kayan sensörleri atarsak model düzelir" hipotezi (H2b) **desteklenmedi.**
**Bu ne demek?** Drift gerçek ve ölçülebilir, ama performans kaybının *tek başına* açıklaması değil. Büyük olasılıkla sinyal baştan zayıf ve (muhtemelen sensörler dışında başka nedenlerle de) zamanla değişken.

### 6.6 SPC vs ML (`spc.py`, `spc_vs_ml.csv`)
- PCA: sağlam eğitim ürünleri üzerinde 123 bileşen (%90 varyans). UCL = 553,4.
- Test döneminde T² alarmı ürünlerin sadece **%3'ünde** çıktı ve alarm verilenlerin **hiçbiri kusurlu değildi**.

| Yöntem | PR-AUC (%95 aralık) | ROC-AUC (%95 aralık) |
|---|---|---|
| Hotelling T² | 0,066 (0,039–0,120) | 0,523 (0,402–0,649) |
| Random Forest | 0,053 (0,035–0,086) | 0,483 (0,379–0,583) |
| Baz (rastgele) | 0,055 | 0,5 |

**Okuma:** İkisinin de aralığı rastgele değerini kapsıyor. **Birbirinden de ayırt edilemiyorlar.** Klasik yöntem kurtarıcı değil.

### 6.7 CV'de güven aralıkları (`cv_bootstrap.csv`)
Random Forest PR-AUC 0,206 (0,157–0,283), XGBoost 0,173, LogReg ~0,135. RF'nin aralığı rastgele (0,066) çok üstünde. (Not: bu tahminler 3 CV tekrarının ortalaması olduğu için `model_results`'tan biraz yüksek.)

### 6.8 Maliyet analizi
Varsayım: Yanlış alarm (sağlam ürünü ayıklamak) = 1 birim. Kusuru kaçırmak = 5, 10, 20 veya 50 birim. **Gerçek fabrika maliyeti yok, bunlar senaryo.** İki karşılaştırma stratejisi var: **hiç kontrol etme** (tüm ürünler geçsin) ve **hepsini kontrol et** (hepsi ayıklansın).

**a) Rastgele CV'de (`cost_shap.py`, RF):**

| Kaçırma maliyeti | En iyi eşik | Model maliyeti | Hiç kontrol etme | Hepsini kontrol et |
|---|---|---|---|---|
| 5 | 0,25 | 466 | 520 | 1463 |
| 10 | 0,11 | 672 | 1040 | 1463 |
| 20 | 0,09 | 852 | 2080 | 1463 |
| 50 | 0,09 | 1212 | 5200 | 1463 |

Oran 10'da %35 tasarruf. Parlak görünüyor ama **iyimser**: hem tahminler rastgele CV'den, hem eşik tüm veriye bakılarak seçilmiş.

**b) Katı kontrol: Kronolojik (`cost_time.py`, `cost_chronological.csv`):** Eşik **sadece eğitim dönemi** tahminlerinden seçiliyor, son %30'da uygulanıyor.
Sonuç: **Hiçbir model, hiçbir maliyet oranında en iyi basit stratejiyi yenemedi.** Örnek (RF, oran 10): model 273, hiç kontrol etmeme 260. Oran 50'de model 736, hepsini kontrol etme 445. Yani model zararlı bile.

**Sonuç:** Yanıltıcı doğrulama sadece istatistik metriklerini değil, **ekonomik faydayı da şişiriyor.**

---

## 7. Araştırma sorularının cevapları

| RQ | Soru | Hipotez | Sonuç |
|---|---|---|---|
| **RQ1** | Rastgele ve zaman sıralı doğrulamada performans nasıl farklılaşıyor? | H1: zaman sıralıda daha düşük | **Destekleniyor.** Random Forest lift: 2,69 → 1,60 → 0,95 → 1,12. Diğer modellerde de aynı yön. Aralıklar geniş. |
| **RQ2** | Sensörler ne kadar kayıyor, kayma performans kaybını açıklıyor mu? | H2a: eğitimde kayan sensörler test döneminde de daha çok kayar. H2b: sadece stabil sensörlerle daha iyi tahmin | **H2a destekleniyor** (KS 0,213 vs 0,107). **H2b desteklenmiyor** (stabil 0,068, drift'li 0,076, rastgele 0,065 hepsi rastgele yakını). %61 sensör kaymış. |
| **RQ3** | Klasik SPC ile ML kıyası? | H3: ML anlamlı şekilde SPC'den iyi değil | **Destekleniyor.** İkisi de rastgele ve birbirinden ayırt edilemez. |
| **RQ4** | Maliyete göre en iyi eşik, model fayda sağlıyor mu? | H4: yüksek maliyet oranında model iki basit stratejiyi yener; kronolojikte avantaj daha küçük/yok | **CV'de evet (oran 10'da %35), kronolojikte hayır** (hiçbir oranda yenemedi). |

---

## 8. Neyi iddia edebiliriz, neyi edemeyiz

**Edebiliriz:**
- SECOM'da rastgele CV, zaman sıralı doğrulamaya göre belirgin şekilde iyimser.
- Sensörlerin çoğu bu üç ayda istatistiksel olarak kaymış.
- Kayan sensörleri çıkarmak (en azından bu tasarımda) performansı kurtarmıyor.
- Klasik T² kartı da bu veride rastgeleden ayırt edilemiyor.
- Rastgele CV'den gelen maliyet tasarrufu zaman sıralı testte ortadan kalkıyor.

**Edemeyiz:**
- "Modellerimiz iyi çalışıyor." (Çalışmıyor, zaman sıralı testte.)
- "Sorun drift'tir." (Drift var ama tek açıklama değil.)
- "Bu bulgu tüm yarı iletken fabrikaları için geçerli." (Tek veri seti.)
- "Diğer SECOM makaleleri hatalıdır." (Tam metin okumadık; sadece kendi bulgumuzu söyleyebiliriz.)
- "Şu kadar para tasarruf edilir." (Maliyetler varsayım.)

**Zayıflıklar:**
- Tek veri seti, 104 kusurlu, zaman sıralı testte yalnızca ~26 kusurlu.
- Sensörler anonim, alan bilgisiyle özellik üretemedik.
- Hiperparametre ayarı yok.
- Drift'in nedenini bilmiyoruz (aşınma mı, hammadde mi, ölçüm cihazı mı?).
- Literatür tam metinden doğrulanmadı.

---

## 9. Raporlarla ilişkisi

| Rapor | İçerik | Bu projeden nereye karşılık gelir? |
|---|---|---|
| **Report 1** (16 Ekim) | Giriş, literatür, gap, amaç, RQ'lar, plan | Bölüm 1-2, ve "neden bu analizi yapıyoruz" |
| **Report 2** (13 Kasım) | Yöntem, veri, değişkenler, değerlendirme | Bölüm 3-5 |
| **Report 3** (4 Aralık) | Analiz, sonuçlar, tartışma, RQ cevapları | Bölüm 6-8 |
| **Report 4** (25 Aralık) | Hepsinin birleşimi, makale | Hepsi |

Araştırma defteri: `RESEARCH_LOG.md`. Hangi makale okundu, hangi karar neden alındı, hangi sonuç çıktı: orada.

---

## 10. Olası jüri soruları ve cevapları

**S: Neden accuracy kullanmadınız?**
C: Veri %93 sağlam. Hepsine "sağlam" diyen model %93 doğruluk alır ama hiç kusur yakalamaz. Nadir sınıf için PR-AUC ve lift daha anlamlı.

**S: Neden rastgele CV'ye "iyimser" diyorsunuz?**
C: Rastgele bölmede test örneğinin zamansal komşuları eğitimde. Model geleceği değil benzerini tahmin ediyor. Gerçek kullanımda sadece geçmiş eldedir. Bunu rastgele, blok, kronolojik ve walk-forward ile ölçtük; lift 2,7'den ~1'e düştü.

**S: Veri sızıntısını nasıl engellediniz?**
C: Eksik doldurma, ölçekleme, özellik seçimi ve SMOTE'u pipeline içine koyduk; her katmanda sadece eğitim verisinde öğreniliyor. Ayrıca drift'li/stabil sensör ayrımını yalnızca eğitim döneminden yaptık. Eşiği de eğitim döneminden seçtik.

**S: Neden Random Forest/XGBoost, neden derin öğrenme değil?**
C: 1567 satır ve 104 pozitif örnekle derin öğrenme anlamlı olmaz. Odak model yeniliği değil doğrulama. Standart modeller literatürle kıyas için yeterli.

**S: Modeliniz çalışmıyor, projenin katkısı ne?**
C: Katkı, yaygın doğrulama pratiğinin (rastgele CV) SECOM'da sonucu ne kadar şişirdiğini göstermek ve bunu istatistik metriklerinde de, maliyet çıkarımında da ölçmek. Olumsuz sonuç da bilimsel bulgudur, özellikle endüstri uygulamasında yanlış güven maliyetlidir.

**S: Drift olduğunu nasıl bildiniz?**
C: Her sensör için iki dönemin dağılımını KS testiyle karşılaştırdık, Bonferroni ile düzelttik. 446 sensörün 270'i anlamlı kaymıştı.

**S: Peki drift neden performans düşüşünü açıklamıyor?**
C: Sadece stabil sensörlerle model kurunca da performans düzelmedi. Olası nedenler: sinyal zaten zayıf, kusur nedeni ölçülen sensörlerde değil, ilişkiler zamanla değişiyor (sadece dağılım değil, sensör-kusur ilişkisi de). Bunu bu çalışmada test edemedik; gelecek çalışma.

**S: Maliyet oranlarını nereden buldunuz?**
C: Bulmadık, varsaydık. 5, 10, 20, 50 senaryolarını bir duyarlılık analizi olarak sunuyoruz. Gerçek fabrikada gerçek maliyetle yeniden hesaplanmalı.

**S: Sadece 104 kusurlu örnekle sonuçlar güvenilir mi?**
C: Değil, bu yüzden bootstrap güven aralıkları veriyoruz. Aralıklar geniş; "kesin şu değer" yerine "rastgeleden ayırt edilebilir / edilemez" diyoruz. Zaman sıralı testte yalnızca ~26 kusurlu var, bu en büyük zayıflığımız.

**S: Başka veri setinde de aynı olur mu?**
C: Bilmiyoruz; tek veri seti kullandık. Bu bir sınırlılık ve ikinci veri seti gelecek iş.

**S: Diğer SECOM makaleleri neden %99 doğruluk bulmuş?**
C: Tam metinleri okuyup inceleyeceğiz. Olası nedenler: dengesiz veride accuracy metriği, bölmeden önce resampling (sızıntı), farklı doğrulama. Şu an sadece özetlerine dayandığımız için kesin iddia etmiyoruz.

**S: AI kullandınız mı?**
C: Evet, kod yazımında, taslak metinlerde ve literatür taramasında araç olarak kullandık. Sonuçların doğruluğu, kodun anlaşılması ve referansların doğrulanması bizim sorumluluğumuzda. Kayıtlar `RESEARCH_LOG.md`'de.

---

## 11. Kendinizi test edin
Şunları bir arkadaşınıza anlatabiliyor musunuz?
1. Neden "hepsi sağlam" diyen model %93 doğruluk alır ve neden bu kötü?
2. Lift 1,0 ne demek, 2,7 ne demek?
3. Rastgele CV neden iyimser? Bir benzetme yapabilir misiniz?
4. Veri sızıntısına bir örnek verin.
5. KS testi neyi ölçer? Bonferroni neden gerekli?
6. Hotelling T² nedir, neden SPC'nin çok değişkenli hali?
7. Neden "drift var ama tek açıklama değil" diyoruz?
8. Maliyet analizi neden CV'de iyi, kronolojikte kötü?
9. Projenin en büyük zayıflığı nedir ve nasıl dürüstçe söylersiniz?
10. Bu projeyi yayına dönüştürmek için ne eklerdiniz?

Hepsini cevaplayabiliyorsanız projeyi savunabilirsiniz. Cevaplayamadığınız soru varsa ilgili bölüme geri dönün veya bana sorun.
