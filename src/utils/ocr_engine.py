"""
OCR Engine Module - Tesseract Wrapper
Offline OCR processing with multi-language support
CV2 KALDIRILDI - Sadece PIL kullanılıyor (portable uyumluluk için)
"""

import pytesseract
from PIL import Image, ImageFilter, ImageOps
import numpy as np
from typing import Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OCREngine:
    """Tesseract OCR wrapper with preprocessing capabilities"""

    SUPPORTED_LANGUAGES = {
        'tur': 'Türkçe',
        'eng': 'English',
        'deu': 'Deutsch',
        'fra': 'Français',
        'spa': 'Español',
        'ita': 'Italiano',
        'rus': 'Русский',
        'ara': 'العربية',
        'chi_sim': '简体中文',
        'jpn': '日本語'
    }

    def __init__(self, tesseract_cmd: Optional[str] = None, tessdata_dir: Optional[str] = None):
        """
        Initialize OCR Engine

        Args:
            tesseract_cmd: Path to tesseract executable (auto-detected if None)
            tessdata_dir: Path to tessdata directory (auto-detected if None)
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        if tessdata_dir:
            self.tessdata_dir = tessdata_dir
        else:
            self.tessdata_dir = None

        self.current_language = 'tur+eng'  # Default: Turkish + English

    def set_language(self, lang_code: str):
        """Set OCR language"""
        self.current_language = lang_code
        logger.info(f"OCR language set to: {lang_code}")

    def preprocess_image(self, image: Image.Image, enhance: bool = True) -> Image.Image:
        """
        Preprocess image for better OCR accuracy (PIL version)

        Args:
            image: Input PIL Image
            enhance: Apply enhancement techniques

        Returns:
            Preprocessed PIL Image
        """
        # Convert to grayscale
        if image.mode != 'L':
            gray = image.convert('L')
        else:
            gray = image.copy()

        if not enhance:
            return gray

        # Apply mild blur for denoising
        denoised = gray.filter(ImageFilter.MedianFilter(size=3))

        # Auto contrast for better thresholding
        enhanced = ImageOps.autocontrast(denoised)

        return enhanced

    def preprocess_array(self, image_array: np.ndarray, enhance: bool = True) -> Image.Image:
        """
        Preprocess numpy array image (PIL version)

        Args:
            image_array: Input image as numpy array
            enhance: Apply enhancement techniques

        Returns:
            Preprocessed PIL Image
        """
        # Convert numpy array to PIL Image
        if len(image_array.shape) == 3:
            if image_array.shape[2] == 4:
                # RGBA
                pil_image = Image.fromarray(image_array, 'RGBA').convert('RGB')
            else:
                # RGB or BGR
                pil_image = Image.fromarray(image_array)
        else:
            # Grayscale
            pil_image = Image.fromarray(image_array, 'L')

        return self.preprocess_image(pil_image, enhance)

    def extract_text_from_image(
        self,
        image_path: str,
        preprocess: bool = True,
        config: str = '--oem 3 --psm 3'
    ) -> str:
        """
        Extract text from image file

        Args:
            image_path: Path to image file
            preprocess: Apply preprocessing
            config: Tesseract configuration

        Returns:
            Extracted text
        """
        try:
            # Load image with PIL
            image = Image.open(image_path)

            # Convert to RGB if needed
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')

            # Preprocess if requested
            if preprocess:
                image = self.preprocess_image(image)

            # Perform OCR
            custom_config = config
            if self.tessdata_dir:
                custom_config += f' --tessdata-dir "{self.tessdata_dir}"'

            text = pytesseract.image_to_string(
                image,
                lang=self.current_language,
                config=custom_config
            )

            logger.info(f"Successfully extracted text from: {image_path}")
            return text.strip()

        except Exception as e:
            logger.error(f"Error extracting text from {image_path}: {str(e)}")
            raise

    def extract_text_from_array(
        self,
        image_array: np.ndarray,
        preprocess: bool = True,
        config: str = '--oem 3 --psm 3'
    ) -> str:
        """
        Extract text from numpy array (for PDF pages)

        Args:
            image_array: Image as numpy array
            preprocess: Apply preprocessing
            config: Tesseract configuration

        Returns:
            Extracted text
        """
        try:
            # Preprocess if requested
            if preprocess:
                pil_image = self.preprocess_array(image_array)
            else:
                # Convert to PIL without preprocessing
                if len(image_array.shape) == 3:
                    pil_image = Image.fromarray(image_array)
                else:
                    pil_image = Image.fromarray(image_array, 'L')

            # Perform OCR
            custom_config = config
            if self.tessdata_dir:
                custom_config += f' --tessdata-dir "{self.tessdata_dir}"'

            text = pytesseract.image_to_string(
                pil_image,
                lang=self.current_language,
                config=custom_config
            )

            return text.strip()

        except Exception as e:
            logger.error(f"Error extracting text from array: {str(e)}")
            raise

    def get_available_languages(self) -> List[str]:
        """Get list of available Tesseract languages"""
        try:
            langs = pytesseract.get_languages(config='')
            return [lang for lang in langs if lang in self.SUPPORTED_LANGUAGES]
        except Exception as e:
            logger.warning(f"Could not get available languages: {str(e)}")
            return ['eng', 'tur']  # Fallback to defaults

    def detect_orientation(self, image_path: str) -> dict:
        """
        Detect image orientation and rotation angle

        Returns:
            Dict with orientation info (angle, confidence, etc.)
        """
        try:
            image = Image.open(image_path)
            osd = pytesseract.image_to_osd(image)

            # Parse OSD output
            info = {}
            for line in osd.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()

            return info
        except Exception as e:
            logger.warning(f"Could not detect orientation: {str(e)}")
            return {'Rotate': '0', 'Orientation confidence': '0'}
