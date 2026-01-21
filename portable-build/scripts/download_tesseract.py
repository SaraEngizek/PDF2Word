#!/usr/bin/env python3
"""
Tesseract Bundle Hazırlayıcı
Tüm platformlar için Tesseract ve tessdata indirir/kopyalar

Bu script:
1. Tesseract'ı sistem kurulumundan kopyalar veya indirir
2. Gerekli dil dosyalarını (tessdata) indirir
3. Bundle klasörünü hazırlar
"""

import os
import sys
import platform
import shutil
import urllib.request
import zipfile
import tarfile
from pathlib import Path


# Tessdata indirme URL'leri (GitHub releases)
TESSDATA_BASE_URL = "https://github.com/tesseract-ocr/tessdata_best/raw/main"

# İndirilecek diller
LANGUAGES = ['eng', 'tur', 'deu', 'fra', 'spa', 'ita', 'rus']

# Script dizini
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
BUNDLE_DIR = PROJECT_ROOT / "portable-build" / "tesseract-bundle"


def print_header(text):
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)


def print_step(num, text):
    print(f"\n[{num}] {text}")


def download_file(url, dest_path):
    """URL'den dosya indir"""
    print(f"    İndiriliyor: {url}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"    ✓ Kaydedildi: {dest_path}")
        return True
    except Exception as e:
        print(f"    ✗ Hata: {e}")
        return False


def setup_tessdata():
    """Tessdata dil dosyalarını indir"""
    print_header("Tessdata Hazırlanıyor")

    tessdata_dir = BUNDLE_DIR / "tessdata"
    tessdata_dir.mkdir(parents=True, exist_ok=True)

    print_step(1, f"Dil dosyaları indiriliyor: {', '.join(LANGUAGES)}")

    for lang in LANGUAGES:
        traineddata = tessdata_dir / f"{lang}.traineddata"
        if traineddata.exists():
            print(f"    ✓ {lang}.traineddata zaten mevcut")
            continue

        url = f"{TESSDATA_BASE_URL}/{lang}.traineddata"
        if not download_file(url, traineddata):
            # Alternatif: tessdata_fast dene
            url_fast = url.replace("tessdata_best", "tessdata_fast")
            download_file(url_fast, traineddata)

    print("\n✓ Tessdata hazır!")
    return tessdata_dir


def copy_system_tesseract_windows():
    """Windows'ta sistem Tesseract'ını kopyala"""
    print_header("Windows Tesseract Bundle")

    windows_bundle = BUNDLE_DIR / "windows"
    windows_bundle.mkdir(parents=True, exist_ok=True)

    # Olası Tesseract konumları
    possible_paths = [
        Path(r"C:\Program Files\Tesseract-OCR"),
        Path(r"C:\Program Files (x86)\Tesseract-OCR"),
    ]

    tesseract_dir = None
    for path in possible_paths:
        if path.exists() and (path / "tesseract.exe").exists():
            tesseract_dir = path
            break

    if not tesseract_dir:
        print("\n!!! Tesseract bulunamadı!")
        print("\nManuel kurulum gerekli:")
        print("1. https://github.com/UB-Mannheim/tesseract/wiki adresine gidin")
        print("2. tesseract-ocr-w64-setup-*.exe indirin")
        print("3. Kurulumu yapın")
        print("4. Bu scripti tekrar çalıştırın")
        return None

    print_step(1, f"Tesseract bulundu: {tesseract_dir}")
    print_step(2, "Dosyalar kopyalanıyor...")

    # tesseract.exe ve DLL'leri kopyala
    for item in tesseract_dir.iterdir():
        if item.suffix in ['.exe', '.dll'] or item.is_dir():
            dest = windows_bundle / item.name
            if item.is_file():
                shutil.copy2(item, dest)
                print(f"    ✓ {item.name}")
            elif item.is_dir() and item.name != 'tessdata':
                shutil.copytree(item, dest, dirs_exist_ok=True)
                print(f"    ✓ {item.name}/")

    print("\n✓ Windows bundle hazır!")
    return windows_bundle


def copy_system_tesseract_macos():
    """macOS'ta sistem Tesseract'ını kopyala"""
    print_header("macOS Tesseract Bundle")

    macos_bundle = BUNDLE_DIR / "macos"
    macos_bundle.mkdir(parents=True, exist_ok=True)
    (macos_bundle / "bin").mkdir(exist_ok=True)
    (macos_bundle / "lib").mkdir(exist_ok=True)

    # Tesseract konumu
    tesseract_path = shutil.which("tesseract")

    if not tesseract_path:
        # Homebrew konumlarını kontrol et
        for path in ["/usr/local/bin/tesseract", "/opt/homebrew/bin/tesseract"]:
            if Path(path).exists():
                tesseract_path = path
                break

    if not tesseract_path:
        print("\n!!! Tesseract bulunamadı!")
        print("\nKurulum için:")
        print("  brew install tesseract tesseract-lang")
        return None

    print_step(1, f"Tesseract bulundu: {tesseract_path}")
    print_step(2, "Binary kopyalanıyor...")

    # Binary'yi kopyala
    dest_bin = macos_bundle / "bin" / "tesseract"
    shutil.copy2(tesseract_path, dest_bin)
    os.chmod(dest_bin, 0o755)
    print(f"    ✓ tesseract")

    # Bağımlı kütüphaneleri bul (otool kullanarak)
    print_step(3, "Kütüphaneler kopyalanıyor...")
    try:
        import subprocess
        result = subprocess.run(
            ["otool", "-L", tesseract_path],
            capture_output=True, text=True
        )
        for line in result.stdout.split('\n'):
            if line.strip().startswith('/') and '/System/' not in line and '/usr/lib/' not in line:
                lib_path = line.split()[0]
                if Path(lib_path).exists():
                    lib_name = Path(lib_path).name
                    dest_lib = macos_bundle / "lib" / lib_name
                    shutil.copy2(lib_path, dest_lib)
                    print(f"    ✓ {lib_name}")
    except Exception as e:
        print(f"    Uyarı: Kütüphaneler kopyalanamadı: {e}")

    print("\n✓ macOS bundle hazır!")
    return macos_bundle


def copy_system_tesseract_linux():
    """Linux'ta sistem Tesseract'ını kopyala"""
    print_header("Linux Tesseract Bundle")

    linux_bundle = BUNDLE_DIR / "linux"
    linux_bundle.mkdir(parents=True, exist_ok=True)
    (linux_bundle / "bin").mkdir(exist_ok=True)
    (linux_bundle / "lib").mkdir(exist_ok=True)

    # Tesseract konumu
    tesseract_path = shutil.which("tesseract")

    if not tesseract_path:
        print("\n!!! Tesseract bulunamadı!")
        print("\nKurulum için:")
        print("  Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-tur")
        print("  Fedora: sudo dnf install tesseract tesseract-langpack-tur")
        print("  Arch: sudo pacman -S tesseract tesseract-data-tur")
        return None

    print_step(1, f"Tesseract bulundu: {tesseract_path}")
    print_step(2, "Binary kopyalanıyor...")

    # Binary'yi kopyala
    dest_bin = linux_bundle / "bin" / "tesseract"
    shutil.copy2(tesseract_path, dest_bin)
    os.chmod(dest_bin, 0o755)
    print(f"    ✓ tesseract")

    # Bağımlı kütüphaneleri bul (ldd kullanarak)
    print_step(3, "Kütüphaneler kopyalanıyor...")
    try:
        import subprocess
        result = subprocess.run(
            ["ldd", tesseract_path],
            capture_output=True, text=True
        )
        for line in result.stdout.split('\n'):
            if "=> /" in line:
                parts = line.split("=>")
                if len(parts) >= 2:
                    lib_path = parts[1].split()[0]
                    # Temel sistem kütüphanelerini atla
                    if Path(lib_path).exists() and not any(x in lib_path for x in
                        ['/libc.', '/libm.', '/libpthread.', '/libdl.', '/librt.', '/ld-linux']):
                        lib_name = Path(lib_path).name
                        dest_lib = linux_bundle / "lib" / lib_name
                        shutil.copy2(lib_path, dest_lib)
                        print(f"    ✓ {lib_name}")
    except Exception as e:
        print(f"    Uyarı: Kütüphaneler kopyalanamadı: {e}")

    print("\n✓ Linux bundle hazır!")
    return linux_bundle


def main():
    print_header("OCR Dönüştürücü - Tesseract Bundle Hazırlayıcı")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Bundle dizini: {BUNDLE_DIR}")

    # Tessdata'yı indir/hazırla
    setup_tessdata()

    # Platform'a göre Tesseract'ı kopyala
    system = platform.system()

    if system == "Windows":
        copy_system_tesseract_windows()
    elif system == "Darwin":
        copy_system_tesseract_macos()
    elif system == "Linux":
        copy_system_tesseract_linux()
    else:
        print(f"\n!!! Desteklenmeyen platform: {system}")
        return 1

    print_header("TAMAMLANDI")
    print(f"\nBundle dizini: {BUNDLE_DIR}")
    print("\nŞimdi build scriptini çalıştırabilirsiniz:")
    if system == "Windows":
        print("  .\\portable-build\\scripts\\build_windows.bat")
    elif system == "Darwin":
        print("  ./portable-build/scripts/build_macos.sh")
    else:
        print("  ./portable-build/scripts/build_linux.sh")

    return 0


if __name__ == "__main__":
    sys.exit(main())
