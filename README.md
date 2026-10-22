# Çıkmışlar — Bir soru daha.

**451 soru · 5 yıl · 7 ders.** Kurulum veya derleme gerektirmeyen statik çalışma sitesi.

## Açılış

`index.html` dosyasını tarayıcıda açın. Yerel dosya olarak ve internetsiz çalışır. JavaScript kapalıysa `soru-arsivi.html` bütün soruları okunabilir biçimde sunar.

## Çalışma

- Yıl ve ders birlikte filtrelenebilir. Bütün yıllar/bütün dersler seçilince tüm arşiv açılır.
- Kaynak sırası veya karışık sıra seçilebilir.
- Bir şık seçildiği anda kaynak anahtarına göre doğru yeşil, yanlış kırmızı gösterilir. Yanlış seçimde doğru seçenek de yeşil yanar. İlk cevap o tur için korunur.
- Önceki/sonraki düğmeleri ve aranabilir soru dizini bulunur.
- Sonuçlar ekranından yanlışlar veya aynı set yeniden çözülebilir. Cevapsız sorular yanlış sayılmaz.
- Açık/koyu tema geçişi vardır. Tema tercihi kaydedilmez.

## Kayıt tutulmaz

Hesap, çerez, localStorage, sessionStorage, IndexedDB, analiz aracı veya sunucuya sonuç gönderimi yoktur. Seçimler ve sayaçlar yalnızca açık sayfanın belleğindedir; sayfa yenilendiğinde silinir. Görselleri ayrı sekmede açmak mevcut çözüm sekmesini sıfırlamaz. Normal tarayıcı dosya önbelleği, uygulamanın çözüm geçmişi kaydetmesi değildir.

## Cevap ve içerik sınırları

- 447 soru, **hocaların yayımladığı kaynak cevap anahtarına göre** değerlendirilir. Editoryal bilimsel şüpheler, alternatif cevap önerileri ve eksik kaynak metni, mevcut cevap anahtarının kullanılmasını engellemez.
- Kaynakta iptal edilmiş 2 soru ile cevap anahtarı bulunmayan veya okunamayan 2 soru puan dışındadır; bunlar ayrı belirtilir, cevap tahmin edilmez.
- Arayüzde yalnızca kaynakta bildirilen iptal ve düzeltme notları gösterilir. Özgün verideki editoryal notlar korunur ancak puanlamayı etkilemez ve kullanıcıya gösterilmez.
- 78 şekil/tablo parçası 45 soruyla ilişkilendirilmiştir. PDF'lerin gömülü görselleri çıkarılmış; taranmış 2021–2022 kaynağındaki ilgili görseller soruya ait alanlardan kesilmiştir. Şekiller yeniden çizilmemiştir.
- 138 tam kaynak sayfası korunmuştur. Bazı görsel bağlamlar veya eksik alanlar için bu sayfalar ayrıca açılabilir; **cevap işaretleri ve başka sorular içerebilirler**.
- 2021–2022 kaynağındaki örtülü/okunamayan alanlar tahminle tamamlanmamıştır. Kaynakta olmayan açıklamalar veya bilimsel cevap düzeltmeleri eklenmemiştir.

## GitHub Pages için

Bu klasörün **içeriğini** yayınlanacak deponun site köküne koyun; `index.html`, `css`, `js` ve `assets` aynı düzende kalmalıdır. Yalnızca HTML dosyasını yüklemek yeterli değildir. Bütün yollar göreli olduğundan proje alt yolunda yayınlanmaya uygundur. Telefonunuzdan yayın adresini açabilirsiniz. Bu teslimde GitHub'a yükleme veya yayınlama yapılmamıştır.

## Tasarım ve dosyalar

Web Dili / sunum-sitesi çekirdeği kullanıldı. Fontlar sistem yedeklerinden gelir; uzak font, CDN veya çevrimiçi çalışma bağımlılığı yoktur.

- `index.html`: çalışma uygulaması
- `soru-arsivi.html`: JavaScript gerektirmeyen tam arşiv
- `js/questions.js`: kaynağı değiştirmeden oluşturulan çalışma verisi
- `js/core.js`, `js/app.js`: soru mantığı ve arayüz
- `css/`: korunmuş tasarım çekirdeği ve uygulama stilleri
- `assets/figures/`: soruya ait şekiller
- `assets/pages/`: özgün kaynak sayfa görüntüleri
- `DOGRULAMA.md`: kontroller ve doğrulama sınırları

Kaynak PDF ve veri dosyalarına yazılmamıştır.
