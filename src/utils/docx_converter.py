"""
DOCX Converter Module
Convert extracted OCR text to formatted Word documents
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path
from typing import List, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DOCXConverter:
    """Convert OCR text to DOCX format with formatting"""

    def __init__(self):
        """Initialize DOCX Converter"""
        self.default_font = 'Calibri'
        self.default_size = 11

    def create_document(
        self,
        text_content: str,
        output_path: str,
        title: Optional[str] = None,
        add_metadata: bool = True
    ) -> str:
        """
        Create simple DOCX document from text

        Args:
            text_content: Text to convert
            output_path: Output file path
            title: Document title
            add_metadata: Add processing metadata

        Returns:
            Path to created document
        """
        try:
            doc = Document()

            # Add title if provided
            if title:
                heading = doc.add_heading(title, 0)
                heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Add metadata
            if add_metadata:
                metadata = doc.add_paragraph()
                metadata.add_run(
                    f"OCR Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                ).italic = True
                metadata.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                doc.add_paragraph()  # Blank line

            # Split text into paragraphs
            paragraphs = text_content.split('\n\n')

            for para_text in paragraphs:
                if para_text.strip():
                    para = doc.add_paragraph(para_text.strip())
                    # Set default font
                    for run in para.runs:
                        run.font.name = self.default_font
                        run.font.size = Pt(self.default_size)

            # Save document
            doc.save(output_path)
            logger.info(f"Document saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error creating document: {str(e)}")
            raise

    def create_multi_page_document(
        self,
        page_texts: List[str],
        output_path: str,
        title: Optional[str] = None,
        add_page_numbers: bool = True,
        add_page_breaks: bool = True
    ) -> str:
        """
        Create DOCX document from multiple pages

        Args:
            page_texts: List of text content for each page
            output_path: Output file path
            title: Document title
            add_page_numbers: Add page number headers
            add_page_breaks: Add page breaks between pages

        Returns:
            Path to created document
        """
        try:
            doc = Document()

            # Add title if provided
            if title:
                heading = doc.add_heading(title, 0)
                heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
                doc.add_paragraph()

            # Process each page
            for page_num, page_text in enumerate(page_texts, 1):
                # Add page number header if requested
                if add_page_numbers:
                    page_header = doc.add_paragraph()
                    run = page_header.add_run(f"[Sayfa {page_num}]")
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(128, 128, 128)
                    page_header.alignment = WD_ALIGN_PARAGRAPH.RIGHT

                # Add page content
                paragraphs = page_text.split('\n\n')
                for para_text in paragraphs:
                    if para_text.strip():
                        para = doc.add_paragraph(para_text.strip())
                        for run in para.runs:
                            run.font.name = self.default_font
                            run.font.size = Pt(self.default_size)

                # Add page break (except for last page)
                if add_page_breaks and page_num < len(page_texts):
                    doc.add_page_break()

            # Save document
            doc.save(output_path)
            logger.info(f"Multi-page document saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error creating multi-page document: {str(e)}")
            raise

    def create_formatted_document(
        self,
        text_content: str,
        output_path: str,
        title: Optional[str] = None,
        font_name: str = 'Calibri',
        font_size: int = 11,
        line_spacing: float = 1.15,
        margins: Optional[dict] = None
    ) -> str:
        """
        Create formatted DOCX document with custom styling

        Args:
            text_content: Text to convert
            output_path: Output file path
            title: Document title
            font_name: Font family
            font_size: Font size in points
            line_spacing: Line spacing multiplier
            margins: Dictionary with top, bottom, left, right margins in inches

        Returns:
            Path to created document
        """
        try:
            doc = Document()

            # Set margins if provided
            if margins:
                sections = doc.sections
                for section in sections:
                    section.top_margin = Inches(margins.get('top', 1))
                    section.bottom_margin = Inches(margins.get('bottom', 1))
                    section.left_margin = Inches(margins.get('left', 1))
                    section.right_margin = Inches(margins.get('right', 1))

            # Add title
            if title:
                heading = doc.add_heading(title, 0)
                heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
                doc.add_paragraph()

            # Add content
            paragraphs = text_content.split('\n\n')

            for para_text in paragraphs:
                if para_text.strip():
                    para = doc.add_paragraph(para_text.strip())

                    # Apply formatting
                    para_format = para.paragraph_format
                    para_format.line_spacing = line_spacing
                    para_format.space_after = Pt(6)

                    for run in para.runs:
                        run.font.name = font_name
                        run.font.size = Pt(font_size)

            # Save document
            doc.save(output_path)
            logger.info(f"Formatted document saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error creating formatted document: {str(e)}")
            raise

    def save_as_txt(self, text_content: str, output_path: str) -> str:
        """
        Save text content as plain TXT file

        Args:
            text_content: Text to save
            output_path: Output file path

        Returns:
            Path to created file
        """
        try:
            # Ensure .txt extension
            if not output_path.endswith('.txt'):
                output_path = output_path.replace('.docx', '.txt')

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text_content)

            logger.info(f"Text file saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error saving text file: {str(e)}")
            raise

    def merge_documents(self, doc_paths: List[str], output_path: str) -> str:
        """
        Merge multiple DOCX documents into one

        Args:
            doc_paths: List of document paths to merge
            output_path: Output file path

        Returns:
            Path to merged document
        """
        try:
            merged_doc = Document()

            for i, doc_path in enumerate(doc_paths):
                sub_doc = Document(doc_path)

                # Copy content
                for element in sub_doc.element.body:
                    merged_doc.element.body.append(element)

                # Add page break (except for last document)
                if i < len(doc_paths) - 1:
                    merged_doc.add_page_break()

            # Save merged document
            merged_doc.save(output_path)
            logger.info(f"Merged document saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error merging documents: {str(e)}")
            raise
