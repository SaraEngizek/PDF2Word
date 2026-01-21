"""
PDF Handler Module
Convert PDF pages to images for OCR processing

Uses pdf2image (poppler-based) instead of PyMuPDF for better cross-platform compatibility
CV2 KALDIRILDI - Sadece PIL/numpy kullanılıyor (portable uyumluluk için)

macOS için: Poppler Homebrew'dan kullanılıyor (brew install poppler)
"""

import numpy as np
from pathlib import Path
from typing import List, Tuple, Generator, Optional
import logging
import platform
import os
import sys
import subprocess
import shutil

# pdf2image for PDF to image conversion
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_poppler_path() -> Optional[str]:
    """
    Get poppler path for portable builds
    macOS'ta SIP nedeniyle embedded dylib'ler çalışmıyor
    Bu yüzden sistem poppler'ını kullanıyoruz
    """
    system = platform.system()

    # Önce sistem PATH'inde poppler var mı kontrol et
    pdftoppm_path = shutil.which("pdftoppm")
    if pdftoppm_path:
        poppler_bin = str(Path(pdftoppm_path).parent)
        logger.info(f"System poppler found at: {poppler_bin}")
        return poppler_bin

    # macOS: Homebrew paths
    if system == "Darwin":
        homebrew_paths = [
            "/opt/homebrew/bin",  # Apple Silicon
            "/usr/local/bin",      # Intel Mac
        ]
        for path in homebrew_paths:
            pdftoppm = Path(path) / "pdftoppm"
            if pdftoppm.exists():
                logger.info(f"Homebrew poppler found at: {path}")
                return path

    # Windows: Common installation paths
    if system == "Windows":
        windows_paths = [
            r"C:\Program Files\poppler\bin",
            r"C:\Program Files (x86)\poppler\bin",
            r"C:\poppler\bin",
        ]
        for path in windows_paths:
            if Path(path).exists() and (Path(path) / "pdftoppm.exe").exists():
                logger.info(f"Windows poppler found at: {path}")
                return path

    # Linux: Usually in PATH
    if system == "Linux":
        linux_paths = [
            "/usr/bin",
            "/usr/local/bin",
        ]
        for path in linux_paths:
            if (Path(path) / "pdftoppm").exists():
                logger.info(f"Linux poppler found at: {path}")
                return path

    logger.warning("Poppler not found in system PATH")
    return None


def check_poppler_installed() -> bool:
    """Check if poppler is properly installed and accessible"""
    try:
        result = subprocess.run(
            ["pdftoppm", "-v"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def get_poppler_install_instructions() -> str:
    """Get platform-specific poppler installation instructions"""
    system = platform.system()

    if system == "Darwin":
        return """
Poppler kurulu değil!

macOS için kurulum:
1. Terminal'i açın
2. Homebrew yoksa kurun:
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
3. Poppler kurun:
   brew install poppler
4. Uygulamayı yeniden başlatın
"""
    elif system == "Windows":
        return """
Poppler kurulu değil!

Windows için kurulum:
1. https://github.com/oschwartz10612/poppler-windows/releases adresine gidin
2. En son sürümü indirin (Release-XX.XX.X-X.zip)
3. Zip'i çıkarın (örn: C:\\poppler)
4. bin klasörünü PATH'e ekleyin
5. Uygulamayı yeniden başlatın
"""
    else:
        return """
Poppler kurulu değil!

Linux için kurulum:
Ubuntu/Debian:
  sudo apt-get install poppler-utils

Fedora:
  sudo dnf install poppler-utils

Arch:
  sudo pacman -S poppler

Uygulamayı yeniden başlatın.
"""


class PDFHandler:
    """Handle PDF file operations and page extraction"""

    def __init__(self, dpi: int = 300):
        """
        Initialize PDF Handler

        Args:
            dpi: Resolution for PDF to image conversion (higher = better quality)
        """
        self.dpi = dpi
        self.poppler_path = get_poppler_path()

        # Poppler kontrolü
        if not self.poppler_path and not check_poppler_installed():
            raise RuntimeError(get_poppler_install_instructions())

    def get_page_count(self, pdf_path: str) -> int:
        """
        Get number of pages in PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            Number of pages
        """
        try:
            # Use pdfinfo to get actual page count
            from pdf2image.pdf2image import pdfinfo_from_path
            info = pdfinfo_from_path(pdf_path, poppler_path=self.poppler_path)
            page_count = info.get('Pages', 1)
            return page_count
        except PDFInfoNotInstalledError:
            logger.error("Poppler not installed. Please install poppler-utils.")
            raise RuntimeError(get_poppler_install_instructions())
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {str(e)}")
            raise

    def extract_page_as_image(self, pdf_path: str, page_number: int) -> np.ndarray:
        """
        Extract single PDF page as image

        Args:
            pdf_path: Path to PDF file
            page_number: Page number (0-indexed)

        Returns:
            Page as numpy array (image) - RGB format
        """
        try:
            # pdf2image uses 1-indexed pages
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=page_number + 1,
                last_page=page_number + 1,
                poppler_path=self.poppler_path
            )

            if not images:
                raise ValueError(f"Page {page_number} does not exist")

            # Convert PIL Image to numpy array - keep RGB format
            pil_image = images[0]
            img = np.array(pil_image)

            logger.info(f"Extracted page {page_number + 1} from {pdf_path}")
            return img

        except PDFInfoNotInstalledError:
            logger.error("Poppler not installed")
            raise RuntimeError(get_poppler_install_instructions())
        except Exception as e:
            logger.error(f"Error extracting page {page_number}: {str(e)}")
            raise

    def extract_all_pages(self, pdf_path: str) -> Generator[Tuple[int, np.ndarray], None, None]:
        """
        Extract all pages from PDF as images (generator for memory efficiency)

        Args:
            pdf_path: Path to PDF file

        Yields:
            Tuple of (page_number, image_array) - RGB format
        """
        try:
            # Get total page count first
            total_pages = self.get_page_count(pdf_path)

            # Process one page at a time for memory efficiency
            for page_num in range(total_pages):
                images = convert_from_path(
                    pdf_path,
                    dpi=self.dpi,
                    first_page=page_num + 1,
                    last_page=page_num + 1,
                    poppler_path=self.poppler_path
                )

                if images:
                    pil_image = images[0]
                    img = np.array(pil_image)  # Keep RGB format

                    logger.info(f"Processing page {page_num + 1}/{total_pages}")
                    yield (page_num, img)

        except PDFInfoNotInstalledError:
            logger.error("Poppler not installed")
            raise RuntimeError(get_poppler_install_instructions())
        except Exception as e:
            logger.error(f"Error extracting pages from {pdf_path}: {str(e)}")
            raise

    def check_if_scanned(self, pdf_path: str, sample_pages: int = 3) -> bool:
        """
        Check if PDF is scanned (image-based) or contains searchable text

        Note: pdf2image doesn't extract text directly, so we use a heuristic
        based on file size and page dimensions

        Args:
            pdf_path: Path to PDF file
            sample_pages: Number of pages to sample

        Returns:
            True if scanned (needs OCR), False if already searchable
        """
        try:
            # For pdf2image, we can't easily check text content
            # We'll assume all PDFs need OCR processing
            # A more sophisticated check would require additional libraries like pdfplumber

            logger.info("PDF analysis: Assuming OCR needed (pdf2image mode)")
            return True

        except Exception as e:
            logger.error(f"Error checking PDF type: {str(e)}")
            return True

    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        Get PDF metadata

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with PDF information
        """
        try:
            from pdf2image.pdf2image import pdfinfo_from_path

            info_raw = pdfinfo_from_path(pdf_path, poppler_path=self.poppler_path)

            info = {
                'pages': info_raw.get('Pages', 0),
                'title': info_raw.get('Title', ''),
                'author': info_raw.get('Author', ''),
                'subject': info_raw.get('Subject', ''),
                'creator': info_raw.get('Creator', ''),
                'producer': info_raw.get('Producer', ''),
                'format': info_raw.get('PDF version', ''),
                'encryption': info_raw.get('Encrypted', None),
                'is_scanned': self.check_if_scanned(pdf_path)
            }
            return info
        except PDFInfoNotInstalledError:
            logger.error("Poppler not installed")
            raise RuntimeError(get_poppler_install_instructions())
        except Exception as e:
            logger.error(f"Error getting PDF info: {str(e)}")
            raise


class ImageHandler:
    """Handle image file operations - PIL based"""

    SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.webp']

    @staticmethod
    def load_image(image_path: str) -> np.ndarray:
        """
        Load image from file

        Args:
            image_path: Path to image file

        Returns:
            Image as numpy array (RGB format)
        """
        try:
            pil_img = Image.open(image_path)

            # Convert to RGB if needed
            if pil_img.mode in ('RGBA', 'P'):
                pil_img = pil_img.convert('RGB')
            elif pil_img.mode == 'L':
                pil_img = pil_img.convert('RGB')

            img = np.array(pil_img)

            logger.info(f"Loaded image: {image_path}")
            return img
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {str(e)}")
            raise

    @staticmethod
    def is_supported(file_path: str) -> bool:
        """
        Check if file format is supported

        Args:
            file_path: Path to file

        Returns:
            True if supported
        """
        ext = Path(file_path).suffix.lower()
        return ext in ImageHandler.SUPPORTED_FORMATS or ext == '.pdf'

    @staticmethod
    def get_image_info(image_path: str) -> dict:
        """
        Get image metadata

        Args:
            image_path: Path to image file

        Returns:
            Dictionary with image information
        """
        try:
            pil_img = Image.open(image_path)
            width, height = pil_img.size

            # Get channel count based on mode
            mode_channels = {
                'L': 1,
                'LA': 2,
                'RGB': 3,
                'RGBA': 4,
                'CMYK': 4,
                'P': 1,
            }
            channels = mode_channels.get(pil_img.mode, 3)

            info = {
                'width': width,
                'height': height,
                'channels': channels,
                'format': Path(image_path).suffix.lower(),
                'size_mb': Path(image_path).stat().st_size / (1024 * 1024)
            }
            return info
        except Exception as e:
            logger.error(f"Error getting image info: {str(e)}")
            raise
