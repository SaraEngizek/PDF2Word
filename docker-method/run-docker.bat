@echo off
REM Docker ile OCR Converter Otomatik Çalıştırma - Windows

echo ========================================
echo OCR Converter - Docker Yöntemi
echo ========================================
echo.

REM Input/output klasörleri kontrol et
if not exist "input\" (
    echo [Bilgi] input\ klasörü oluşturuluyor...
    mkdir input
    echo    Dosyalarınızı input\ klasörüne koyun
)

if not exist "output\" (
    echo [Bilgi] output\ klasörü oluşturuluyor...
    mkdir output
)

REM Image kontrol et
echo.
echo Docker image kontrol ediliyor...
docker images | findstr "ocr-converter" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Image bulundu
) else (
    echo [HATA] Image bulunamadı!
    echo.
    echo Lütfen önce image'i yükleyin:
    echo   docker load ^< ocr-converter-docker-image.tar.gz
    echo.
    echo Veya build edin:
    echo   docker build -t ocr-converter:latest .
    pause
    exit /b 1
)

REM GUI mi yoksa CLI mi?
echo.
echo Nasıl çalıştırmak istersiniz?
echo 1) GUI (Grafik Arayüz)
echo 2) CLI (Komut Satırı - input\ klasöründeki dosyaları işle)
set /p choice="Seçiminiz (1/2): "

if "%choice%"=="1" (
    echo.
    echo [Bilgi] GUI modu başlatılıyor...
    echo    Not: Windows'ta GUI sınırlı olabilir

    docker run --rm ^
        -v %cd%\input:/app/input ^
        -v %cd%\output:/app/output ^
        --network none ^
        ocr-converter:latest

) else if "%choice%"=="2" (
    echo.
    echo [Bilgi] CLI modu başlatılıyor...
    echo    input\ klasöründeki dosyalar işlenecek

    REM Input klasöründe dosya var mı kontrol et
    dir /b input\* >nul 2>&1
    if %errorlevel% neq 0 (
        echo [HATA] input\ klasörü boş!
        echo    Lütfen işlemek istediğiniz PDF/görsel dosyalarını input\ klasörüne koyun
        pause
        exit /b 1
    )

    docker run --rm ^
        -v %cd%\input:/app/input ^
        -v %cd%\output:/app/output ^
        --network none ^
        ocr-converter:latest ^
        python src/ocr_processor.py --input /app/input --output /app/output

) else (
    echo [HATA] Geçersiz seçim
    pause
    exit /b 1
)

echo.
echo ========================================
echo [BAŞARILI] İşlem tamamlandı!
echo [Bilgi] Sonuçlar output\ klasöründe
echo ========================================
pause
