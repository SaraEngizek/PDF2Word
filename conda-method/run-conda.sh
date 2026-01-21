#!/bin/bash
# Conda Environment ile OCR Converter Çalıştırma

echo "🐍 OCR Converter - Conda Yöntemi"
echo "================================="
echo ""

# Conda kontrol
if ! command -v conda &> /dev/null; then
    echo "❌ Conda bulunamadı!"
    echo "Lütfen önce setup-conda.sh scriptini çalıştırın"
    exit 1
fi

# Environment aktif mi kontrol et
if [[ "$CONDA_DEFAULT_ENV" != "ocr-converter" ]]; then
    echo "🔧 Environment aktifleştiriliyor..."
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate ocr-converter

    if [ $? -ne 0 ]; then
        echo "❌ Environment aktifleştirilemedi!"
        echo "Environment mevcut mu kontrol edin:"
        echo "  conda env list"
        exit 1
    fi
fi

# Tesseract kontrol
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Tesseract bulunamadı!"
    echo "Uygulama Tesseract olmadan çalışmaz."
    echo ""
    echo "Kurulum:"
    echo "  macOS: brew install tesseract tesseract-lang"
    echo "  Linux: sudo apt-get install tesseract-ocr tesseract-ocr-tur"
    echo ""
    exit 1
fi

# Ana dizine git
cd ../

# Uygulamayı çalıştır
echo "🚀 OCR Converter başlatılıyor..."
python src/main.py

# Deaktifleştir (opsiyonel)
# conda deactivate
