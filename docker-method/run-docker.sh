#!/bin/bash
# Docker ile OCR Converter Otomatik Çalıştırma

echo "🐳 OCR Converter - Docker Yöntemi"
echo "=================================="
echo ""

# Input/output klasörleri kontrol et
if [ ! -d "input" ]; then
    echo "📁 input/ klasörü oluşturuluyor..."
    mkdir -p input
    echo "   Dosyalarınızı input/ klasörüne koyun"
fi

if [ ! -d "output" ]; then
    echo "📁 output/ klasörü oluşturuluyor..."
    mkdir -p output
fi

# Image kontrol et
echo ""
echo "🔍 Docker image kontrol ediliyor..."
if docker images | grep -q "ocr-converter"; then
    echo "✅ Image bulundu"
else
    echo "❌ Image bulunamadı!"
    echo ""
    echo "Lütfen önce image'i yükleyin:"
    echo "  docker load < ocr-converter-docker-image.tar.gz"
    echo ""
    echo "Veya build edin:"
    echo "  docker build -t ocr-converter:latest ."
    exit 1
fi

# GUI mi yoksa CLI mi?
echo ""
echo "Nasıl çalıştırmak istersiniz?"
echo "1) GUI (Grafik Arayüz)"
echo "2) CLI (Komut Satırı - input/ klasöründeki dosyaları işle)"
read -p "Seçiminiz (1/2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "🖥️  GUI modu başlatılıyor..."
    echo "   Not: X11 forwarding gerekli (XQuartz macOS'ta)"

    # macOS için XQuartz kontrolü
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if ! command -v xquartz &> /dev/null; then
            echo "⚠️  XQuartz bulunamadı. GUI çalışmayabilir."
            echo "   Kurulum: brew install --cask xquartz"
        else
            xhost +local:docker 2>/dev/null
        fi
    fi

    docker run --rm \
        -e DISPLAY=$DISPLAY \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -v $(pwd)/input:/app/input \
        -v $(pwd)/output:/app/output \
        --network none \
        ocr-converter:latest

elif [ "$choice" = "2" ]; then
    echo ""
    echo "📋 CLI modu başlatılıyor..."
    echo "   input/ klasöründeki dosyalar işlenecek"

    # Input klasöründe dosya var mı kontrol et
    if [ -z "$(ls -A input)" ]; then
        echo "❌ input/ klasörü boş!"
        echo "   Lütfen işlemek istediğiniz PDF/görsel dosyalarını input/ klasörüne koyun"
        exit 1
    fi

    docker run --rm \
        -v $(pwd)/input:/app/input \
        -v $(pwd)/output:/app/output \
        --network none \
        ocr-converter:latest \
        python src/ocr_processor.py --input /app/input --output /app/output

else
    echo "❌ Geçersiz seçim"
    exit 1
fi

echo ""
echo "✅ İşlem tamamlandı!"
echo "📂 Sonuçlar output/ klasöründe"
