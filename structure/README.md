Selenium test ve tüm yapı:

Projemizde iki tane pod ve bir tane selenium servisini ayağa kaldıracak infrastructer'lar altında manifest dosyalarımız var, bununla birlikte unittest yani insider websitesine girip adım adım görevleri tamamlayan bir unittest classımız var. bu unittes bir podda ayağa kalkıp servis aracılığı ile chrome nodeuna bağlanıp burada selenium testlerini gerçekleştiriyor. Testler unittest kütüphanesi sayesiyle ilk önce bir headless chrome tarayıcısı başlatıyor daha sonra testleri aşama aşama gerçekleştiriyor, eğer bir test sırasında fail durumu olursa assert fırlatıyor ve test hakkında log dosyasına bilgi yazıyor. Ana dizinimizde buluna python scripti ise test-case podu ayağa kalktıktan sonra bu scrip çalıştırıp scriptin log yazdığı dosyayı okuyarak bize iletişim ve bilgi sağlıyor. 