# 📄 OCR Dönüştürücü - Offline Cross-Platform OCR

**Taranmış PDF ve görselleri düzenlenebilir Word belgelerine dönüştürün**

🔐 Tamamen Offline | 🌍 Çok Dilli | 💻 Cross-Platform

---

## 🎯 2 Kullanım Yöntemi

Bu proje **2 farklı şekilde** kullanılabilir. Hangisini seçeceğiniz ihtiyacınıza bağlı:

### 🐳 Yöntem 1: Docker (Önerilen - Her Şey Dahil)

**Avantajları:**
- ✅ **Tesseract dahil** - Hiçbir şey kurmanıza gerek yok
- ✅ **Tüm bağımlılıklar dahil** - Python, kütüphaneler, her şey
- ✅ **Platform bağımsız** - Tek image her yerde çalışır
- ✅ **Tamamen offline** - İnternet bağlantısı gerektirmez

**Boyut:** ~1-2 GB (her şey dahil)

**Hızlı Başlangıç:**
```bash
cd docker-method
docker build -t ocr-converter:latest .
docker save ocr-converter:latest | gzip > ocr-converter.tar.gz

# Başka sisteme taşı, sonra:
docker load < ocr-converter.tar.gz
./run-docker.sh
```

📖 **Detaylı Bilgi:** [docker-method/README_DOCKER.md](docker-method/README_DOCKER.md)

---

### 🐍 Yöntem 2: Conda (Hafif - Bilimsel)

**Avantajları:**
- ✅ **Hafif** - Docker'dan küçük (~500 MB-1 GB)
- ✅ **Hızlı** - Native performans
- ✅ **Geliştirme dostu** - Kolayca değiştirilebilir
- ✅ **Taşınabilir** - conda-pack ile tek dosya

**Sınırlamalar:**
- ⚠️ **Tesseract ayrı kurulmalı** - Her sistemde

**Boyut:** ~500 MB-1 GB + Tesseract (~150 MB)

**Hızlı Başlangıç:**
```bash
cd conda-method
conda env create -f environment.yml
conda pack -n ocr-converter -o ocr-env.tar.gz

# Başka sisteme taşı, sonra:
tar -xzf ocr-env.tar.gz -C ~/ocr-env
source ~/ocr-env/bin/activate
conda-unpack
```

📖 **Detaylı Bilgi:** [conda-method/README_CONDA.md](conda-method/README_CONDA.md)

---

## 📊 Karşılaştırma

| Özellik | Docker 🐳 | Conda 🐍 |
|---------|-----------|----------|
| **Tesseract** | ✅ Dahil | ❌ Ayrı kur |
| **Boyut** | 1-2 GB | 500 MB-1 GB |
| **Kurulum** | Kolay | Orta |
| **Hız** | İyi | ✅ Mükemmel |
| **Platform** | ✅ Her yerde | Platform-specific |
| **İzolasyon** | ✅ Tam | İyi |
| **Geliştirme** | Zor | ✅ Kolay |

### 🎯 Hangisini Seçmeliyim?

| Durumunuz | Öneri |
|-----------|-------|
| **En basit çözüm istiyorum** | 🐳 Docker |
| **Tesseract kurmak istemiyorum** | 🐳 Docker |
| **Her platformda kullanacağım** | 🐳 Docker |
| **Daha hafif çözüm istiyorum** | 🐍 Conda |
| **Kod geliştireceğim** | 🐍 Conda |
| **Native performans istiyorum** | 🐍 Conda |

**Emin değilseniz:** 🐳 **Docker yöntemini seçin** - En kolay ve eksiksiz!

---

## ✨ Özellikler

### 📄 Dosya Desteği
- ✅ PDF (taranmış belgeler)
- ✅ PNG, JPG, JPEG
- ✅ TIFF, BMP, WebP
- ✅ Çok sayfalı PDF'ler
- ✅ Toplu işlem

### 🌍 Dil Desteği
- 🇹🇷 **Türkçe** (tam karakter desteği: ğ, ü, ş, ı, ö, ç)
- 🇬🇧 İngilizce
- 🇩🇪 Almanca
- 🇫🇷 Fransızca
- 🇪🇸 İspanyolca
- 🇮🇹 İtalyanca
- Ve 100+ dil daha...

### 📝 Çıktı Formatları
- 📄 Word (.docx) - Düzenlenebilir
- 📝 Plain Text (.txt)
- Her ikisi birden

### 🎨 Görüntü İşleme
- 📐 Otomatik yönlendirme düzeltme
- 🔍 Gürültü azaltma
- ⚡ Kontrast iyileştirme
- 🎯 Eğrilik düzeltme

### 💻 Platform Desteği
- 🪟 Windows 10/11
- 🍎 macOS 10.14+ (Intel & Apple Silicon)
- 🐧 Linux (Ubuntu, Debian, Fedora, Arch)

---

## 📂 Proje Yapısı

```
ocr-converter-clean/
├── 🐳 docker-method/          # Docker ile kullanım
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── README_DOCKER.md       # Detaylı kılavuz
│   ├── run-docker.sh
│   └── run-docker.bat
│
├── 🐍 conda-method/           # Conda ile kullanım
│   ├── environment.yml
│   ├── README_CONDA.md        # Detaylı kılavuz
│   ├── setup-conda.sh
│   └── run-conda.sh
│
├── 📂 src/                    # Kaynak kodlar
│   ├── main.py               # Ana uygulama
│   ├── ocr_processor.py      # OCR koordinatörü
│   ├── gui/                  # PyQt6 arayüz
│   └── utils/                # Yardımcı modüller
│
├── 📂 assets/                 # Varlıklar
│   ├── tessdata/             # Tesseract dil dosyaları
│   └── icons/                # Uygulama ikonları
│
├── 📂 tests/                  # Test dosyaları
│
├── 📄 requirements.txt        # Python bağımlılıkları
├── 📄 setup.py               # Kurulum scripti
├── 📄 LICENSE                # MIT Lisansı
└── 📄 README.md              # Bu dosya
```

---

## 🚀 Hemen Başlayın

### Docker Yöntemi (Önerilen)

```bash
# 1. Docker klasörüne git
cd docker-method

# 2. README'yi oku
cat README_DOCKER.md

# 3. Image oluştur
docker build -t ocr-converter:latest .

# 4. Çalıştır
./run-docker.sh
```

### Conda Yöntemi

```bash
# 1. Conda klasörüne git
cd conda-method

# 2. README'yi oku
cat README_CONDA.md

# 3. Environment oluştur
./setup-conda.sh

# 4. Çalıştır
./run-conda.sh
```

---

## 📖 Dokümantasyon

| Dosya | Açıklama |
|-------|----------|
| `README.md` | Bu dosya - Genel bakış |
| `docker-method/README_DOCKER.md` | Docker kullanım kılavuzu |
| `conda-method/README_CONDA.md` | Conda kullanım kılavuzu |
| `QUICKSTART.md` | Hızlı başlangıç (eski - referans için) |
| `INSTALL.md` | Detaylı kurulum (eski - referans için) |

---

## 💡 SSS

### Docker vs Conda?

**Docker seçin:**
- En basit çözüm istiyorsanız
- Tesseract kurmak istemiyorsanız
- Tek dosya ile her yere taşımak istiyorsanız

**Conda seçin:**
- Daha küçük boyut istiyorsanız
- Kod üzerinde çalışacaksanız
- Native performans istiyorsanız

### Tesseract neden ayrı?

Conda yönteminde Tesseract sistem düzeyinde kütüphane olduğu için Python environment'ına dahil edilemez. Docker'da ise sistem image'ına dahil edilir.

### İnternet gerektiriyor mu?

**Hazırlık aşaması:** Evet (image/environment oluştururken)
**Kullanım aşaması:** Hayır (tamamen offline)

### Boyut çok büyük değil mi?

Docker: ~1-2 GB ama **her şey dahil** (Tesseract, Python, tüm kütüphaneler)
Conda: ~500 MB-1 GB + ayrı Tesseract kurulumu

### Hangi platformda çalışır?

Her ikisi de Windows, macOS ve Linux'ta çalışır.
Docker: Tek image her yerde
Conda: Platform-specific environment

---

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun
3. Commit edin
4. Pull Request gönderin

---

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [OpenCV](https://opencv.org/)
- [python-docx](https://python-docx.readthedocs.io/)

---

## 📧 İletişim

- **GitHub Issues:** Hata bildirimi
- **GitHub Discussions:** Sorular ve tartışmalar

---

**⭐ Beğendiyseniz yıldız vermeyi unutmayın!**

**🚀 Mutlu OCR'lar!**
