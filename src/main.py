#!/usr/bin/env python3
"""
OCR Converter - Main Application Entry Point
Cross-platform offline OCR application
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
import logging

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.main_window import MainWindow
from ocr_processor import OCRProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_tesseract():
    """Check if Tesseract is installed and accessible"""
    import pytesseract

    try:
        # Try to get Tesseract version
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
        return True
    except Exception as e:
        logger.error(f"Tesseract not found: {str(e)}")
        return False


def find_tesseract():
    """
    Try to find Tesseract installation
    Returns path to tesseract executable or None
    """
    import platform
    import shutil

    # Try common locations based on OS
    system = platform.system()

    if system == "Windows":
        # Common Windows installation paths
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            Path(__file__).parent.parent / "tesseract" / "tesseract.exe"
        ]

        for path in possible_paths:
            if Path(path).exists():
                return str(path)

    elif system == "Darwin":  # macOS
        # Check if installed via Homebrew
        tesseract_path = shutil.which("tesseract")
        if tesseract_path:
            return tesseract_path

        # Check common macOS locations
        possible_paths = [
            "/usr/local/bin/tesseract",
            "/opt/homebrew/bin/tesseract"
        ]

        for path in possible_paths:
            if Path(path).exists():
                return str(path)

    else:  # Linux
        tesseract_path = shutil.which("tesseract")
        if tesseract_path:
            return tesseract_path

    return None


def find_tessdata():
    """
    Try to find tessdata directory
    Returns path to tessdata directory or None
    """
    import platform

    system = platform.system()

    # First check bundled tessdata
    bundled_tessdata = Path(__file__).parent.parent / "assets" / "tessdata"
    if bundled_tessdata.exists():
        return str(bundled_tessdata)

    # Check system locations
    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tessdata",
            r"C:\Program Files (x86)\Tesseract-OCR\tessdata"
        ]
    elif system == "Darwin":
        possible_paths = [
            "/usr/local/share/tessdata",
            "/opt/homebrew/share/tessdata"
        ]
    else:  # Linux
        possible_paths = [
            "/usr/share/tesseract-ocr/4.00/tessdata",
            "/usr/share/tesseract-ocr/5/tessdata",
            "/usr/share/tessdata"
        ]

    for path in possible_paths:
        if Path(path).exists():
            return str(path)

    return None


def setup_tesseract():
    """Setup Tesseract paths"""
    import pytesseract

    tesseract_cmd = find_tesseract()
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        logger.info(f"Tesseract found at: {tesseract_cmd}")

    tessdata_dir = find_tessdata()
    if tessdata_dir:
        logger.info(f"Tessdata found at: {tessdata_dir}")
        return tesseract_cmd, tessdata_dir

    return tesseract_cmd, None


def show_error_dialog(message):
    """Show error dialog"""
    app = QApplication(sys.argv)
    QMessageBox.critical(None, "Hata", message)
    sys.exit(1)


def main():
    """Main application entry point"""
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("PDF2Word")
        app.setOrganizationName("OCR Converter")

        # Setup Tesseract
        tesseract_cmd, tessdata_dir = setup_tesseract()

        # Check if Tesseract is available
        if not check_tesseract():
            error_msg = (
                "Tesseract OCR motoru bulunamadı!\n\n"
                "Lütfen Tesseract'ı yükleyin:\n\n"
                "Windows: https://github.com/UB-Mannheim/tesseract/wiki\n"
                "macOS: brew install tesseract\n"
                "Linux: sudo apt-get install tesseract-ocr\n\n"
                "Tesseract kurduktan sonra Türkçe dil paketini de yüklemeyi unutmayın:\n"
                "sudo apt-get install tesseract-ocr-tur (Linux)\n"
                "brew install tesseract-lang (macOS)"
            )
            show_error_dialog(error_msg)
            return

        # Check for Turkish language data
        try:
            import pytesseract
            langs = pytesseract.get_languages()
            if 'tur' not in langs:
                logger.warning("Turkish language data not found. OCR may not work correctly for Turkish text.")
                QMessageBox.warning(
                    None,
                    "Uyarı",
                    "Türkçe dil paketi bulunamadı.\n\n"
                    "Türkçe OCR için Tesseract Türkçe dil paketini yüklemeniz önerilir.\n\n"
                    "Uygulama yine de çalışacak ancak Türkçe karakter tanıma doğruluğu düşük olabilir."
                )
        except Exception as e:
            logger.warning(f"Could not check language data: {str(e)}")

        # Initialize OCR Processor
        ocr_processor = OCRProcessor(tesseract_cmd, tessdata_dir)

        # Create and show main window
        window = MainWindow(ocr_processor)
        window.show()

        # Run application
        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        show_error_dialog(f"Uygulama başlatılırken hata oluştu:\n\n{str(e)}")


if __name__ == "__main__":
    main()
