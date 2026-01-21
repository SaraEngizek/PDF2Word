"""
Main GUI Window - PyQt6 Interface
Cross-platform OCR application interface
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QProgressBar, QFileDialog, QTextEdit,
    QGroupBox, QListWidget, QMessageBox, QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QPixmap
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OCRWorker(QThread):
    """Background worker thread for OCR processing"""

    progress = pyqtSignal(int, str)  # Progress percentage and status message
    finished = pyqtSignal(str)  # Output file path
    error = pyqtSignal(str)  # Error message

    def __init__(self, ocr_processor, files, output_dir, settings):
        super().__init__()
        self.ocr_processor = ocr_processor
        self.files = files
        self.output_dir = output_dir
        self.settings = settings
        self._is_running = True

    def run(self):
        """Process OCR in background thread"""
        try:
            total_files = len(self.files)

            for idx, file_path in enumerate(self.files):
                if not self._is_running:
                    break

                file_name = Path(file_path).name
                self.progress.emit(
                    int((idx / total_files) * 100),
                    f"İşleniyor: {file_name}"
                )

                # Process file
                output_path = self.ocr_processor.process_file(
                    file_path,
                    self.output_dir,
                    self.settings
                )

                self.progress.emit(
                    int(((idx + 1) / total_files) * 100),
                    f"Tamamlandı: {file_name}"
                )

            self.finished.emit(self.output_dir)

        except Exception as e:
            logger.error(f"OCR processing error: {str(e)}")
            self.error.emit(str(e))

    def stop(self):
        """Stop the worker thread"""
        self._is_running = False


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self, ocr_processor):
        super().__init__()
        self.ocr_processor = ocr_processor
        self.worker = None
        self.file_list = []

        self.init_ui()

    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("PDF2Word - Offline Optical Character Recognition")
        self.setGeometry(100, 100, 900, 700)

        # Enable drag and drop
        self.setAcceptDrops(True)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("📄 PDF2Word")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("Taranmış PDF ve görselleri düzenlenebilir Word dosyalarına dönüştürün")
        subtitle.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)

        # File selection area
        file_group = QGroupBox("📁 Dosya Seçimi")
        file_layout = QVBoxLayout()

        # Drag & drop label
        self.drop_label = QLabel("Dosyaları buraya sürükleyin\nveya aşağıdaki butona tıklayın")
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #3498db;
                border-radius: 10px;
                padding: 40px;
                background-color: #ecf0f1;
                color: #34495e;
                font-size: 14px;
            }
        """)
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_layout.addWidget(self.drop_label)

        # File selection buttons
        button_layout = QHBoxLayout()
        self.add_files_btn = QPushButton("📄 Dosya Ekle")
        self.add_files_btn.clicked.connect(self.add_files)
        self.add_files_btn.setStyleSheet("padding: 10px; font-size: 13px;")

        self.clear_files_btn = QPushButton("🗑️ Listeyi Temizle")
        self.clear_files_btn.clicked.connect(self.clear_files)
        self.clear_files_btn.setStyleSheet("padding: 10px; font-size: 13px;")

        button_layout.addWidget(self.add_files_btn)
        button_layout.addWidget(self.clear_files_btn)
        file_layout.addLayout(button_layout)

        # File list
        self.file_list_widget = QListWidget()
        self.file_list_widget.setMaximumHeight(120)
        file_layout.addWidget(self.file_list_widget)

        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # Settings area
        settings_group = QGroupBox("⚙️ Ayarlar")
        settings_layout = QVBoxLayout()

        # Language selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Dil:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([
            "Türkçe + İngilizce (tur+eng)",
            "Türkçe (tur)",
            "İngilizce (eng)",
            "Almanca (deu)",
            "Fransızca (fra)",
            "İspanyolca (spa)",
            "İtalyanca (ita)"
        ])
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        settings_layout.addLayout(lang_layout)

        # Output format selection
        format_layout = QHBoxLayout()
        format_label = QLabel("Çıktı Formatı:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Word (.docx)", "Metin (.txt)", "Her İkisi"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        settings_layout.addLayout(format_layout)

        # Processing options
        options_layout = QHBoxLayout()
        self.preprocess_check = QCheckBox("Görüntü İyileştirme")
        self.preprocess_check.setChecked(True)
        self.preprocess_check.setToolTip("Daha iyi OCR sonuçları için görüntü ön işleme uygula")

        self.page_numbers_check = QCheckBox("Sayfa Numaraları Ekle")
        self.page_numbers_check.setChecked(True)

        options_layout.addWidget(self.preprocess_check)
        options_layout.addWidget(self.page_numbers_check)
        options_layout.addStretch()
        settings_layout.addLayout(options_layout)

        # DPI setting
        dpi_layout = QHBoxLayout()
        dpi_label = QLabel("PDF Çözünürlüğü (DPI):")
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(150, 600)
        self.dpi_spin.setValue(300)
        self.dpi_spin.setSingleStep(50)
        self.dpi_spin.setToolTip("Yüksek DPI = Daha iyi kalite, daha yavaş işlem")
        dpi_layout.addWidget(dpi_label)
        dpi_layout.addWidget(self.dpi_spin)
        dpi_layout.addStretch()
        settings_layout.addLayout(dpi_layout)

        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        # Progress area
        progress_group = QGroupBox("📊 İşlem Durumu")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Beklemede...")
        self.status_label.setStyleSheet("color: #7f8c8d;")
        progress_layout.addWidget(self.status_label)

        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)

        # Action buttons
        action_layout = QHBoxLayout()

        self.start_btn = QPushButton("▶️ OCR İşlemini Başlat")
        self.start_btn.clicked.connect(self.start_processing)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.start_btn.setEnabled(False)

        self.cancel_btn = QPushButton("⏹️ İptal Et")
        self.cancel_btn.clicked.connect(self.cancel_processing)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        action_layout.addWidget(self.start_btn)
        action_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(action_layout)

        # Footer
        footer = QLabel("💡 İpucu: PDF ve görselleri (PNG, JPG, TIFF) destekler | Tamamen offline çalışır")
        footer.setStyleSheet("font-size: 10px; color: #95a5a6;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(footer)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.add_files_to_list(files)

    def add_files(self):
        """Open file dialog to add files"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Dosya Seç",
            "",
            "Desteklenen Dosyalar (*.pdf *.png *.jpg *.jpeg *.tiff *.tif *.bmp);;Tüm Dosyalar (*)"
        )
        if files:
            self.add_files_to_list(files)

    def add_files_to_list(self, files):
        """Add files to processing list"""
        for file_path in files:
            if file_path not in self.file_list:
                self.file_list.append(file_path)
                self.file_list_widget.addItem(Path(file_path).name)

        self.start_btn.setEnabled(len(self.file_list) > 0)
        self.drop_label.setText(f"✅ {len(self.file_list)} dosya seçildi")

    def clear_files(self):
        """Clear file list"""
        self.file_list.clear()
        self.file_list_widget.clear()
        self.start_btn.setEnabled(False)
        self.drop_label.setText("Dosyaları buraya sürükleyin\nveya aşağıdaki butona tıklayın")

    def start_processing(self):
        """Start OCR processing"""
        if not self.file_list:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir dosya seçin!")
            return

        # Get output directory
        output_dir = QFileDialog.getExistingDirectory(self, "Çıktı Klasörünü Seçin")
        if not output_dir:
            return

        # Prepare settings
        lang_map = {
            0: 'tur+eng', 1: 'tur', 2: 'eng',
            3: 'deu', 4: 'fra', 5: 'spa', 6: 'ita'
        }
        settings = {
            'language': lang_map[self.lang_combo.currentIndex()],
            'output_format': self.format_combo.currentIndex(),  # 0: DOCX, 1: TXT, 2: Both
            'preprocess': self.preprocess_check.isChecked(),
            'page_numbers': self.page_numbers_check.isChecked(),
            'dpi': self.dpi_spin.value()
        }

        # Disable controls
        self.start_btn.setEnabled(False)
        self.add_files_btn.setEnabled(False)
        self.clear_files_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)

        # Start worker thread
        self.worker = OCRWorker(self.ocr_processor, self.file_list, output_dir, settings)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.processing_finished)
        self.worker.error.connect(self.processing_error)
        self.worker.start()

    def update_progress(self, value, message):
        """Update progress bar and status"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)

    def processing_finished(self, output_dir):
        """Handle processing completion"""
        self.progress_bar.setValue(100)
        self.status_label.setText("✅ İşlem tamamlandı!")

        # Re-enable controls
        self.start_btn.setEnabled(True)
        self.add_files_btn.setEnabled(True)
        self.clear_files_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        QMessageBox.information(
            self,
            "Başarılı",
            f"OCR işlemi tamamlandı!\n\nDosyalar kaydedildi:\n{output_dir}"
        )

        # Clear file list
        self.clear_files()

    def processing_error(self, error_message):
        """Handle processing error"""
        self.status_label.setText("❌ Hata oluştu!")

        # Re-enable controls
        self.start_btn.setEnabled(True)
        self.add_files_btn.setEnabled(True)
        self.clear_files_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        QMessageBox.critical(self, "Hata", f"İşlem sırasında hata oluştu:\n\n{error_message}")

    def cancel_processing(self):
        """Cancel ongoing processing"""
        if self.worker:
            self.worker.stop()
            self.worker.wait()
            self.status_label.setText("⏹️ İşlem iptal edildi")
            self.cancel_btn.setEnabled(False)
            self.start_btn.setEnabled(True)
            self.add_files_btn.setEnabled(True)
            self.clear_files_btn.setEnabled(True)
