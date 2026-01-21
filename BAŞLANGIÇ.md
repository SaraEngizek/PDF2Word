# 🚀 BURADAN BAŞLAYIN

## 📌 Hangi Klasöre Gitmem Gerekiyor?

Projenizde **2 ayrı yöntem** klasörü var:

```
ocr-converter-clean/
├── 🐳 docker-method/      ← Docker kullanacaksanız buraya
└── 🐍 conda-method/       ← Conda kullanacaksanız buraya
```

---

## 🎯 Hangisini Seçmeliyim?

### Kısa Cevap:

**🐳 Docker seçin** - En kolay, her şey dahil!

---

### Detaylı Karşılaştırma:

#### 🐳 Docker Yöntemi

```bash
cd docker-method/
cat README_DOCKER.md  # Detaylı kılavuz oku
```

**Ne zaman seçmeli:**
- ✅ En basit çözüm istiyorsanız
- ✅ Tesseract kurmak istemiyorsanız
- ✅ Tek dosya ile taşımak istiyorsanız
- ✅ Platform bağımsız istiyorsanız

**Boyut:** ~1-2 GB (her şey dahil)

**Adımlar:**
1. `cd docker-method/`
2. `docker build -t ocr-converter:latest .`
3. `./run-docker.sh`

---

#### 🐍 Conda Yöntemi

```bash
cd conda-method/
cat README_CONDA.md  # Detaylı kılavuz oku
```

**Ne zaman seçmeli:**
- ✅ Daha küçük boyut istiyorsanız
- ✅ Kod geliştirmeye devam edecekseniz
- ✅ Native performans istiyorsanız
- ⚠️ Tesseract ayrı kurmaya razısınız

**Boyut:** ~500 MB-1 GB (+ Tesseract ayrı)

**Adımlar:**
1. `cd conda-method/`
2. `./setup-conda.sh`
3. `./run-conda.sh`

---

## 📋 Hızlı Karar Matrisi

| Sorum | Cevabınız | Seçim |
|-------|-----------|-------|
| Tesseract kurmak ister miyim? | Hayır | 🐳 Docker |
| En basit çözüm? | Evet | 🐳 Docker |
| Boyut önemli mi? | Evet | 🐍 Conda |
| Kod değiştirecek miyim? | Evet | 🐍 Conda |
| Şüpheliyim | Ne yapayım? | 🐳 Docker |

---

## 🎓 İlk Adımınız

### Docker İçin:

```bash
cd docker-method/
```

README_DOCKER.md dosyasını açın ve adım adım takip edin.

### Conda İçin:

```bash
cd conda-method/
```

README_CONDA.md dosyasını açın ve adım adım takip edin.

---

## 💡 Önemli Notlar

1. **Her iki yöntem de offline çalışır** (hazırlık aşaması hariç)
2. **Docker daha büyük ama eksiksiz** - Tesseract dahil
3. **Conda daha hafif ama Tesseract ayrı** - Her sistemde kurmalısınız
4. **İkisini de deneyebilirsiniz** - Çakışmazlar

---

## 🆘 Yardım

Her klasörde **kendi README dosyası var**:

- `docker-method/README_DOCKER.md` - Docker için tam kılavuz
- `conda-method/README_CONDA.md` - Conda için tam kılavuz

---

## ✅ Özet

1. Bir yöntem seçin (🐳 Docker önerilir)
2. O klasöre girin
3. README dosyasını okuyun
4. Adımları takip edin
5. OCR'ı kullanın!

**Hepsi bu kadar! 🎉**

---

**Başarılar! 🚀**
