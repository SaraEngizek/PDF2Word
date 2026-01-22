#!/bin/bash
# PDF2Word - Linux Offline Kurulum Scripti
# Tesseract OCR ve Poppler'ı offline deb paketlerinden kurar

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "  PDF2Word - Linux Offline Kurulum"
echo "============================================================"
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Root kontrolü
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}⚠${NC}  Bu script root yetkisi gerektirir."
    echo "Lütfen şu şekilde çalıştırın: sudo ./install.sh"
    exit 1
fi

# Tesseract kontrolü
echo "🔍 Sistem kontrol ediliyor..."
NEED_INSTALL=false

if ! command -v tesseract &> /dev/null; then
    echo -e "${YELLOW}⚠${NC}  Tesseract OCR bulunamadı"
    NEED_INSTALL=true
else
    echo -e "${GREEN}✓${NC} Tesseract bulundu: $(tesseract --version 2>&1 | head -n1)"
fi

if ! command -v pdftoppm &> /dev/null; then
    echo -e "${YELLOW}⚠${NC}  Poppler (pdftoppm) bulunamadı"
    NEED_INSTALL=true
else
    echo -e "${GREEN}✓${NC} Poppler bulundu"
fi

echo ""

# Kurulum gerekiyorsa
if [ "$NEED_INSTALL" = true ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📥 Offline paketler kuruluyor..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [ -d "debs" ] && [ "$(ls -A debs/*.deb 2>/dev/null)" ]; then
        # Deb paketlerini kur
        dpkg -i debs/*.deb 2>/dev/null || true

        # Eksik bağımlılıkları çöz
        apt-get install -f -y 2>/dev/null || true

        echo -e "${GREEN}✓${NC} Paketler kuruldu"
    else
        echo -e "${RED}❌ HATA: debs/ klasöründe paket bulunamadı!${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} Tüm bağımlılıklar zaten kurulu"
fi

echo ""
echo "============================================================"
echo -e "${GREEN}✅ Kurulum tamamlandı!${NC}"
echo "============================================================"
echo ""
echo "Şimdi PDF2Word uygulamasını çalıştırabilirsiniz:"
echo "  ./PDF2Word"
echo ""
