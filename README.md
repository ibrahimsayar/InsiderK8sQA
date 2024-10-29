# InsiderK8sQA
Insider web sitesi için AWS EKS ve EC2 aracılığı ile Kubernetes ve Selenium ile otomatik testler gerçekleştiren QA projesi.

## İçindekiler

- [Gereklilikler]()
- [Kurulum]()
- [Kullanım]()
- [Çalışma Sistemi]()
- - [Test Nasıl Yönetiliyor ve Chrome Pod'una Gönderiliyor]()
- - [Local ve Canlı Aşamaları]()
- - [Inter-Pod İletişimi]()
- [Klasör Yapısı]()
- [Karşılaşılan Problemler]()

## Gereklilikler

- **Docker (v27.2.0+)**
- **Minikube (v1.34.0+)**
- **Python (v3.12.5+)**
- **Kubectl (Client Version: v1.30.2+ || Server Version: v1.31.0)**
- **AWSCLI (aws-cli/2.18.15+)**

## Kurulum

```bash
# Repoyu klonlayın
git clone git@github.com:ibrahimsayar/InsiderK8sQA.git
# Klasöre girin
cd InsiderK8sQA
# Minikube'ü başlatın
minikube start
# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt
# Virtual environment'i etkinleştirin
```

## Kullanım

```bash
# Podlarınızı servis edin
python main.py
```

# Çalışma Sistemi
### Test Nasıl Yönetiliyor ve Chrome Pod'una Gönderiliyor
Test podu ayağa kalktığında, gelecek tetiklemeyi bekleyerek container içerisinde bulunan, unittestler ile yazılmış Python scriptini çalıştırmaya başlıyor. Test başladığında, servis katmanında oluşturduğumuz servisteki portları kullanarak selenium servisine bağlanıp gerekli testleri iletiyor; chrome node bu pod içerisinde ayağa kalkarak gerekli işlemleri yaptıktan sonra logları geri iletiyor.
### Local ve Canlı Aşamaları
#### Local
Local olarak projeyi çalıştırmak için öncelikle containerları yönetmemi sağlayan docker'a ihtiyaç duydum. Docker zaten daha önce configure etmiştim. Testimi selenium python ile yazdıktan sonra docker ile image haline getirdim bunları yaparken testleri pod'a göndererek yapamayacağım için, ilk önce başka bir containerda da bir chrome standalone da ayağa kaldırdım. Testimimin başarılını sonucu aldıktan sonra, kubernetes'i local ortamda yönetmemizi sağlayan minikube kurulumlarını yaptım. Minikube kurulumu yaptıktan sonra yine docker'da da kubernetes ile çalışacağım ayarlarını yapmam gerekiyordu. Bu aşamaları da tamamladıktan sonra context tanımlaması yaparak local ortamımı kubernetes'de çalışabileceğim bir duruma getirdim. Artık pod yaml dosyalarımı apply etmek için sistemim hazırdı.
#### Canlı
Canlı olarak projeyi çalıştırmak için EC2 ortamında bir instance'e ihtiyacım vardı. EC2 servine tarayıcı ile girdikten sonra t2.micro tipinde bir instance oluşturdum. Bu instance kurulumunu yaptıktan sonra gerekli ssh bağlantısını sağlayacağım pem dosyasını indirdim. Termius yönetim idesi ile ec2 sunucma bağlandım. Linux güncellemelerini yaptıktan sonra kubernetes'i kubectl, eksctl ve awscli araçlarını yükledim. awscli kubeconfig dosyamı güncelledikten sonra eks'de cluster oluşturup, gerekli tanımlamaları yaptım. Artık yapmam gereken tek şey bu iki poddaki işlemleri yönetecek python scriptini çalıştırmaktı. Python scripti kubernetes api araclığı iletişimde kalmamı sağlayıp testleri yönetimini yapıcaktı. Canlıda en çok sorun yaşadığım şey ise build alırken sadece bir architecture için build almam oldu localimde çalışan image ec2 içerisinde kubernetes tarafından pull edilince o arcihtecture uymadığı için çalışmıyordu. Bunu çözümünü buildx kullanarak tüm platformlar için image alarak buldum. 
### Inter-Pod İletişimi
Servisler aslında iki uçtaki iletişimi farklı yöntemlerle gerçekleştiren bir iletişim aracı olarak görebilir. İki insanın farklı dillerde konuşurken ortak olan herhangi bir dilde konuşması gibi. Pod ayağa kalkarken ona herhangi diğer bir podla nasıl iletişim kuracağını bu servis araclığı ile belirtiyoruz. Podlar worker node içerisinde bulunan kube-proxy'de oluşturduğumuz networkler sayesinde birbiri ile iletişime geçiyorlar. Bu network parametreleri'de servis tanımlamaları yaptığımız yaml dosyalarımızın içinde bulunuyor.
### Klasör Yapısı

```
InsiderK8sQA/
├── requirements.txt                                    # main.py scriptinin çalışması için gerekli olan kütüphaneler
├── test_and_chrome_node_pod_and_log_screenshot.png     # Podların ayakta olduğunu ve test çıktılarını gösteren ekran resmi
├── README.md                                           # Readme.md
├── .gitignore                                          # Repository'e göndermememiz gereken gereksiz dosyaları belirttiğimiz dosya
├── main.py                                             # Podların uygulanması, ayağa kalkması, testlerini yapıp loglarını okuduğumuz ana script
├── /chrome_node
│   └── /infrastructure
│       └── chrome-node-deployment.yaml                 # Chrome node ve service tanımlamalarını yaptığımız manifest dosyası
├── /test_node
│   └── /docker
│       ├── requirements.txt                            # Testimizi gerçekleştircek python scriptinin ihtiyacı olan gerekli kütüphaneler: Örneğin selenium
│       ├── Dockerfile                                  # Testimizi image haline getirmek için Dockerfile
│       └── test-case.py                                # Testimizi yapan python scripti
│   └── /infrastructure
│       └── test-controller-deployment.yaml             # Test işlemlerinin çalışacağı pod'un tanımlamalarını yaptığımız manifest dosyası
├── /assets
│   └── /EC2
│       ├── kubernetes-management-instance-key.pem      # EC2'ya bağlantı sağlamk için pem dosyası
├── /structure
│   └── README.md                                       # Test ve diğer yapıyı açıkladığım dosya
```
## Karşılaşılan Problemler ve Ek Bilgi
- Chrome podunu ayağa kaldırırken bir docker image görüntüsüne ihtiyacım olmadı çünkü direkt olarak public bir repository'den çalışacağım image'a ulaşabiliyordum
- Build aldığımız python scriptinin her ortamda çalışmasını çözmem neredeyse 1 günümü aldı. Buildx yöntemi ile tüm architecture'lara uyarladım.
- EKS ortamında cluster oluştururken t2.microyu kullanıyordum bu da test gerçekleştirirken, nod'un memory'sinin yetmemesine ve pod'un çökmesine neden oluyordu. Bununda çözümünü kaldıracağım node'ların tipini t2.medium seçerek buldum.
