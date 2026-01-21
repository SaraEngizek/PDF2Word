#!/bin/bash
# ============================================
# PDF2Word - macOS Build
# Tesseract gömülü, Poppler sistem'den
# Intel ve Apple Silicon desteği
# ============================================

set -e

echo ""
echo "========================================"
echo "  PDF2Word - macOS Build"
echo "  Tesseract gömülü"
echo "  Poppler = brew install poppler"
echo "========================================"
echo ""

# Proje kök dizinine git
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "[1/7] Proje dizini: $PROJECT_ROOT"

# Homebrew kontrolü
echo "[2/7] Homebrew kontrol ediliyor..."
if ! command -v brew &> /dev/null; then
    echo "Homebrew bulunamadı. Yükleniyor..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Homebrew prefix bul
if [ -d "/opt/homebrew" ]; then
    HOMEBREW_PREFIX="/opt/homebrew"
else
    HOMEBREW_PREFIX="/usr/local"
fi
echo "Homebrew prefix: $HOMEBREW_PREFIX"

# Python kontrolü
echo "[3/7] Python kontrol ediliyor..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 bulunamadı. Yükleniyor..."
    brew install python@3.11
fi

# Poppler kontrolü - SİSTEMDEN KULLANILACAK
echo "[4/7] Poppler kontrol ediliyor..."
if ! command -v pdftoppm &> /dev/null; then
    echo "Poppler bulunamadı. Yükleniyor..."
    brew install poppler
fi
echo "✓ Poppler kurulu: $(which pdftoppm)"

# Tesseract kontrolü
if ! command -v tesseract &> /dev/null; then
    echo "Tesseract bulunamadı. Yükleniyor..."
    brew install tesseract tesseract-lang
fi
echo "✓ Tesseract kurulu: $(which tesseract)"

# Virtual environment oluştur
echo "[5/7] Virtual environment hazırlanıyor..."
rm -rf venv 2>/dev/null || true
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
echo "[6/7] Bağımlılıklar yükleniyor..."
pip install --upgrade pip
pip install PyQt6 pytesseract pdf2image Pillow numpy python-docx
pip install pyinstaller

# Tesseract tessdata'yı bundle'a kopyala
echo "Tessdata hazırlanıyor..."
TESSDATA_DIR="$PROJECT_ROOT/portable-build/tesseract-bundle/tessdata"
mkdir -p "$TESSDATA_DIR"

if [ -d "$HOMEBREW_PREFIX/share/tessdata" ]; then
    cp "$HOMEBREW_PREFIX/share/tessdata"/*.traineddata "$TESSDATA_DIR/" 2>/dev/null || true
    echo "Tessdata kopyalandı: $(ls "$TESSDATA_DIR" | wc -l | tr -d ' ') dosya"
fi

# Build işlemi
echo "[7/7] PyInstaller ile build yapılıyor..."
cd "$PROJECT_ROOT"

pyinstaller --clean --noconfirm \
    portable-build/specs/macos_portable.spec

if [ $? -ne 0 ]; then
    echo "HATA: Build başarısız!"
    exit 1
fi

# DMG oluştur
echo ""
echo "DMG oluşturuluyor..."
APP_NAME="PDF2Word"
DMG_NAME="PDF2Word_macOS"

if [ -d "dist/$APP_NAME.app" ]; then
    rm -f "dist/$DMG_NAME.dmg" 2>/dev/null || true
    hdiutil create -volname "$APP_NAME" -srcfolder "dist/$APP_NAME.app" -ov -format UDZO "dist/$DMG_NAME.dmg"
fi

# Başarılı
echo ""
echo "========================================"
echo "  BUILD BAŞARILI!"
echo "========================================"
echo ""
echo "Çıktı dosyaları:"
echo "  App: $PROJECT_ROOT/dist/$APP_NAME.app"
if [ -f "dist/$DMG_NAME.dmg" ]; then
    DMG_SIZE=$(du -h "dist/$DMG_NAME.dmg" | cut -f1)
    echo "  DMG: $PROJECT_ROOT/dist/$DMG_NAME.dmg ($DMG_SIZE)"
fi
echo ""
echo "⚠️  ÖNEMLİ: Bu uygulama için gereksinimler:"
echo "   - Tesseract: brew install tesseract tesseract-lang"
echo "   - Poppler: brew install poppler"
echo ""
echo "   Kullanıcılar bu iki paketi yükledikten sonra"
echo "   uygulama çalışacaktır."
echo ""
