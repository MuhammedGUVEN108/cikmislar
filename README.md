# Çıkmışlar — Bir soru daha.

**541 soru · 6 yıl · 7 ders.** Kurulum veya derleme gerektirmeyen statik çalışma sitesi.

## 2026-2027 çıkmışları

- 90 gerçek sınav sorusu eklendi; arşiv 541 soru ve 6 akademik yıl oldu. Gerçek Dışı Mod'un 180 sorusu ayrıdır.
- Yeni kayıtlar `js/questions-2026-2027.js` içinde; önceki 451 kayıt değiştirilmedi. `author`, `sourceRef` ve `booklet` kaynak bilgilerini korur; soru sahibi çözüm ekranında görünür.
- 26 kaynak görseli, görselli A-E seçenekleri ve 90 kaynak cevabı korundu. `verifiedKeys: null`, cevapların tamamının bağımsız bilimsel doğrulamasının yapılmadığı anlamına gelir.
- Kaynak 8. sorunun Na yükü Na⁺ olarak düzeltildi; kaynak metni `originalStem` alanında, açıklama ve akademik bağlantı kayıtta korunur. 42. sorunun ayrık indisleri özgün sayfanın metin sırasıyla yeniden birleştirildi. Yanlış seçeneklerin içeriği değiştirilmedi.
- Yeni yılın tam sayfa görselleri özgün kişisel sonuç dökümünden değil, düzeltilmiş soru kitapçığından üretilmiştir; öğrenci adı/puanı/işaretlemeleri içermez.

## v1.2

- Üstteki **Gerçek Dışı Mod** düğmesi, bu yılın ders slaytlarından üretilmiş **iki denemede toplam 180 teorik soruyu** aynı soru motorunda açar. Bunlar çıkmış veya gerçek sınav sorusu değildir; pratik soru içermez ve öğretim üyesi incelemesinden geçmemiştir.
- Her denemenin dağılımı: 27 Tıbbi Biyoloji, 24 Organik Kimya, 13 Tıp Tarihi ve Etik, 13 Histoloji ve Embriyoloji, 7 Halk Sağlığı, 6 Tıbbi Biyokimya.
- Deneme seti filtresinden **Deneme 01**, **Deneme 02** veya **Bütün denemeler** seçilebilir. Yeni açılan Gerçek Dışı Mod'da en yeni deneme seçili gelir. Set ve ders birlikte filtrelenir; soru dizini ve kaynak penceresi gerçek deneme adını gösterir.
- Her iki modda da ilk şık seçimi kilitlenir; doğru/yanlış hemen görünür. Deneme modunda açıklama da otomatik açılır. Ders filtresi, karışık sıra, soru dizini, tema ve yanlışları yeniden çözme ortak arayüzü kullanır.
- Çıkmış ve deneme cevapları açık sekmede ayrı tutulur. Mod değiştirirken çalışma korunur; sayfa yenilenince her ikisi de silinir. Deneme anahtarı, özgün kaynak anahtarından ayrı `authoredKey` alanındadır; eski 451 kayıt değiştirilmemiştir.
- Deneme sorularının kaynak penceresinde slayt dosyası, sayfa / slayt numarası ve ilgili metin yer alır. Eski ikili PPT kaynağında konum, slayt numarası olmadığı belirtilen metin kaydıdır. Yerel dosya yolları veya erişilemeyen masaüstü bağlantıları yayımlanmaz.
- Doğrudan mod bağlantısı: `?mod=gercek-disi`.
- Gerçek Dışı Mod yalnızca **koyu mor temada** çalışır; tema düğmesi bu modda görünmez. Çıkmışlara dönüldüğünde önceki açık/koyu tercih geri gelir.
- Bu moddaki **180 sorunun her birinde** kısa AI açıklaması üstte korunur. Altındaki kapalı **Şıkları tek tek incele** ve **Terimleri açıkla** bölümleri istenirse açılır: toplam **900 şık açıklaması**, **458 farklı terim tanımı** vardır. Bunlar sabit metindir; tarayıcıdan AI servisine istek gönderilmez.
- Deneme 02'nin slayt referansları 40 dosyaya uzanır. N-bağlı glikozilasyon slaydındaki Asp/Asn karışıklığı açıkça belirtilip asparajin esas alınmıştır; perinatal hesapta gebelik sınırı soruda tanımlanmıştır. İlgili iki sorunun kaynak penceresinde NCBI ve WHO ek kontrol bağlantıları bulunur.
- **Not hesabı:** finalsiz geçişte ham yıl içi ortalama **79,5**, final dahil ağırlıklı toplamda **59,5** baraj kabul edilir; bu değerler sırasıyla 80 ve 60'a yuvarlanır. Ara notlar ayrıca yuvarlanmaz. Gereken final ve kalan not hedefleri bu barajlara göre hesaplanır. Örnek: yıl içi ortalama 50 ise gereken final 73,75'tir; toplam 59,50 olur.

## v1.1

Bu bölüm önceki sürümün notlarıdır; güncel geçiş barajları v1.2'de açıklanmıştır.

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
- `js/generated-questions.js`: Gerçek Dışı Mod'un 90 sorusu ve slayt referansları
- `js/generated-explanations.js`: bu 90 sorunun A–E gerekçeleri ve ortak terim sözlüğü
- `js/generated-exam-02.js`: Deneme 02'nin 90 sorusu, 450 şık gerekçesi ve sözlüğe eklenen 109 tanım
- `js/generated-manifest.json`: denemenin kapsamı ve ders dağılımı
- `js/core.js`, `js/app.js`: soru mantığı ve arayüz
- `css/`: korunmuş tasarım çekirdeği ve uygulama stilleri
- `assets/figures/`: soruya ait şekiller
- `assets/pages/`: özgün kaynak sayfa görüntüleri
- `DOGRULAMA.md`: kontroller ve doğrulama sınırları

Kaynak PDF ve veri dosyalarına yazılmamıştır.
