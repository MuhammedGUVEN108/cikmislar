# Cevap anahtarı güncellemesi · 22 Ekim 2026

- Sonradan kullanıcının isteğiyle ana sayfaya ve okunabilir arşive Cloudflare Web Analytics kodu eklenmiştir. İlk sürümde analiz aracı bulunmadığına ilişkin aşağıdaki kayıt tarihseldir; çözüm cevapları ve sonuçları hâlâ gönderilmez.

- Puanlama, kullanıcının isteğiyle hocaların yayımladığı kaynak cevap anahtarını esas alır: **447 puanlanan soru**, **2 iptal**, **2 anahtarı bulunmayan/okunamayan soru**.
- Editoryal bilimsel şüphe ve alternatif cevap önerileri puanlamayı durdurmaz; bu notlar arayüzden ve okunabilir arşivden kaldırılmıştır. Özgün soru verisi korunmuştur.
- JavaScript sözdizimi, cevap değerlendirmesi, filtreleme ve bellekte çalışan DOM benzetimindeki kırmızı/yeşil geri bildirim kontrolü geçti. Gerçek tarayıcı/telefon testi yapılmadı.

## İlk sürüm doğrulama kaydı · 18 Ekim 2026

Aşağıdaki kayıt ilk sürüme aittir; güncel puanlama sayıları yukarıdadır.

## Geçen kontroller

- **451 benzersiz soru**; yıl ve ders dağılımları kaynak veriyle aynı.
- Bütün soru kökleri, şık metinleri, kaynak anahtarları, yıl ve ders bilgileri özgün JSON kayıtlarıyla karşılaştırıldı.
- **433 kaynak anahtarlı soru / 18 değerlendirme dışı soru** ayrımı doğrulandı.
- **2.255 şık değerlendirmesi** ve **96 yıl/ders/inceleme filtresi birleşimi** kontrol edildi.
- Karışık sıralamada soru kaybı/tekrarı oluşmadığı ve özgün dizinin değiştirilmediği doğrulandı.
- JavaScript dosyaları Node VM ile sözdizimi kontrolünden geçti.
- Bellekte çalışan DOM benzetimiyle: ilk ekran, filtre sayıları, sıfırlama, çözüm başlatma, kırmızı/yeşil sınıfları, ilk cevabı koruma, önceki/sonraki geçişi, inceleme soruları, kaynak sayfasını yükleme, soru dizini ve arama, sonuç ekranı, yanlışları tekrar çözme ve tema geçişleri kontrol edildi.
- **138 kaynak sayfasının SHA256 değerleri** veri klasöründeki özgün PNG'lerle eşleşiyor.
- **5 kaynak PDF'nin SHA256 değerleri** veri kayıtlarındaki özgün değerlerle eşleşiyor.
- **78 şekil parçası** referansları kontrol edildi. Çıkarılan şekiller ve kaynak sayfalara ait küçük önizleme levhaları görsel olarak incelendi. Devam sayfalarındaki aynı köklü soruların görsel eşlemesi ayrıca düzeltildi/kontrol edildi.
- Bütün yerel bağlantılar ve görseller mevcut; HTML kimlikleri benzersiz.
- JavaScript gerektirmeyen arşiv **451 sorunun tamamını** içeriyor.
- CSS ayrıştırma/parantez ve anlamsal değişken başvuruları kontrol edildi.
- Uygulama kodunda kalıcı tarayıcı depolaması, çerez, telemetri, servis çalışanı veya sonuç gönderme çağrısı bulunmuyor.

## Doğrulama sınırları

- Ortamda bağlı tarayıcı bulunamadı; in-app browser açma denemesi de “Browser is not available: iab” sonucunu verdi.
- **Gerçek tarayıcı görünümü, telefon/dar ekran düzeni, dokunma, klavye odağı ve gerçek dosya/HTTP açılışı doğrulanmadı.** DOM benzetimi bunların yerine geçmez.
- Mobil CSS kuralları yazıldı; gerçek cihazda test edilmiş gibi değerlendirilmemeli.
- Site GitHub'a yüklenmedi ve canlı yayın doğrulanmadı.
- Cevapların bağımsız bilimsel doğrulaması yapılmadı. Kaynakta verilen inceleme notları korunmuştur.

Kaynak veri SHA256 (`questions.json`):

`15d043875baff96c13f65da077f531908bb14a1a8cc5b951f030f01dbec59fc9`
