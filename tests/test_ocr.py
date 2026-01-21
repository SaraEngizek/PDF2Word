"""
Test suite for OCR functionality
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.ocr_engine import OCREngine
from utils.pdf_handler import PDFHandler, ImageHandler
from utils.docx_converter import DOCXConverter
from ocr_processor import OCRProcessor


class TestOCREngine:
    """Test OCR Engine functionality"""

    def test_ocr_engine_init(self):
        """Test OCR engine initialization"""
        engine = OCREngine()
        assert engine is not None
        assert engine.current_language == 'tur+eng'

    def test_set_language(self):
        """Test language setting"""
        engine = OCREngine()
        engine.set_language('eng')
        assert engine.current_language == 'eng'

    def test_supported_languages(self):
        """Test supported languages list"""
        engine = OCREngine()
        langs = engine.SUPPORTED_LANGUAGES
        assert 'tur' in langs
        assert 'eng' in langs


class TestPDFHandler:
    """Test PDF Handler functionality"""

    def test_pdf_handler_init(self):
        """Test PDF handler initialization"""
        handler = PDFHandler(dpi=300)
        assert handler.dpi == 300
        assert handler.zoom == 300 / 72

    def test_image_handler_supported_formats(self):
        """Test supported image formats"""
        assert ImageHandler.is_supported('test.pdf')
        assert ImageHandler.is_supported('test.png')
        assert ImageHandler.is_supported('test.jpg')
        assert ImageHandler.is_supported('test.tiff')
        assert not ImageHandler.is_supported('test.xyz')


class TestDOCXConverter:
    """Test DOCX Converter functionality"""

    def test_docx_converter_init(self):
        """Test DOCX converter initialization"""
        converter = DOCXConverter()
        assert converter.default_font == 'Calibri'
        assert converter.default_size == 11


class TestOCRProcessor:
    """Test OCR Processor integration"""

    def test_processor_init(self):
        """Test processor initialization"""
        processor = OCRProcessor()
        assert processor.ocr_engine is not None
        assert processor.docx_converter is not None


def test_integration():
    """Basic integration test"""
    # This is a basic smoke test
    processor = OCRProcessor()
    assert processor is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
