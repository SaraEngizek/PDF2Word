# Test Dosyaları

Bu klasör test dosyalarını içerir.

## Test Verilerini Hazırlama

### 1. Örnek Dosyalar Ekleyin

`tests/samples/` klasörüne test dosyalarınızı ekleyin:

```
tests/
├── samples/
│   ├── sample_turkish.pdf       # Türkçe içerikli taranmış PDF
│   ├── sample_english.pdf       # İngilizce içerikli PDF
│   ├── sample_image.png         # Test görseli
│   ├── sample_handwritten.jpg   # El yazısı örneği
│   └── sample_table.tiff        # Tablo içeren görsel
└── test_ocr.py
```

### 2. Test Dosyası Önerileri

**PDF Test Dosyaları:**
- Düşük kalite tarama (150 DPI)
- Normal kalite tarama (300 DPI)
- Yüksek kalite tarama (600 DPI)
- Eğik/çarpık sayfalar
- Renkli ve siyah-beyaz taramalar
- Çok sayfalı belgeler

**Görsel Test Dosyaları:**
- Düz metin
- Karışık metin (başlık, paragraf)
- Tablolar
- El yazısı
- Düşük kontrast
- Gürültülü görüntüler

### 3. Testleri Çalıştırma

```bash
# Birim testler
pytest tests/test_ocr.py -v

# Tüm testler
pytest tests/ -v

# Kapsama raporu ile
pytest tests/ --cov=src --cov-report=html
```

### 4. Manuel Test

```bash
# GUI ile test
python src/main.py

# Test dosyalarını yükleyin ve işleyin
```

## Beklenen Sonuçlar

### Başarılı OCR Kriterleri:

1. **Türkçe Karakterler**: ğ, ü, ş, ı, ö, ç doğru tanınmalı
2. **Noktalama**: Virgül, nokta, soru işareti korunmalı
3. **Paragraf Yapısı**: Satır sonları ve paragraflar doğru olmalı
4. **Sayı Tanıma**: Rakamlar doğru tanınmalı
5. **Format Korunumu**: Başlıklar ve metin ayrımı yapılmalı

### Bilinen Sınırlamalar:

- El yazısı tanıma %70-80 doğruluk
- Çok düşük kalite (<150 DPI) zor
- Eğik metin zorlu olabilir
- Karmaşık tablolar bozulabilir
- Çok küçük fontlar (< 8pt) zor

## Örnek Test Senaryoları

### Senaryo 1: Basit Türkçe Metin
**Giriş:** Türkçe paragraf içeren PDF
**Beklenen:** Tüm Türkçe karakterler doğru, paragraflar korunmuş

### Senaryo 2: İki Sütunlu Sayfa
**Giriş:** Gazete tarzı iki sütunlu PDF
**Beklenen:** Sütunlar tanınmış (sıralama bozuk olabilir)

### Senaryo 3: Tablo İçeren Belge
**Giriş:** Tablo içeren taranmış belge
**Beklenen:** Metin çıkarılmış (tablo formatı kaybolabilir)

### Senaryo 4: Toplu İşlem
**Giriş:** 10 farklı PDF dosyası
**Beklenen:** Hepsi işlenmiş, hata yok

## Performans Testleri

Test ederken şunları ölçün:

1. **İşlem Süresi**:
   - 1 sayfa: ~3-5 saniye
   - 10 sayfa: ~30-50 saniye

2. **Bellek Kullanımı**:
   - Normal: ~200-500 MB
   - Peak: ~1 GB (büyük PDF'ler için)

3. **Doğruluk**:
   - Basılı metin: %95+
   - El yazısı: %70-80
   - Düşük kalite: %80-90

## Hata Durumları

Test edilmesi gereken hata senaryoları:

- ❌ Bozuk PDF dosyası
- ❌ Şifreli PDF
- ❌ Desteklenmeyen format
- ❌ Boş dosya
- ❌ Çok büyük dosya (>100 MB)
- ❌ Disk doluyken kaydetme
- ❌ İzin olmadan yazma

## Test Raporları

Test sonuçlarınızı kaydedin:

```
tests/
├── reports/
│   ├── test_report_2024_01_20.md
│   └── performance_metrics.csv
```

## Katkı

Yeni test senaryoları eklerseniz:
1. Test dosyasını dokumentasyon ile ekleyin
2. Beklenen sonucu açıklayın
3. Bilinen sorunları listeleyin
