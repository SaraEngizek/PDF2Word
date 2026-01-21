#!/bin/bash
# ============================================
# PDF2Word - Linux Portable Build
# Tesseract gömülü, internet gerektirmeyen
# AppImage formatında çıktı
# pdf2image (poppler) kullanılıyor
# ============================================

set -e

echo ""
echo "========================================"
echo "  PDF2Word - Linux Build"
echo "  Portable Versiyon (Tesseract Gömülü)"
echo "========================================"
echo ""

# Proje kök dizinine git
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "[1/9] Proje dizini: $PROJECT_ROOT"

# Dağıtım kontrolü
echo "[2/9] Sistem bilgisi alınıyor..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "Dağıtım: $NAME $VERSION"
fi

# Python kontrolü
echo "[3/9] Python kontrol ediliyor..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 bulunamadı. Yükleniyor..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python python-pip
    else
        echo "HATA: Paket yöneticisi bulunamadı. Python3'ü manuel yükleyin."
        exit 1
    fi
fi

# Poppler kontrolü (pdf2image için gerekli)
echo "[4/9] Poppler kontrol ediliyor..."
if ! command -v pdftoppm &> /dev/null; then
    echo "Poppler bulunamadı. Yükleniyor..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y poppler-utils
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y poppler-utils
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm poppler
    else
        echo "UYARI: Poppler yüklenemedi. PDF işleme çalışmayabilir."
    fi
fi

# Sistem bağımlılıkları
echo "[5/9] Sistem bağımlılıkları kontrol ediliyor..."
PACKAGES_TO_INSTALL=""

# Qt bağımlılıkları
if ! ldconfig -p | grep -q libQt6; then
    if command -v apt-get &> /dev/null; then
        PACKAGES_TO_INSTALL="$PACKAGES_TO_INSTALL libxcb-xinerama0 libxcb-cursor0"
    fi
fi

if [ -n "$PACKAGES_TO_INSTALL" ]; then
    echo "Gerekli paketler yükleniyor: $PACKAGES_TO_INSTALL"
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y $PACKAGES_TO_INSTALL
    fi
fi

# Virtual environment oluştur
echo "[6/9] Virtual environment hazırlanıyor..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Bağımlılıkları yükle
echo "[7/9] Bağımlılıklar yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# Tesseract bundle hazırla
echo "[8/9] Tesseract bundle hazırlanıyor..."
TESSERACT_BUNDLE="$PROJECT_ROOT/portable-build/tesseract-bundle/linux"
TESSDATA_DIR="$PROJECT_ROOT/portable-build/tesseract-bundle/tessdata"

mkdir -p "$TESSERACT_BUNDLE/bin"
mkdir -p "$TESSERACT_BUNDLE/lib"
mkdir -p "$TESSDATA_DIR"

# Sistem Tesseract'ını kontrol et
if command -v tesseract &> /dev/null; then
    TESSERACT_PATH=$(which tesseract)
    TESSERACT_VERSION=$(tesseract --version 2>&1 | head -1)
    echo "Sistem Tesseract bulundu: $TESSERACT_VERSION"

    # Tesseract binary'sini kopyala
    if [ ! -f "$TESSERACT_BUNDLE/bin/tesseract" ]; then
        cp "$TESSERACT_PATH" "$TESSERACT_BUNDLE/bin/"

        # Bağımlı kütüphaneleri bul ve kopyala
        echo "Kütüphaneler kopyalanıyor..."
        for lib in $(ldd "$TESSERACT_PATH" | grep "=> /" | awk '{print $3}'); do
            # Sistem kütüphanelerini atla
            if [[ ! "$lib" =~ ^/lib ]] && [[ ! "$lib" =~ ^/usr/lib/x86_64-linux-gnu/lib(c|m|pthread|dl|rt) ]]; then
                cp "$lib" "$TESSERACT_BUNDLE/lib/" 2>/dev/null || true
            fi
        done
    fi

    # Tessdata'yı kopyala
    SYSTEM_TESSDATA=""
    if [ -d "/usr/share/tesseract-ocr/5/tessdata" ]; then
        SYSTEM_TESSDATA="/usr/share/tesseract-ocr/5/tessdata"
    elif [ -d "/usr/share/tesseract-ocr/4.00/tessdata" ]; then
        SYSTEM_TESSDATA="/usr/share/tesseract-ocr/4.00/tessdata"
    elif [ -d "/usr/share/tessdata" ]; then
        SYSTEM_TESSDATA="/usr/share/tessdata"
    fi

    if [ -n "$SYSTEM_TESSDATA" ] && [ ! -f "$TESSDATA_DIR/eng.traineddata" ]; then
        echo "Tessdata kopyalanıyor: $SYSTEM_TESSDATA"
        cp "$SYSTEM_TESSDATA"/*.traineddata "$TESSDATA_DIR/" 2>/dev/null || true
    fi
else
    echo ""
    echo "!!! UYARI: Sistem Tesseract bulunamadı!"
    echo ""
    echo "Lütfen önce Tesseract'ı yükleyin:"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get install tesseract-ocr tesseract-ocr-tur"
    echo ""
    echo "Fedora:"
    echo "  sudo dnf install tesseract tesseract-langpack-tur"
    echo ""
    echo "Arch:"
    echo "  sudo pacman -S tesseract tesseract-data-tur"
    echo ""

    read -p "Yine de devam etmek ister misiniz? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build işlemi
echo "[9/9] PyInstaller ile build yapılıyor..."
cd "$PROJECT_ROOT"

pyinstaller --clean --noconfirm \
    portable-build/specs/linux_portable.spec

if [ $? -ne 0 ]; then
    echo "HATA: Build başarısız!"
    exit 1
fi

# AppImage oluştur (opsiyonel)
echo ""
echo "AppImage oluşturmaya çalışılıyor..."

# AppImageTool indir
APPIMAGE_TOOL="$PROJECT_ROOT/portable-build/appimagetool-x86_64.AppImage"
if [ ! -f "$APPIMAGE_TOOL" ]; then
    echo "AppImageTool indiriliyor..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" \
        -O "$APPIMAGE_TOOL" 2>/dev/null || true
    chmod +x "$APPIMAGE_TOOL" 2>/dev/null || true
fi

# AppDir oluştur
APPDIR="$PROJECT_ROOT/dist/OCR_Donusturucu.AppDir"
if [ -f "$PROJECT_ROOT/dist/ocr-donusturucu" ]; then
    mkdir -p "$APPDIR/usr/bin"
    mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

    # Binary kopyala
    cp "$PROJECT_ROOT/dist/ocr-donusturucu" "$APPDIR/usr/bin/"

    # Desktop entry oluştur
    cat > "$APPDIR/ocr-donusturucu.desktop" << 'EOF'
[Desktop Entry]
Name=PDF2Word
Comment=Offline OCR Application
Exec=ocr-donusturucu
Icon=ocr-donusturucu
Type=Application
Categories=Office;Graphics;
EOF

    # AppRun oluştur
    cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/ocr-donusturucu" "$@"
EOF
    chmod +x "$APPDIR/AppRun"

    # AppImage oluştur
    if [ -f "$APPIMAGE_TOOL" ]; then
        ARCH=x86_64 "$APPIMAGE_TOOL" "$APPDIR" "$PROJECT_ROOT/dist/OCR_Donusturucu-x86_64.AppImage" 2>/dev/null || true
    fi
fi

# Başarılı
echo ""
echo "========================================"
echo "  BUILD BAŞARILI!"
echo "========================================"
echo ""
echo "Çıktı dosyaları:"
echo "  Binary: $PROJECT_ROOT/dist/ocr-donusturucu"
if [ -f "$PROJECT_ROOT/dist/OCR_Donusturucu-x86_64.AppImage" ]; then
    echo "  AppImage: $PROJECT_ROOT/dist/OCR_Donusturucu-x86_64.AppImage"
fi
echo ""
echo "Kullanım:"
echo "  chmod +x dist/ocr-donusturucu"
echo "  ./dist/ocr-donusturucu"
echo ""
echo "Bu uygulama tamamen portable:"
echo "- Tesseract gömülü (eğer bundle varsa)"
echo "- Poppler (PDF işleme) sistem kurulumu kullanılıyor"
echo "- Internet gerektirmez"
echo "- USB'den çalışır"
echo ""
