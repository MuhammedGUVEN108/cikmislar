# 2. Kurul AI desteği

3 Kasım 2026: 469 kaydın 344’üne çözüm özeti, beş ayrı şık gerekçesi ve terim açıklamaları eklendi. Eksik veya tartışmalı görülen 125 kayda AI eklenmedi. Gerekçeler [kontrol listesinde](AI_KURUL2_KONTROL.md). Liste editoryal değerlendirmedir; kaynak kurumun resmî düzeltmesi değildir.

Veri `js/data/archive/ai-support-kurul2.js` içinde `ARCHIVE_EXPLANATIONS`, `ARCHIVE_GLOSSARY` ve `ARCHIVE_AI_MANIFEST` olarak bulunur. Kaynak soru nesneleri, şıklar ve `sourceKeys` değiştirilmez. `verifiedKeys` doldurulmaz. Açıklamalar bağımsız akademik inceleme yerine geçmez; mevcut AI uyarısı korunur.

AI paneli yalnız ilk cevap verildikten sonra açılır. Destek eklenmeyen sorularda panel görünmez. Yanlış ilk seçimden sonra da çözüm okunabilir; ilk cevap kilidi ve kaynak anahtarına göre puanlama değişmez. Gerçek Dışı Mod kendi açıklama ve sözlüğünü kullanmaya devam eder. Veri statik dosyadır; çözüm sırasında model/API çağrısı veya yeni kullanım ücreti yoktur. İnternetsiz dosya açılışı korunur.

## Güncelleme ve kontrol

`py -3 -X utf8 tools/ai-kurul2/author.py` açıkça yazılmış açıklamalardan JS dosyasını ve dışlama listesini yeniden üretir. Dış servis/model çağırmaz. Yıl dosyaları metinleri, `exclusions.py` kapsam kararlarını içerir. Tekrar kullanılan şıklarda açık permütasyon ve anahtar eşleşme kontrolü vardır. Şık harfi veya anahtar uyuşmazlığında üretim durur; yeni kaynak sorular değerlendirilmeden sessizce eklenmez.

Node PATH’te değilse README’deki tam yolu kullan:

```text
node tools/check.cjs
node tools/check-kurul2.cjs
node tools/check-ai-kurul2.cjs
node tools/check-kurul2-ui.cjs
```

Son araç Node ile DOM simülasyonudur; gerçek tarayıcı veya mobil görsel testi değildir. 469 sorunun cevap öncesi/sonrası panelini, dışlama kapsamını, şık gerekçelerini ve sözlüklerini denetler. Veri kontrolü, açıklama dosyasının kaynak/deneme verilerini değiştirmediğini ve kaynak soruların HEAD ile aynı kaldığını kontrol eder; Git satır sonu farkı içerik değişikliği sayılmaz.

## İncelemede başvurulan kaynaklar

Bu kaynaklar belirli mekanizma ve belirsizlik kararlarına yardımcı oldu; 344 açıklamanın tümü için bağımsız bilimsel doğrulama yapıldığı anlamına gelmez.

- [NHGRI — Gen](https://www.genome.gov/genetics-glossary/Gene)
- [NICHD — Nükleozom çekirdeği ve kromatin](https://annualreport.nichd.nih.gov/clark.html)
- [NCBI — Besinlerden enerji elde edilmesi](https://www.ncbi.nlm.nih.gov/books/NBK26882/)
- [NIST — t testi](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/t_test.htm)
- [NIST — Normal dağılım](https://itl.nist.gov/div898/handbook/pmc/section5/pmc51.htm)
- [NIH ODS — B12](https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/)
- [NIH ODS — Vitamin ve mineral bilgi sayfaları](https://ods.od.nih.gov/FactSheets/List-VitaminsMinerals/)
- [Imperial College — Karboksilik asit türevlerinin indirgenmesi](https://www.ch.ic.ac.uk/local/organic/tutorial/DB_Carbonylnotes1.pdf)
- [University of Alberta — Alken hidratasyonu](https://www.chem.ualberta.ca/~chem263b2/pdf/notes03.pdf)
- [OpenStax — Erken çocukluk bilişsel gelişimi](https://openstax.org/books/lifespan-development/pages/5-3-cognition-in-early-childhood)

## Teslim sınırı

Otomatik veri ve davranış kontrolleri bilimsel doğruluk garantisi değildir. Bu çalışmada tarayıcı bağlantı sunucusu erişilemedi; Windows aracı mevcut URL’yi güvenilir belirleyemediği için bilgisayar kullanımı durdu. Güvenlik engeli aşılmadı. Gerçek tarayıcıda 320/390/1440 piksel görsel kontrolü tamamlanmış sayılmaz. GitHub gönderimi, Workers dağıtımı ve canlı dosya eşleşmesi ayrıca doğrulanır.
