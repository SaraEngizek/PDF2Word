#!/bin/bash
# Conda Environment Otomatik Kurulum

set -e

echo "🐍 OCR Converter - Conda Kurulumu"
echo "==================================="
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Conda kontrolü
echo "🔍 Conda kontrol ediliyor..."
if command -v conda &> /dev/null; then
    echo -e "${GREEN}✅ Conda bulundu: $(conda --version)${NC}"
else
    echo -e "${RED}❌ Conda bulunamadı!${NC}"
    echo ""
    echo "Conda kurulumu gerekli:"
    echo ""
    echo "macOS:"
    echo "  brew install miniconda"
    echo ""
    echo "Linux:"
    echo "  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    echo "  bash Miniconda3-latest-Linux-x86_64.sh"
    echo ""
    echo "Windows:"
    echo "  https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Environment var mı kontrol et
echo ""
echo "🔍 Mevcut environment kontrol ediliyor..."
if conda env list | grep -q "ocr-converter"; then
    echo -e "${YELLOW}⚠️  ocr-converter environment zaten mevcut!${NC}"
    echo "Silip yeniden oluşturmak ister misiniz? (y/n)"
    read -r response
    if [[ "$response" == "y" ]]; then
        conda env remove -n ocr-converter
        echo -e "${GREEN}✅ Eski environment silindi${NC}"
    else
        echo "Kurulum iptal edildi"
        exit 0
    fi
fi

# Environment oluştur
echo ""
echo "📦 Environment oluşturuluyor..."
echo "   (Bu işlem 5-10 dakika sürebilir)"
conda env create -f environment.yml

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Environment başarıyla oluşturuldu${NC}"
else
    echo -e "${RED}❌ Environment oluşturulamadı!${NC}"
    exit 1
fi

# conda-pack kontrol et
echo ""
echo "🔍 conda-pack kontrol ediliyor..."
if conda list -n base | grep -q "conda-pack"; then
    echo -e "${GREEN}✅ conda-pack kurulu${NC}"
else
    echo -e "${YELLOW}⚠️  conda-pack kurulu değil${NC}"
    echo "conda-pack kurmak ister misiniz? (portable environment için gerekli) (y/n)"
    read -r response
    if [[ "$response" == "y" ]]; then
        conda install -c conda-forge conda-pack -y
        echo -e "${GREEN}✅ conda-pack kuruldu${NC}"
    fi
fi

# Tesseract kontrol et
echo ""
echo "🔍 Tesseract kontrol ediliyor..."
if command -v tesseract &> /dev/null; then
    echo -e "${GREEN}✅ Tesseract bulundu: $(tesseract --version | head -1)${NC}"
else
    echo -e "${YELLOW}⚠️  Tesseract bulunamadı!${NC}"
    echo ""
    echo "Tesseract kurulumu gerekli:"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS:"
        echo "  brew install tesseract tesseract-lang"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Linux:"
        echo "  sudo apt-get install tesseract-ocr tesseract-ocr-tur"
    fi
    echo ""
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Kurulum tamamlandı!${NC}"
echo "=========================================="
echo ""
echo "Kullanım:"
echo "  1. Environment'ı aktifleştir:"
echo "     conda activate ocr-converter"
echo ""
echo "  2. Uygulamayı çalıştır:"
echo "     cd ../  # ana dizine dön"
echo "     python src/main.py"
echo ""
echo "  3. Deaktifleştir:"
echo "     conda deactivate"
echo ""
echo "Portable hale getirmek için:"
echo "  conda activate ocr-converter"
echo "  conda pack -n ocr-converter -o ocr-converter-env.tar.gz"
echo ""
