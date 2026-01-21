# Runtime hook for cv2 - config.py dosyalarını oluşturur
# Bu hook uygulama başlamadan ÖNCE çalışır
import sys
import os

def setup_cv2():
    """cv2 config dosyalarını oluştur"""
    if not getattr(sys, 'frozen', False):
        return

    try:
        bundle_dir = sys._MEIPASS
        cv2_dir = os.path.join(bundle_dir, 'cv2')

        if not os.path.isdir(cv2_dir):
            # cv2 dizini yoksa oluştur
            try:
                os.makedirs(cv2_dir, exist_ok=True)
            except:
                return

        # Config dosyalarını oluştur
        config_content = 'BINARIES_PATHS = []\n'

        for cfg_name in ['config.py', 'config-3.py', 'config-3.10.py',
                         'config-3.11.py', 'config-3.12.py', 'config-3.13.py']:
            cfg_path = os.path.join(cv2_dir, cfg_name)
            if not os.path.exists(cfg_path):
                try:
                    with open(cfg_path, 'w') as f:
                        f.write(config_content)
                except:
                    pass

        # __init__.py yoksa oluştur
        init_path = os.path.join(cv2_dir, '__init__.py')
        if not os.path.exists(init_path):
            try:
                with open(init_path, 'w') as f:
                    f.write('# cv2 package init\n')
                    f.write('from cv2 import *\n')
            except:
                pass

    except Exception:
        pass

# Hook'u çalıştır
setup_cv2()
