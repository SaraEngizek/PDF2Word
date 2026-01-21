# -*- mode: python ; coding: utf-8 -*-
"""
Linux Portable Build Specification - PDF2Word
Tesseract ve tessdata gömülü, internet gerektirmeyen build
AppImage formatında çıktı için optimize edilmiş
pdf2image (poppler) kullanılıyor
OpenCV KALDIRILDI - sadece PIL kullanılıyor
"""

import os
import sys
from pathlib import Path

# Proje kök dizini
project_root = Path(SPECPATH).parent.parent

# Tesseract bundle dizini
tesseract_bundle = project_root / 'portable-build' / 'tesseract-bundle' / 'linux'

# Tessdata dizini
tessdata_dir = project_root / 'portable-build' / 'tesseract-bundle' / 'tessdata'

# Poppler bundle dizini (Linux için)
poppler_bundle = project_root / 'portable-build' / 'poppler-bundle' / 'linux'

block_cipher = None

# Gömülecek dosyaları hazırla
datas = [
    # Tessdata dil dosyaları
    (str(tessdata_dir), 'tessdata'),
]

# Linux Tesseract bundle varsa ekle
if tesseract_bundle.exists():
    datas.append((str(tesseract_bundle), 'tesseract'))

# Linux Poppler bundle varsa ekle (pdf2image için gerekli)
if poppler_bundle.exists():
    datas.append((str(poppler_bundle), 'poppler'))

# Assets varsa ekle
assets_dir = project_root / 'assets'
if assets_dir.exists():
    datas.append((str(assets_dir), 'assets'))

# Hidden imports - OpenCV YOK
hiddenimports = [
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'pytesseract',
    'numpy',
    'numpy.core',
    'numpy.core._methods',
    'numpy.core._multiarray_umath',
    'PIL',
    'PIL.Image',
    'PIL.ImageFilter',
    'PIL.ImageOps',
    'pdf2image',
    'pdf2image.pdf2image',
    'pdf2image.exceptions',
    'docx',
    'docx.shared',
    'docx.enum.text',
]

a = Analysis(
    [str(project_root / 'src' / 'main_portable.py')],
    pathex=[str(project_root / 'src')],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'pandas',
        'IPython',
        'jupyter',
        'fitz',
        'PyMuPDF',
        'cv2',
        'opencv-python',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Linux executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF2Word',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF2Word_Linux',
)
