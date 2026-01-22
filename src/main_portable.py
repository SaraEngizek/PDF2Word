#!/usr/bin/env python3
"""
OCR Converter - Portable Main Application Entry Point
Tamamen offline, tüm platformlarda portatif çalışan OCR uygulaması
OpenCV kullanılmıyor - sadece PIL ile çalışıyor
"""

import sys
import os
from pathlib import Path
import logging

# Logging ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_application_path():
    """PyInstaller veya normal çalışma için uygulama yolunu al"""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).parent


def get_base_path():
    """Executable'ın bulunduğu dizini al"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent


def setup_portable_environment():
    """Portatif çalışma için ortamı hazırla"""
    import platform

    app_path = get_application_path()
    system = platform.system()

    # Tessdata yolunu bul ve ayarla
    tessdata_candidates = [
        app_path / "tessdata",
        app_path / "tesseract" / "tessdata",
        app_path / "tesseract" / "share" / "tessdata",
    ]

    for tessdata_path in tessdata_candidates:
        if tessdata_path.exists():
            os.environ['TESSDATA_PREFIX'] = str(tessdata_path)
            logger.info(f"TESSDATA_PREFIX set to: {tessdata_path}")
            break

    # Tesseract executable yolunu bul
    if system == "Windows":
        tesseract_candidates = [
            app_path / "tesseract" / "tesseract.exe",
            app_path / "tesseract.exe",
        ]
    else:
        tesseract_candidates = [
            app_path / "tesseract" / "bin" / "tesseract",
            app_path / "tesseract" / "tesseract",
        ]

    tesseract_cmd = None
    for candidate in tesseract_candidates:
        if candidate.exists():
            tesseract_cmd = str(candidate)
            logger.info(f"Bundled Tesseract found at: {tesseract_cmd}")
            break

    # Windows'ta PATH'e ekle
    if system == "Windows":
        tesseract_dir = app_path / "tesseract"
        if tesseract_dir.exists():
            os.environ['PATH'] = str(tesseract_dir) + os.pathsep + os.environ.get('PATH', '')

        # Poppler'ı da PATH'e ekle
        poppler_dir = app_path / "poppler"
        if poppler_dir.exists():
            os.environ['PATH'] = str(poppler_dir) + os.pathsep + os.environ.get('PATH', '')

    # Linux'ta sistem tesseract'ını kullan (deb paketi ile kurulmuş)
    elif system == "Linux":
        # Sistem tesseract'ı kullanılacak, özel bir ayar gerekmiyor
        logger.info("Linux: Using system tesseract (installed via deb package)")

    # macOS'ta Homebrew PATH'lerini ekle (poppler ve tesseract için)
    elif system == "Darwin":
        homebrew_paths = ["/opt/homebrew/bin", "/usr/local/bin"]
        current_path = os.environ.get('PATH', '')
        for hb_path in homebrew_paths:
            if Path(hb_path).exists() and hb_path not in current_path:
                os.environ['PATH'] = hb_path + os.pathsep + current_path
                current_path = os.environ['PATH']
        logger.info(f"Updated PATH for macOS: {os.environ['PATH'][:100]}...")

    return tesseract_cmd


def find_system_tesseract():
    """Sistem Tesseract'ını bul"""
    import platform
    import shutil

    system = platform.system()

    # shutil.which ile kontrol
    tesseract_path = shutil.which("tesseract")
    if tesseract_path:
        return tesseract_path

    # Platform-özel konumları kontrol et
    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
    elif system == "Darwin":
        possible_paths = [
            "/usr/local/bin/tesseract",
            "/opt/homebrew/bin/tesseract",
        ]
    else:
        possible_paths = [
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract",
        ]

    for path in possible_paths:
        if Path(path).exists():
            return path

    return None


def find_tessdata():
    """Tessdata dizinini bul"""
    import platform

    system = platform.system()

    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tessdata",
            r"C:\Program Files (x86)\Tesseract-OCR\tessdata",
        ]
    elif system == "Darwin":
        possible_paths = [
            "/usr/local/share/tessdata",
            "/opt/homebrew/share/tessdata",
        ]
    else:
        possible_paths = [
            "/usr/share/tesseract-ocr/5/tessdata",
            "/usr/share/tesseract-ocr/4.00/tessdata",
            "/usr/share/tessdata",
        ]

    for path in possible_paths:
        if Path(path).exists():
            return path

    return None


def check_tesseract(tesseract_cmd=None):
    """Tesseract'ın çalışıp çalışmadığını kontrol et"""
    import pytesseract

    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    try:
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
        return True
    except Exception as e:
        logger.error(f"Tesseract check failed: {str(e)}")
        return False


def show_error_dialog(message, parent=None):
    """Hata diyaloğu göster"""
    from PyQt6.QtWidgets import QApplication, QMessageBox

    if not QApplication.instance():
        app = QApplication(sys.argv)

    QMessageBox.critical(parent, "Hata", message)


def show_tesseract_install_guide():
    """Tesseract kurulum kılavuzu göster"""
    import platform

    system = platform.system()

    if system == "Windows":
        guide = """
Tesseract OCR bulunamadı!

Windows için kurulum:
1. https://github.com/UB-Mannheim/tesseract/wiki adresine gidin
2. En son sürümü indirin (tesseract-ocr-w64-setup-*.exe)
3. Kurulumu çalıştırın
4. "Additional language data" bölümünde Türkçe'yi seçin
5. Uygulamayı yeniden başlatın
"""
    elif system == "Darwin":
        guide = """
Tesseract OCR bulunamadı!

macOS için kurulum:
1. Terminal'i açın
2. Homebrew yoksa: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
3. Tesseract kurun: brew install tesseract tesseract-lang
4. Uygulamayı yeniden başlatın
"""
    else:
        guide = """
Tesseract OCR bulunamadı!

Linux için kurulum:
Ubuntu/Debian:
  sudo apt-get install tesseract-ocr tesseract-ocr-tur

Fedora:
  sudo dnf install tesseract tesseract-langpack-tur

Arch:
  sudo pacman -S tesseract tesseract-data-tur

Uygulamayı yeniden başlatın.
"""
    return guide


def main():
    """Ana uygulama giriş noktası"""
    from PyQt6.QtWidgets import QApplication, QMessageBox

    try:
        # QApplication oluştur
        app = QApplication(sys.argv)
        app.setApplicationName("PDF2Word")
        app.setOrganizationName("OCR Converter")
        app.setApplicationVersion("1.0.0")

        # Portatif ortamı hazırla
        bundled_tesseract = setup_portable_environment()

        # Tesseract'ı kontrol et
        tesseract_cmd = bundled_tesseract
        tessdata_dir = os.environ.get('TESSDATA_PREFIX')

        # Gömülü Tesseract yoksa sistem Tesseract'ını dene
        if not tesseract_cmd or not check_tesseract(tesseract_cmd):
            tesseract_cmd = find_system_tesseract()
            if not tessdata_dir:
                tessdata_dir = find_tessdata()

        # Tesseract hala bulunamadıysa hata göster
        if not tesseract_cmd or not check_tesseract(tesseract_cmd):
            guide = show_tesseract_install_guide()
            show_error_dialog(guide)
            sys.exit(1)

        # Türkçe dil paketini kontrol et
        import pytesseract
        try:
            langs = pytesseract.get_languages()
            if 'tur' not in langs:
                QMessageBox.warning(
                    None,
                    "Uyarı",
                    "Türkçe dil paketi bulunamadı.\n\n"
                    "Türkçe OCR için Tesseract Türkçe dil paketini yüklemeniz önerilir.\n\n"
                    "Uygulama çalışacak ancak Türkçe karakter tanıma doğruluğu düşük olabilir."
                )
        except Exception as e:
            logger.warning(f"Could not check language data: {str(e)}")

        # src dizinini path'e ekle
        src_path = get_application_path()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        # Modülleri import et
        from gui.main_window import MainWindow
        from ocr_processor import OCRProcessor

        # OCR Processor başlat
        ocr_processor = OCRProcessor(tesseract_cmd, tessdata_dir)

        # Ana pencereyi oluştur ve göster
        window = MainWindow(ocr_processor)
        window.show()

        # Uygulamayı çalıştır
        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        show_error_dialog(f"Uygulama başlatılırken hata oluştu:\n\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
