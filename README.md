# Çıkmışlar — Bir soru daha.

**451 soru · 5 yıl · 7 ders.** Kurulum veya derleme gerektirmeyen statik çalışma sitesi.

## v1.1

- Her sorunun altında başlangıçta kapalı bir **AI desteği** kutusu vardır. 419 kısa açıklama, soru verisindeki `aiExplanation` alanında sabit düz metindir; 32 iptal/eksik/belirsiz kayıtta açıklama boştur. Metinler sayfa açılırken üretilmez ve AI servisine istek gönderilmez.
- Kutular, küçük puntolu “Bu metin AI'dır, doğruluğu şüphelidir kontrol ediniz.” uyarısını taşır. Soru metinleri ve hoca cevap anahtarları korunmuştur.
- **Not Hesaplama** menüsü yıl içi ortalamayı, kalan not hedefini ve gereken final notunu hesaplar. Kurulların yıl sonuna katkıları sırasıyla %11, %9, %11, %11, %12; Bilimsellik ve İHU'nun her biri %3; final %40'tır. Yıl içi ortalama, bu %60'lık katkının 0,60'a bölünmesiyle bulunur. Finalsiz hedef 80, final dahil hedef 60'tır. Ek bir final alt sınırı veya okul yuvarlama kuralı varsayılmaz.
- Notlarda boş ile sıfır ayrılır; 0–100 dışındaki girdiler reddedilir. Tamamlanmamış notlardan kesin final sonucu çıkarılmaz. Notlar tarayıcı belleğinde tutulur, kaydedilmez.
- Açılışta v1.1 güncelleme penceresi gösterilir. Pencere görüntülendi bilgisi çerez veya kalıcı depoya yazılmaz; sayfa yeniden açılırsa yeniden gösterilir.

## Açılış

`index.html` dosyasını tarayıcıda açın. Yerel dosya olarak ve internetsiz çalışır. JavaScript kapalıysa `soru-arsivi.html` bütün soruları okunabilir biçimde sunar.

## Çalışma

- Yıl ve ders birlikte filtrelenebilir. Bütün yıllar/bütün dersler seçilince tüm arşiv açılır.
- Kaynak sırası veya karışık sıra seçilebilir.
- Bir şık seçildiği anda kaynak anahtarına göre doğru yeşil, yanlış kırmızı gösterilir. Yanlış seçimde doğru seçenek de yeşil yanar. İlk cevap o tur için korunur.
- Önceki/sonraki düğmeleri ve aranabilir soru dizini bulunur.
- Sonuçlar ekranından yanlışlar veya aynı set yeniden çözülebilir. Cevapsız sorular yanlış sayılmaz.
- Açık/koyu tema geçişi vardır. Tema tercihi kaydedilmez.

## Çözüm kaydı ve ziyaret istatistikleri

Hesap, çerez, localStorage, sessionStorage, IndexedDB veya sunucuya çözüm sonucu gönderimi yoktur. Seçimler ve sayaçlar yalnızca açık sayfanın belleğindedir; sayfa yenilendiğinde silinir. Görselleri ayrı sekmede açmak mevcut çözüm sekmesini sıfırlamaz. Normal tarayıcı dosya önbelleği, uygulamanın çözüm geçmişi kaydetmesi değildir.

Kullanıcının isteğiyle ana sayfaya ve okunabilir arşive Cloudflare Web Analytics eklenmiştir. Genel ziyaret ve performans istatistikleri Cloudflare panelinden izlenir; soru seçimleri, verilen cevaplar ve doğru/yanlış sonuçları analize gönderilmez. Analiz internet bağlantısı gerektirir; soru çözümü çevrimdışı çalışmayı sürdürür.

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
