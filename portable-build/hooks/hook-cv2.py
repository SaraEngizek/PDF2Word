# Minimal cv2 hook - subprocess crash'i önlemek için
# collect_dynamic_libs ve collect_data_files KULLANILMIYOR
# Bu fonksiyonlar cv2 import ederken subprocess açıyor ve Killed: 9 hatası veriyor

# Boş tutarak PyInstaller'ın default cv2 hook'unu override ediyoruz
# cv2 zaten hiddenimports ile ekleniyor

hiddenimports = []
datas = []
binaries = []
