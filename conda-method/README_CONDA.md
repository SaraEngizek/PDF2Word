# 🐍 Conda Yöntemi - Taşınabilir Python Environment

## ✅ Avantajları
- ✅ **Hafif** - Docker'dan daha küçük (~500 MB - 1 GB)
- ✅ **Hızlı** - Native performans (container overhead yok)
- ✅ **Bilimsel** - Conda ekosistemi, numpy/scipy optimize edilmiş
- ✅ **Versiyon kontrolü** - Environment'ı kolayca yönet
- ✅ **Taşınabilir** - conda-pack ile tek dosya

## ⚠️ Sınırlamalar
- ❌ **Tesseract ayrı** - Her sistemde Tesseract kurmalısınız
- ⚠️ **Platform bağımlı** - macOS environment'ı Linux'ta çalışmaz

---

## 🚀 Hızlı Başlangıç

### Adım 1: Conda Environment Oluştur (Şu anki sistemde - internet varken)

```bash
cd conda-method

# Conda/Miniconda kurulu değilse:
# macOS: brew install miniconda
# Linux: wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# Windows: https://docs.conda.io/en/latest/miniconda.html

# Environment oluştur
conda env create -f environment.yml

# Başarılı mı kontrol et
conda env list | grep ocr-converter
```

### Adım 2: conda-pack ile Paketle

```bash
# conda-pack kur (tek seferlik)
conda install -c conda-forge conda-pack

# Environment'ı aktifleştir
conda activate ocr-converter

# Paketle (5-10 dakika sürebilir)
conda pack -n ocr-converter -o ocr-converter-env.tar.gz

# Boyutu kontrol et
ls -lh ocr-converter-env.tar.gz
# Yaklaşık 500 MB - 1 GB olmalı
```

### Adım 3: USB/Cloud'a Kopyala

```bash
# Bu dosyayı taşı:
# ocr-converter-env.tar.gz
```

---

## 💻 Yeni Sistemde Kullanım

### Önce Conda Kur (Tek seferlik - Offline mümkün)

**macOS:**
```bash
# Miniconda installer'ı indir (offline kullanım için)
# https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
```

**Linux:**
```bash
# Offline installer
bash Miniconda3-latest-Linux-x86_64.sh
```

**Windows:**
```bash
# Offline installer
Miniconda3-latest-Windows-x86_64.exe
```

### Tesseract Kur

⚠️ **Önemli:** Conda environment'ı Tesseract içermez, sistem düzeyinde kurmalısınız.

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-tur tesseract-ocr-eng
```

**Windows:**
```bash
# https://github.com/UB-Mannheim/tesseract/wiki
# tesseract-ocr-setup.exe indir ve kur
```

### Environment'ı Aç ve Çalıştır

```bash
# Environment klasörü oluştur
mkdir -p ~/ocr-env

# Paketlenmiş environment'ı aç
tar -xzf ocr-converter-env.tar.gz -C ~/ocr-env

# Environment'ı aktifleştir
source ~/ocr-env/bin/activate

# conda-unpack çalıştır (ilk seferlik)
conda-unpack

# Şimdi kullanıma hazır!
python --version
python -c "import PyQt6; print('OK')"
```

### Uygulamayı Çalıştır

```bash
# Environment aktifken
cd /path/to/ocr-converter-clean
python src/main.py
```

---

## 📁 Klasör Yapısı

```
conda-method/
├── environment.yml         # Conda environment tanımı
├── README_CONDA.md         # Bu dosya
├── setup-conda.sh          # Otomatik kurulum scripti
└── run-conda.sh            # Otomatik çalıştırma scripti
```

---

## 🎯 Komut Referansı

### Environment Yönetimi

```bash
# Environment oluştur
conda env create -f environment.yml

# Environment'ları listele
conda env list

# Environment aktifleştir
conda activate ocr-converter

# Environment deaktifleştir
conda deactivate

# Environment sil
conda env remove -n ocr-converter

# Environment'ı güncelle
conda env update -f environment.yml
```

### conda-pack Kullanımı

```bash
# Pack et
conda pack -n ocr-converter -o env.tar.gz

# Belirli formatta pack et
conda pack -n ocr-converter -o env.tar.gz --format tar.gz

# Çıkış klasörü belirt
conda pack -n ocr-converter --output-dir ./packages

# Prefix'i değiştir (farklı path için)
conda pack -n ocr-converter --dest-prefix /custom/path
```

### Environment Açma (Unpack)

```bash
# Klasöre çıkar
mkdir myenv
tar -xzf env.tar.gz -C myenv

# Aktifleştir
source myenv/bin/activate

# Unpack et (path'leri düzelt)
conda-unpack

# Kullan
python your_script.py
```

---

## 🔧 Sorun Giderme

### "conda: command not found"

```bash
# Conda PATH'te mi kontrol et
which conda

# Yoksa:
# macOS/Linux:
export PATH="$HOME/miniconda3/bin:$PATH"

# Kalıcı yapmak için ~/.bashrc veya ~/.zshrc'ye ekle:
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### "CondaPackError: Cannot pack"

```bash
# Environment'ın doğru aktif olduğundan emin ol
conda activate ocr-converter

# Veya tam path ile
conda pack -p /path/to/env -o env.tar.gz
```

### Paket bulunamıyor

```bash
# Conda kanallarını kontrol et
conda config --show channels

# conda-forge ekle
conda config --add channels conda-forge

# Environment'ı yeniden oluştur
conda env remove -n ocr-converter
conda env create -f environment.yml
```

### "Tesseract not found" - Environment'ta

```bash
# Tesseract sistem düzeyinde kurulu olmalı
# Conda environment'ı içinde DEĞIL

# macOS
brew install tesseract

# Linux
sudo apt-get install tesseract-ocr

# Kontrol et
which tesseract
tesseract --version
```

### Platform uyumsuzluğu

```bash
# macOS environment'ı Linux'ta çalışmaz
# Her platform için ayrı pack etmelisiniz

# Veya platform-bağımsız environment.yml kullanın
# (Bizim environment.yml zaten platform-bağımsız)
```

---

## 💡 İpuçları

### Performans

- Conda environment native performans sunar (Docker'dan daha hızlı)
- SSD kullanımı önerilir
- İlk çalıştırma yavaş olabilir (JIT compilation)

### Boyut Optimizasyonu

```bash
# Gereksiz dosyaları temizle
conda clean --all

# Sadece gerekli paketler
conda list --export > packages.txt
conda create --name minimal --file packages.txt
```

### Offline Conda Kurulumu

```bash
# Miniconda installer'ı önceden indir
# Yeni sistemde:
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3

# Hiç paket indirmeden environment oluştur
conda create --name myenv --offline --use-local python=3.11
```

---

## 📊 Karşılaştırma

| Özellik | Docker | Conda | PyInstaller |
|---------|--------|-------|-------------|
| Tesseract | ✅ Dahil | ❌ Ayrı kur | ❌ Ayrı kur |
| Boyut | 1-2 GB | 500 MB-1 GB | 200-300 MB |
| Hız | Yavaş (container) | ✅ Hızlı (native) | ✅ Hızlı (native) |
| Platform | ✅ Hepsi | ⚠️ Platform-specific | ⚠️ Platform-specific |
| Geliştirme | ⚠️ Zor | ✅ Kolay | ❌ Her build zor |
| İzolasyon | ✅ Tam | ✅ İyi | ❌ Yok |

**Seçim:** Conda, **geliştirme ve bilimsel hesaplama** için ideal!

---

## 🎓 Özet

1. ✅ `conda env create -f environment.yml`
2. ✅ `conda activate ocr-converter`
3. ✅ `conda pack -n ocr-converter -o ocr-env.tar.gz`
4. ✅ Dosyayı USB'ye kopyala (~500 MB-1 GB)
5. ✅ Yeni sistemde:
   - Conda kur (Miniconda)
   - Tesseract kur
   - `tar -xzf ocr-env.tar.gz -C ~/ocr-env`
   - `source ~/ocr-env/bin/activate`
   - `conda-unpack`
6. ✅ Çalıştır: `python src/main.py`

**Hafif ve hızlı, ama Tesseract ayrı kurulmalı!**

---

## 🔗 Kaynaklar

- **Conda Docs:** https://docs.conda.io/
- **conda-pack:** https://conda.github.io/conda-pack/
- **Miniconda:** https://docs.conda.io/en/latest/miniconda.html
- **Tesseract:** https://github.com/tesseract-ocr/tesseract

---

**Sorular için:** Ana dizindeki `README.md`
