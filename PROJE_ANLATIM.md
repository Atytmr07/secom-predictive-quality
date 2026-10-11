# Projeyi Sade Anlatım (Arkadaşımız için)

## Proje ne yapıyor?
Bir fabrikada (yarı iletken üretimi) her ürün için 590 sensör ölçümü var ve her ürünün sonunda "kusurlu / sağlam" bilgisi var. Soru: **Ürün üretilirken sensörlere bakarak kusurlu olacağını önceden tahmin edebilir miyiz?** Kusurlu ürünü erken yakalarsak hurda ve test maliyeti düşer.

Veri: SECOM (UCI), 1567 ürün, 590 sensör, sadece 104 kusurlu (%6,6). Yani sınıflar çok dengesiz.

## Hikaye (sunumda anlatılacak sıra)
1. **Veri nasıl?** Çok sensör, çok eksik değer, az kusurlu ürün. (`src/eda.py` -> `reports/eda.png`)
2. **Modeller:** Lojistik Regresyon, Random Forest, XGBoost kurduk. Rastgele karıştırarak test edince Random Forest en iyi (PR-AUC 0,19; rastgele tahmin 0,07). (`src/models.py`)
3. **Tuzak:** Gerçek hayatta geçmişten öğrenip geleceği tahmin ederiz. Zamana göre bölünce (ilk %70 eğit, son %30 test) performans rastgele seviyesine düştü. (`src/models.py`, `src/temporal.py`)
4. **Neden?** Sensörlerin %61'inin dağılımı zamanla değişmiş (drift); modelin seçtiği sensörlerde bu oran %78. (`src/drift.py`)
5. **Klasik yöntem (SPC) daha mı iyi?** Hotelling T² kontrol kartını da denedik, o da rastgele seviyesinde. Yani sorun yöntem değil, veri zamanla değişiyor. (`src/spc.py`)
6. **Para boyutu:** Kusuru kaçırmak yanlış alarmdan 10 kat pahalıysa, modelle eşik seçmek maliyeti ~%35 düşürüyor (oranlar varsayım). (`src/cost_shap.py`)
7. **Hangi sensörler önemli?** SHAP ile baktık (s477, s33, s510...). Sensör adları anonim, bu yüzden fiziksel yorum yok.

**Ana mesaj:** Rastgele bölme ile umut verici görünen model, zaman sıralı testte çöküyor. Doğrulama tasarımı zamanı dikkate almalı.

## Sözlük
- **PR-AUC:** Dengesiz veride "kusurluları ne kadar iyi buluyorum" ölçüsü. Rastgele tahminde değeri kusur oranına (0,066) eşittir. Accuracy kullanmadık, çünkü hepsine "sağlam" desek %93 çıkar ama işe yaramaz.
- **Veri sızıntısı:** Test verisinin bilgisinin eğitime karışması. Bunu engellemek için tüm ön işleme adımları sadece eğitim kısmında öğrenilir (Pipeline).
- **SMOTE:** Az olan sınıftan yapay örnek üreten yöntem.
- **Drift:** Verinin dağılımının zamanla değişmesi.
- **Hotelling T² / SPC:** Sağlam ürünlerin "normal" davranışını öğrenip bundan sapmaları alarm sayan klasik kalite kontrol yöntemi.
- **Bootstrap güven aralığı:** Sonucun şansa bağlı oynama aralığı. Aralık rastgele seviyeyi içeriyorsa sonuç anlamlı değildir.

## Kurulum
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Veriyi https://archive.ics.uci.edu/static/public/179/secom.zip adresinden indirip `data/raw/` içine açın. Sonra `src/` içinde sırayla: `eda.py`, `models.py`, `temporal.py`, `drift.py`, `spc.py`, `cost_shap.py`.

## Görev paylaşımı önerisi
| Kişi | Görev |
|---|---|
| Sen (A) | Tüm kodu çalıştır ve anla; rapordaki Yöntem + Bulgular bölümlerini kendi cümlelerinle yaz |
| Arkadaş (B) | 1) Bu dosyayı oku ve kodu çalıştır. 2) **Giriş ve literatür:** "predictive quality", "SECOM" ve "concept drift" için 4-5 akademik kaynak bul, rapora Giriş + Kaynakça yaz. 3) **Sunum:** 8-10 slayt, yukarıdaki "hikaye" sırasıyla. |
| Birlikte | Sonuç/öneri bölümü, sunum provası, hocaya gelebilecek soruların cevapları (sözlük bölümü) |
| İsteğe bağlı (B) | Başka bir veri setinde (UCI Steel Plates Faults) `src/models.py`'yi çalıştırıp sonucu karşılaştırmak |

Git kullanımı: `git pull` -> değişiklik yap -> `git add . && git commit -m "mesaj" && git push`. Aynı dosyayı aynı anda düzenlemeyin; bu yüzden raporun bölümlerini ayrı yazın.
