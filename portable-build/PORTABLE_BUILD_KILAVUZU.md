# 🚀 OCR Dönüştürücü - Portatif Build Kılavuzu

Bu kılavuz, OCR Dönüştürücü uygulamasını **internet bağlantısı gerektirmeyen**, **tek dosya halinde**, **tüm işletim sistemlerinde** çalışacak şekilde nasıl derleyeceğinizi açıklar.

---

## 📋 İçindekiler

1. [Genel Bakış](#genel-bakış)
2. [Windows Build](#windows-build)
3. [macOS Build](#macos-build)
4. [Linux Build](#linux-build)
5. [Sorun Giderme](#sorun-giderme)
6. [SSS](#sss)

---

## 🎯 Genel Bakış

### Portatif Sürümün Özellikleri

| Özellik | Açıklama |
|---------|----------|
| ✅ Tek Dosya | Tüm bağımlılıklar gömülü |
| ✅ İnternet Yok | Tamamen offline çalışır |
| ✅ Kurulum Yok | Çıkart ve çalıştır |
| ✅ USB Taşınabilir | Flash bellek üzerinden çalışır |
| ✅ Tesseract Gömülü | OCR motoru dahil |
| ✅ Poppler Gömülü | PDF işleme dahil |
| ✅ Türkçe Desteği | Türkçe dil paketi dahil |

### Gereksinimler

**Build Yapmak İçin:**
- Python 3.8+
- pip (Python paket yöneticisi)
- ~2 GB boş disk alanı
- Tesseract OCR (sistem kurulumu)
- Poppler (PDF işleme için)

**Çalıştırmak İçin:**
- Hiçbir şey! Tek dosya her şeyi içerir

---

## 🪟 Windows Build

### Adım 1: Python Kurulumu

1. [Python.org](https://www.python.org/downloads/)'dan Python 3.11+ indirin
2. Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin
3. Kurulumu tamamlayın

### Adım 2: Tesseract Kurulumu

1. [UB Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) sayfasına gidin
2. En son `tesseract-ocr-w64-setup-*.exe` dosyasını indirin
3. Kurulum sırasında **"Additional language data"** bölümünde **Turkish** seçin
4. Varsayılan konuma (`C:\Program Files\Tesseract-OCR`) kurulum yapın

### Adım 3: Poppler Kurulumu (PDF desteği için)

1. [Poppler Windows](https://github.com/oschwartz10612/poppler-windows/releases) sayfasına gidin
2. En son `Release-XX.XX.X-X.zip` dosyasını indirin
3. Çıkarın ve içindeki dosyaları `portable-build\poppler-bundle\windows\` klasörüne kopyalayın
   - `bin/` klasörü dahil tüm dosyalar

**Alternatif:** Conda ile kurulum:
```batch
conda install -c conda-forge poppler
```

### Adım 4: Build İşlemi

```batch
REM Proje dizinine gidin
cd ocr-converter-clean

REM Tesseract bundle hazırlayın
python portable-build\scripts\download_tesseract.py

REM Build yapın
portable-build\scripts\build_windows.bat
```

### Adım 5: Çıktı

```
dist\OCR_Donusturucu.exe  (~150-200 MB)
```

Bu dosya tamamen bağımsızdır. USB'ye kopyalayıp herhangi bir Windows bilgisayarında çalıştırabilirsiniz.

---

## 🍎 macOS Build

### Adım 1: Homebrew Kurulumu

Terminal'de çalıştırın:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Adım 2: Python, Tesseract ve Poppler Kurulumu

```bash
# Python kur
brew install python@3.11

# Tesseract ve dil paketlerini kur
brew install tesseract tesseract-lang

# Poppler kur (PDF işleme için)
brew install poppler
```

### Adım 3: Build İşlemi

```bash
# Proje dizinine gidin
cd ocr-converter-clean

# Tesseract bundle hazırlayın
python3 portable-build/scripts/download_tesseract.py

# Build yapın
./portable-build/scripts/build_macos.sh
```

### Adım 4: Çıktı

```
dist/OCR Dönüştürücü.app     (App Bundle)
dist/OCR_Donusturucu_macOS.dmg  (DMG dosyası)
```

**.app** dosyasını Applications klasörüne sürükleyerek veya doğrudan çalıştırarak kullanabilirsiniz.

#### Apple Silicon (M1/M2/M3) Notu

Build işlemi otomatik olarak çalıştığı mimariye göre derleme yapar:
- Intel Mac → x86_64 binary
- Apple Silicon → arm64 binary

Universal binary için her iki makinede ayrı build yapıp `lipo` ile birleştirmeniz gerekir.

---

## 🐧 Linux Build

### Adım 1: Sistem Bağımlılıkları

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv \
    tesseract-ocr tesseract-ocr-tur \
    poppler-utils \
    libxcb-xinerama0 libxcb-cursor0
```

**Fedora:**
```bash
sudo dnf install -y python3 python3-pip \
    tesseract tesseract-langpack-tur \
    poppler-utils
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip \
    tesseract tesseract-data-tur \
    poppler
```

### Adım 2: Build İşlemi

```bash
# Proje dizinine gidin
cd ocr-converter-clean

# Tesseract bundle hazırlayın
python3 portable-build/scripts/download_tesseract.py

# Build yapın
./portable-build/scripts/build_linux.sh
```

### Adım 3: Çıktı

```
dist/ocr-donusturucu                    (Standalone binary)
dist/OCR_Donusturucu-x86_64.AppImage   (AppImage - önerilen)
```

**AppImage** formatı en taşınabilir seçenektir. Herhangi bir Linux dağıtımında çalışır:
```bash
chmod +x OCR_Donusturucu-x86_64.AppImage
./OCR_Donusturucu-x86_64.AppImage
```

---

## 🔧 Sorun Giderme

### Tesseract Bulunamadı

**Windows:**
- `C:\Program Files\Tesseract-OCR\tesseract.exe` dosyasının var olduğunu kontrol edin
- PATH ortam değişkenine Tesseract dizinini ekleyin

**macOS/Linux:**
- `which tesseract` komutu ile konumu kontrol edin
- Kurulu değilse yukarıdaki adımları izleyin

### Poppler Bulunamadı (PDF Hatası)

**Windows:**
- Poppler indirip `portable-build\poppler-bundle\windows\` klasörüne kopyaladığınızdan emin olun
- Veya PATH'e poppler bin klasörünü ekleyin

**macOS:**
```bash
brew install poppler
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# Fedora
sudo dnf install poppler-utils

# Arch
sudo pacman -S poppler
```

### Build Başarısız

1. **Python sürümünü kontrol edin:**
   ```bash
   python --version  # 3.8+ olmalı
   ```

2. **Virtual environment temizleyin:**
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **PyInstaller'ı güncelleyin:**
   ```bash
   pip install --upgrade pyinstaller
   ```

### Uygulama Açılmıyor

1. **Terminal/CMD'den çalıştırın** hata mesajını görmek için
2. **Antivirüs** yazılımının engellemediğinden emin olun (Windows)
3. **Gatekeeper** izni verin (macOS): `xattr -d com.apple.quarantine "OCR Dönüştürücü.app"`

### Türkçe Karakterler Bozuk

Tessdata bundle'da `tur.traineddata` dosyasının olduğunu kontrol edin:
```bash
ls portable-build/tesseract-bundle/tessdata/
# tur.traineddata görünmeli
```

### PDF Açılmıyor

- Poppler'ın doğru kurulduğundan emin olun
- Terminal'de `pdftoppm --version` çalıştırarak kontrol edin
- Hata mesajında "Poppler kurulu değil" görüyorsanız poppler kurulumunu yapın

---

## ❓ SSS

### S: Neden bu kadar büyük dosya?

**C:** Portatif sürüm şunları içerir:
- Python runtime (~50 MB)
- PyQt6 GUI framework (~100 MB)
- Tesseract OCR motoru (~20 MB)
- OpenCV görüntü işleme (~80 MB)
- Dil dosyaları (~15 MB)

Toplam: ~150-250 MB (platforma göre değişir)

### S: İnternet olmadan gerçekten çalışıyor mu?

**C:** Evet! Tüm OCR işlemleri lokalde yapılır. Sunucuya hiçbir veri gönderilmez.

### S: Başka dil ekleyebilir miyim?

**C:** Evet. `portable-build/tesseract-bundle/tessdata/` klasörüne `.traineddata` dosyalarını ekleyin ve yeniden build yapın.

### S: Daha küçük dosya boyutu mümkün mü?

**C:** Evet, bazı seçenekler:
1. `--onedir` yerine `--onefile` kullanın (zaten öyle)
2. UPX sıkıştırma aktif (spec dosyasında)
3. Kullanılmayan dilleri kaldırın
4. `tessdata_fast` kullanın (`tessdata_best` yerine)

### S: Farklı bir platforma çapraz derleme yapabilir miyim?

**C:** Hayır. Her platform için o platformda build yapmanız gerekir:
- Windows → Windows'ta build
- macOS → macOS'ta build
- Linux → Linux'ta build

### S: Ticari kullanım için lisans gerekir mi?

**C:** Proje MIT lisanslı, ticari kullanım serbesttir. Ancak:
- Tesseract: Apache 2.0 lisanslı (ticari kullanım serbest)
- Poppler: GPL lisanslı (ticari kullanım için dikkat)
- PyQt6: GPL veya ticari lisans gerektirebilir

### S: PyMuPDF neden kullanılmıyor?

**C:** PyMuPDF bazı platformlarda (özellikle macOS) derleme sorunları yaşatıyordu. pdf2image + Poppler kombinasyonu daha kararlı ve cross-platform uyumlu çalışıyor.

---

## 📁 Dosya Yapısı

```
portable-build/
├── scripts/
│   ├── build_windows.bat      # Windows build scripti
│   ├── build_macos.sh         # macOS build scripti
│   ├── build_linux.sh         # Linux build scripti
│   └── download_tesseract.py  # Tesseract hazırlayıcı
├── specs/
│   ├── windows_portable.spec  # Windows PyInstaller spec
│   ├── macos_portable.spec    # macOS PyInstaller spec
│   └── linux_portable.spec    # Linux PyInstaller spec
├── tesseract-bundle/
│   ├── windows/               # Windows Tesseract dosyaları
│   ├── macos/                 # macOS Tesseract dosyaları
│   ├── linux/                 # Linux Tesseract dosyaları
│   └── tessdata/              # Dil dosyaları (tüm platformlar)
├── poppler-bundle/
│   ├── windows/               # Windows Poppler dosyaları
│   ├── macos/                 # macOS Poppler dosyaları (opsiyonel)
│   └── linux/                 # Linux Poppler dosyaları (opsiyonel)
└── PORTABLE_BUILD_KILAVUZU.md # Bu dosya
```

---

## 🎉 Başarılı Build!

Artık tamamen portatif, internet gerektirmeyen bir OCR uygulamanız var. USB belleğe kopyalayıp istediğiniz bilgisayarda kullanabilirsiniz!

**İyi çalışmalar! 🚀**
