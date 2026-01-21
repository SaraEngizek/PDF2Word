@echo off
REM ============================================
REM OCR Dönüştürücü - Windows Portable Build
REM Tesseract gömülü, internet gerektirmeyen
REM ============================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   OCR Donusturucu - Windows Build
echo   Portable Versiyon (Tesseract Gomulu)
echo ========================================
echo.

REM Proje kök dizinine git
cd /d "%~dp0..\.."
set PROJECT_ROOT=%CD%

echo [1/6] Proje dizini: %PROJECT_ROOT%

REM Python kontrolü
echo [2/6] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi!
    echo Lutfen Python 3.8+ yukleyin: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Virtual environment oluştur
echo [3/6] Virtual environment hazirlaniyor...
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat

REM Bağımlılıkları yükle
echo [4/6] Bagimliliklar yukleniyor...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

REM Tesseract bundle hazırla
echo [5/6] Tesseract bundle hazirlaniyor...
set TESSERACT_BUNDLE=%PROJECT_ROOT%\portable-build\tesseract-bundle\windows
set TESSDATA_DIR=%PROJECT_ROOT%\portable-build\tesseract-bundle\tessdata

REM Tesseract bundle yoksa indir
if not exist "%TESSERACT_BUNDLE%\tesseract.exe" (
    echo.
    echo !!! UYARI: Tesseract bundle bulunamadi!
    echo.
    echo Lutfen asagidaki adimlari takip edin:
    echo.
    echo 1. https://github.com/UB-Mannheim/tesseract/wiki adresinden
    echo    tesseract-ocr-w64-setup-*.exe dosyasini indirin
    echo.
    echo 2. Kurulumu yapin veya portable versiyonu cikarin
    echo.
    echo 3. Asagidaki dosyalari kopyalayin:
    echo    - tesseract.exe
    echo    - *.dll dosyalari
    echo    Hedef: %TESSERACT_BUNDLE%\
    echo.
    echo 4. tessdata klasorunu kopyalayin:
    echo    Hedef: %TESSDATA_DIR%\
    echo    ^(En azindan eng.traineddata ve tur.traineddata^)
    echo.
    pause
    exit /b 1
)

REM Tessdata kontrolü
if not exist "%TESSDATA_DIR%\eng.traineddata" (
    echo UYARI: tessdata bulunamadi!
    echo Lutfen tessdata klasorunu %TESSDATA_DIR% dizinine kopyalayin.
    echo En azindan: eng.traineddata, tur.traineddata
    pause
    exit /b 1
)

REM Build işlemi
echo [6/6] PyInstaller ile build yapiliyor...
cd "%PROJECT_ROOT%"

pyinstaller --clean --noconfirm ^
    portable-build\specs\windows_portable.spec

if errorlevel 1 (
    echo HATA: Build basarisiz!
    pause
    exit /b 1
)

REM Başarılı
echo.
echo ========================================
echo   BUILD BASARILI!
echo ========================================
echo.
echo Cikti dosyasi:
echo   %PROJECT_ROOT%\dist\OCR_Donusturucu.exe
echo.
echo Bu dosya tamamen portable:
echo - Tesseract gomulu
echo - Internet gerektirmez
echo - USB'den calisir
echo.

pause
exit /b 0
