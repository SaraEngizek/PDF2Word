"""
Setup script for OCR Converter
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="ocr-converter",
    version="1.0.0",
    author="OCR Converter Team",
    description="Cross-platform offline OCR application for converting scanned PDFs and images to editable Word documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ocr-converter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.6.0",
        "pytesseract>=0.3.10",
        "PyMuPDF>=1.23.0",
        "opencv-python>=4.8.0",
        "Pillow>=10.0.0",
        "numpy>=1.24.0",
        "python-docx>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ocr-converter=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*", "assets/tessdata/*", "assets/icons/*"],
    },
)
