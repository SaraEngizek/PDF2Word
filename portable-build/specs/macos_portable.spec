# -*- mode: python ; coding: utf-8 -*-
"""
macOS Portable Build Specification
Tesseract ve tessdata gömülü, internet gerektirmeyen build
Intel ve Apple Silicon desteği
pdf2image (poppler) kullanılıyor
OpenCV KALDIRILDI - sadece PIL kullanılıyor
"""

import os
import sys
from pathlib import Path

# Proje kök dizini
project_root = Path(SPECPATH).parent.parent

# Tesseract bundle dizini
tesseract_bundle = project_root / 'portable-build' / 'tesseract-bundle' / 'macos'

# Tessdata dizini
tessdata_dir = project_root / 'portable-build' / 'tesseract-bundle' / 'tessdata'

# Poppler bundle dizini (macOS için)
poppler_bundle = project_root / 'portable-build' / 'poppler-bundle' / 'macos'

block_cipher = None

# Gömülecek dosyaları hazırla
datas = []

# Tessdata varsa ekle
if tessdata_dir.exists():
    datas.append((str(tessdata_dir), 'tessdata'))

# macOS Tesseract bundle varsa ekle
if tesseract_bundle.exists():
    datas.append((str(tesseract_bundle), 'tesseract'))

# macOS Poppler bundle varsa ekle (pdf2image için gerekli)
if poppler_bundle.exists():
    datas.append((str(poppler_bundle), 'poppler'))

# Assets varsa ekle
assets_dir = project_root / 'assets'
if assets_dir.exists():
    datas.append((str(assets_dir), 'assets'))

# Hidden imports - OpenCV YOK, sadece PIL
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
    'numpy.lib',
    'numpy.lib.format',
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFont',
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
    hookspath=[],  # Özel hook yok
    hooksconfig={},
    runtime_hooks=[],  # Runtime hook yok
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'pandas',
        'IPython',
        'jupyter',
        'fitz',
        'PyMuPDF',
        'cv2',  # OpenCV exclude
        'opencv-python',
        'opencv-python-headless',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF2Word',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # UPX kapalı - daha stabil
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
    upx=False,
    upx_exclude=[],
    name='PDF2Word',
)

# macOS App Bundle
app = BUNDLE(
    coll,
    name='PDF2Word.app',
    icon=str(project_root / 'assets' / 'icons' / 'app.icns') if (project_root / 'assets' / 'icons' / 'app.icns').exists() else None,
    bundle_identifier='com.ocrconverter.app',
    info_plist={
        'CFBundleName': 'PDF2Word',
        'CFBundleDisplayName': 'PDF2Word',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.ocrconverter.app',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'CFBundleExecutable': 'PDF2Word',
        'LSMinimumSystemVersion': '10.14.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'PDF Document',
                'CFBundleTypeRole': 'Viewer',
                'LSItemContentTypes': ['com.adobe.pdf'],
            },
            {
                'CFBundleTypeName': 'Image',
                'CFBundleTypeRole': 'Viewer',
                'LSItemContentTypes': ['public.image'],
            },
        ],
    },
)
