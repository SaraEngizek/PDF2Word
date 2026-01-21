"""
OCR Processor - Main processing logic
Coordinates OCR, PDF handling, and DOCX conversion
"""

from pathlib import Path
from typing import Dict, List
import logging

from utils.ocr_engine import OCREngine
from utils.pdf_handler import PDFHandler, ImageHandler
from utils.docx_converter import DOCXConverter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OCRProcessor:
    """Main OCR processing coordinator"""

    def __init__(self, tesseract_cmd=None, tessdata_dir=None):
        """
        Initialize OCR Processor

        Args:
            tesseract_cmd: Path to tesseract executable
            tessdata_dir: Path to tessdata directory
        """
        self.ocr_engine = OCREngine(tesseract_cmd, tessdata_dir)
        self.pdf_handler = None
        self.docx_converter = DOCXConverter()

    def process_file(self, input_path: str, output_dir: str, settings: Dict) -> str:
        """
        Process a single file (PDF or image)

        Args:
            input_path: Path to input file
            output_dir: Directory for output files
            settings: Processing settings dictionary

        Returns:
            Path to output file
        """
        input_file = Path(input_path)
        logger.info(f"Processing file: {input_file.name}")

        # Apply settings
        self.ocr_engine.set_language(settings.get('language', 'tur+eng'))
        dpi = settings.get('dpi', 300)
        self.pdf_handler = PDFHandler(dpi=dpi)

        # Determine file type and process
        if input_file.suffix.lower() == '.pdf':
            return self._process_pdf(input_path, output_dir, settings)
        else:
            return self._process_image(input_path, output_dir, settings)

    def _process_pdf(self, pdf_path: str, output_dir: str, settings: Dict) -> str:
        """Process PDF file"""
        logger.info(f"Processing PDF: {pdf_path}")

        pdf_file = Path(pdf_path)
        output_name = pdf_file.stem

        # Check if PDF needs OCR
        is_scanned = self.pdf_handler.check_if_scanned(pdf_path)
        logger.info(f"PDF is {'scanned' if is_scanned else 'searchable'}")

        if not is_scanned:
            logger.info("PDF already contains searchable text, extracting...")
            # For searchable PDFs, we could extract text directly,
            # but for consistency, we'll still use OCR
            pass

        # Extract pages and perform OCR
        page_texts = []
        preprocess = settings.get('preprocess', True)

        for page_num, page_image in self.pdf_handler.extract_all_pages(pdf_path):
            logger.info(f"OCR on page {page_num + 1}")

            # Perform OCR on page image
            text = self.ocr_engine.extract_text_from_array(
                page_image,
                preprocess=preprocess
            )
            page_texts.append(text)

        # Combine all text
        full_text = '\n\n'.join(page_texts)

        # Save output based on format settings
        output_format = settings.get('output_format', 0)  # 0: DOCX, 1: TXT, 2: Both
        output_paths = []

        if output_format in [0, 2]:  # DOCX or Both
            docx_path = Path(output_dir) / f"{output_name}_ocr.docx"
            self.docx_converter.create_multi_page_document(
                page_texts,
                str(docx_path),
                title=None,  # Başlık ekleme - sadece içerik
                add_page_numbers=settings.get('page_numbers', True)
            )
            output_paths.append(str(docx_path))
            logger.info(f"DOCX saved: {docx_path}")

        if output_format in [1, 2]:  # TXT or Both
            txt_path = Path(output_dir) / f"{output_name}_ocr.txt"
            self.docx_converter.save_as_txt(full_text, str(txt_path))
            output_paths.append(str(txt_path))
            logger.info(f"TXT saved: {txt_path}")

        return output_paths[0] if output_paths else None

    def _process_image(self, image_path: str, output_dir: str, settings: Dict) -> str:
        """Process image file"""
        logger.info(f"Processing image: {image_path}")

        image_file = Path(image_path)
        output_name = image_file.stem

        # Perform OCR
        preprocess = settings.get('preprocess', True)
        text = self.ocr_engine.extract_text_from_image(
            image_path,
            preprocess=preprocess
        )

        # Save output based on format settings
        output_format = settings.get('output_format', 0)
        output_paths = []

        if output_format in [0, 2]:  # DOCX or Both
            docx_path = Path(output_dir) / f"{output_name}_ocr.docx"
            self.docx_converter.create_document(
                text,
                str(docx_path),
                title=None,  # Başlık ekleme - sadece içerik
                add_metadata=False  # Metadata da ekleme
            )
            output_paths.append(str(docx_path))
            logger.info(f"DOCX saved: {docx_path}")

        if output_format in [1, 2]:  # TXT or Both
            txt_path = Path(output_dir) / f"{output_name}_ocr.txt"
            self.docx_converter.save_as_txt(text, str(txt_path))
            output_paths.append(str(txt_path))
            logger.info(f"TXT saved: {txt_path}")

        return output_paths[0] if output_paths else None

    def batch_process(self, file_paths: List[str], output_dir: str, settings: Dict) -> List[str]:
        """
        Process multiple files

        Args:
            file_paths: List of input file paths
            output_dir: Directory for output files
            settings: Processing settings

        Returns:
            List of output file paths
        """
        output_files = []

        for file_path in file_paths:
            try:
                output_path = self.process_file(file_path, output_dir, settings)
                output_files.append(output_path)
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")
                continue

        return output_files

    def get_supported_languages(self) -> List[str]:
        """Get list of available OCR languages"""
        return self.ocr_engine.get_available_languages()
