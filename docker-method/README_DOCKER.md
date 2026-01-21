# 🐳 Docker Yöntemi - Tamamen Offline OCR

## ✅ Avantajları
- ✅ **Tesseract dahil** - Hiçbir şey kurmanıza gerek yok
- ✅ **Tüm bağımlılıklar dahil** - Python, kütüphaneler, her şey
- ✅ **Platform bağımsız** - Windows, macOS, Linux'ta aynı şekilde çalışır
- ✅ **Tamamen izole** - Sisteminizi kirletmez
- ✅ **Network: none** - İnternet bağlantısı bile gerektirmez

## 📦 Boyut
- **Docker Image:** ~1.5-2 GB (her şey dahil)
- **Export edilmiş .tar.gz:** ~800 MB - 1.2 GB

---

## 🚀 Hızlı Başlangıç

### Adım 1: Docker Image Oluştur (Şu anki sistemde - internet varken)

```bash
cd docker-method

# Image oluştur (5-10 dakika sürer)
docker build -t ocr-converter:latest .

# Başarılı mı kontrol et
docker images | grep ocr-converter
```

### Adım 2: Image'i Dosyaya Çıkar (Taşınabilir hale getir)

```bash
# Image'i tar.gz dosyasına çıkar
docker save ocr-converter:latest | gzip > ocr-converter-docker-image.tar.gz

# Boyutunu kontrol et
ls -lh ocr-converter-docker-image.tar.gz
# Yaklaşık 800 MB - 1.2 GB olmalı
```

### Adım 3: USB/Cloud'a Kopyala

```bash
# Bu dosyayı taşı:
# ocr-converter-docker-image.tar.gz
```

---

## 💻 Yeni Sistemde Kullanım (Tamamen Offline)

### Önce Docker Kur (Tek seferlik)

**macOS:**
```bash
# Docker Desktop indir ve kur (offline installer mevcut)
# https://docs.docker.com/desktop/install/mac-install/
```

**Linux:**
```bash
# Offline paket kurulumu (önceden indir)
sudo apt-get install docker.io docker-compose
# veya
sudo yum install docker docker-compose
```

**Windows:**
```bash
# Docker Desktop for Windows (offline installer)
# https://docs.docker.com/desktop/install/windows-install/
```

### Image'i Yükle

```bash
# tar.gz dosyasını yükle
docker load < ocr-converter-docker-image.tar.gz

# Yüklendiğini kontrol et
docker images | grep ocr-converter
```

### Çalıştır

**Basit Kullanım:**
```bash
# Input/output klasörleri oluştur
mkdir -p input output

# Dosyalarınızı input/ klasörüne koyun

# OCR işlemini başlat
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  ocr-converter:latest python src/main.py
```

**GUI ile Kullanım (macOS/Linux):**
```bash
# X11 forwarding ile GUI'yi göster
xhost +local:docker

docker run --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  ocr-converter:latest
```

**Docker Compose ile (Önerilen):**
```bash
# docker-compose.yml dosyasını kopyala
# Sonra:
docker-compose up
```

---

## 📁 Klasör Yapısı

```
docker-method/
├── Dockerfile              # Docker image tanımı
├── docker-compose.yml      # Kolay çalıştırma
├── README_DOCKER.md        # Bu dosya
├── run-docker.sh           # Otomatik çalıştırma scripti (macOS/Linux)
└── run-docker.bat          # Otomatik çalıştırma scripti (Windows)
```

---

## 🎯 Komut Referansı

### Image Oluşturma
```bash
# Build et
docker build -t ocr-converter:latest .

# Build cache olmadan (temiz build)
docker build --no-cache -t ocr-converter:latest .
```

### Image Yönetimi
```bash
# Image'leri listele
docker images

# Image boyutunu gör
docker images ocr-converter:latest

# Image'i sil
docker rmi ocr-converter:latest
```

### Container Yönetimi
```bash
# Çalışan container'ları gör
docker ps

# Tüm container'ları gör
docker ps -a

# Container'ı durdur
docker stop <container-id>

# Container'ı sil
docker rm <container-id>
```

### Export/Import
```bash
# Export et (taşıma için)
docker save ocr-converter:latest | gzip > ocr-converter.tar.gz

# Import et (yeni sistemde)
docker load < ocr-converter.tar.gz

# Veya gzip olmadan:
docker save ocr-converter:latest -o ocr-converter.tar
docker load -i ocr-converter.tar
```

---

## 🔧 Sorun Giderme

### "Cannot connect to Docker daemon"
```bash
# Docker servisini başlat
sudo systemctl start docker  # Linux
# veya Docker Desktop'ı aç (macOS/Windows)
```

### "Permission denied"
```bash
# Kullanıcıyı docker grubuna ekle (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

### GUI çalışmıyor (macOS)
```bash
# XQuartz kur
brew install --cask xquartz

# XQuartz'ı başlat ve ayarları kontrol et
# Preferences > Security > "Allow connections from network clients"
```

### Container çok yavaş
```bash
# Docker'a daha fazla kaynak ayır
# Docker Desktop > Settings > Resources
# - CPU: 4+ cores
# - Memory: 4+ GB
```

### Image çok büyük
```bash
# Multi-stage build kullan (Dockerfile'da zaten var)
# Veya alpine base image kullan (daha küçük)
```

---

## 💡 İpuçları

### Performans
- Docker'a en az 4 GB RAM ayırın
- SSD kullanıyorsanız daha hızlı çalışır
- Volume mount yerine COPY kullanırsanız daha hızlı (ama dosya paylaşımı olmaz)

### Güvenlik
- `--network none` ile internet bağlantısını kesin (zaten docker-compose.yml'de var)
- Container'ları root olmayan kullanıcı ile çalıştırın
- Hassas dosyalar için volume encryption kullanın

### Pratiklik
- Alias oluşturun:
  ```bash
  alias ocr='docker run --rm -v $(pwd):/app/files ocr-converter:latest'
  ```
- Bashrc'ye ekleyin
- `ocr myfile.pdf` şeklinde kullanın

---

## 📊 Karşılaştırma

| Özellik | Docker | Conda | PyInstaller |
|---------|--------|-------|-------------|
| Tesseract | ✅ Dahil | ❌ Ayrı kur | ❌ Ayrı kur |
| Boyut | 1-2 GB | 500 MB-1 GB | 200-300 MB |
| Kurulum | Kolay | Orta | Kolay |
| Taşınabilirlik | ✅ Mükemmel | ✅ İyi | ⚠️ Tesseract gerekir |
| İzolasyon | ✅ Tam | ⚠️ Kısmi | ❌ Yok |

**Seçim:** Docker daha büyük ama **en kolay ve eksiksiz** çözüm!

---

## 🎓 Özet

1. ✅ `docker build -t ocr-converter:latest .`
2. ✅ `docker save ocr-converter:latest | gzip > ocr-converter.tar.gz`
3. ✅ Dosyayı USB'ye kopyala (~1 GB)
4. ✅ Yeni sistemde: `docker load < ocr-converter.tar.gz`
5. ✅ Çalıştır: `docker run ocr-converter:latest`

**Tesseract dahil, hiçbir ek kurulum gerekmez!** 🎉

---

**Sorular için:** Ana dizindeki `README.md` veya Docker dokümantasyonu
