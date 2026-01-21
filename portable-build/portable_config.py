"""
Portable Configuration Module
Bu modül, uygulamanın portatif çalışması için gerekli yolları belirler
"""

import sys
import os
from pathlib import Path


def get_application_path():
    """
    Uygulamanın çalıştığı dizini al
    PyInstaller ile paketlenmiş veya normal Python ile çalışıyor olabilir
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller ile paketlenmiş
        return Path(sys._MEIPASS)
    else:
        # Normal Python ile çalışıyor
        return Path(__file__).parent.parent


def get_base_path():
    """
    Executable'ın bulunduğu dizini al (kullanıcı dosyaları için)
    """
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent


def get_tesseract_path():
    """
    Gömülü Tesseract executable yolunu al
    """
    import platform

    app_path = get_application_path()
    system = platform.system()

    if system == "Windows":
        tesseract_exe = app_path / "tesseract" / "tesseract.exe"
    elif system == "Darwin":  # macOS
        tesseract_exe = app_path / "tesseract" / "bin" / "tesseract"
    else:  # Linux
        tesseract_exe = app_path / "tesseract" / "bin" / "tesseract"

    if tesseract_exe.exists():
        return str(tesseract_exe)

    # Fallback: sistem Tesseract'ı dene
    import shutil
    system_tesseract = shutil.which("tesseract")
    if system_tesseract:
        return system_tesseract

    return None


def get_tessdata_path():
    """
    Gömülü tessdata dizinini al
    """
    import platform

    app_path = get_application_path()
    system = platform.system()

    # Önce uygulama içindeki tessdata'yı kontrol et
    bundled_tessdata = app_path / "tessdata"
    if bundled_tessdata.exists():
        return str(bundled_tessdata)

    # Windows için alternatif konum
    if system == "Windows":
        alt_tessdata = app_path / "tesseract" / "tessdata"
        if alt_tessdata.exists():
            return str(alt_tessdata)

    # macOS/Linux için alternatif konumlar
    else:
        alt_tessdata = app_path / "tesseract" / "share" / "tessdata"
        if alt_tessdata.exists():
            return str(alt_tessdata)

    # Fallback: sistem tessdata'sı
    possible_paths = [
        "/usr/share/tesseract-ocr/4.00/tessdata",
        "/usr/share/tesseract-ocr/5/tessdata",
        "/usr/share/tessdata",
        "/usr/local/share/tessdata",
        "/opt/homebrew/share/tessdata"
    ]

    for path in possible_paths:
        if Path(path).exists():
            return path

    return None


def setup_environment():
    """
    Portatif çalışma için gerekli ortam değişkenlerini ayarla
    """
    tessdata_path = get_tessdata_path()
    if tessdata_path:
        os.environ['TESSDATA_PREFIX'] = tessdata_path

    # Windows'ta PATH'e Tesseract ekle
    import platform
    if platform.system() == "Windows":
        tesseract_dir = get_application_path() / "tesseract"
        if tesseract_dir.exists():
            os.environ['PATH'] = str(tesseract_dir) + os.pathsep + os.environ.get('PATH', '')


def get_available_languages():
    """
    Mevcut dilleri listele
    """
    tessdata_path = get_tessdata_path()
    if not tessdata_path:
        return ['eng', 'tur']

    tessdata_dir = Path(tessdata_path)
    languages = []

    for file in tessdata_dir.glob("*.traineddata"):
        lang = file.stem
        languages.append(lang)

    return sorted(languages)


# Uygulama başlarken ortamı ayarla
setup_environment()
