from PyQt6.QtWidgets import QMainWindow, QDialog
from PyQt6.uic import loadUi
from .translatable_widget import TranslatableWidget
from .settings_dialog import SettingsDialog

class MainWindow(TranslatableWidget, QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        TranslatableWidget.__init__(self)
        
        # UI 파일 로드
        loadUi("resources/ui/WebPConverterGUI.ui", self)
        
        # 번역 키 설정
        self.set_translation_key(self.conversionGroup, "conversion.title")
        self.set_translation_key(self.qualityLabel, "conversion.quality")
        self.set_translation_key(self.formatLabel, "conversion.format")
        self.set_translation_key(self.preserveExifCheck, "conversion.preserve_exif")
        self.set_translation_key(self.resizeGroup, "resize.title")
        self.set_translation_key(self.widthLabel, "resize.width")
        self.set_translation_key(self.heightLabel, "resize.height")
        self.set_translation_key(self.maintainAspectCheck, "resize.maintain_aspect")
        self.set_translation_key(self.watermarkGroup, "watermark.title")
        self.set_translation_key(self.watermarkTextLabel, "watermark.text")
        self.set_translation_key(self.positionLabel, "watermark.position")
        self.set_translation_key(self.opacityLabel, "watermark.opacity")
        self.set_translation_key(self.exifGroup, "exif.title")
        self.set_translation_key(self.preserveExifCheck, "exif.preserve")
        self.set_translation_key(self.stripExifCheck, "exif.strip")
        
        # 메뉴 액션 연결
        self.actionSettings.triggered.connect(self._show_settings)
        
        # 언어 변경 시그널 연결
        self.language_changed.connect(self._on_language_changed)
        
    def _show_settings(self):
        """설정 다이얼로그를 표시합니다."""
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 설정이 저장되었을 때의 처리
            pass
            
    def _on_language_changed(self, language_code):
        """언어가 변경되었을 때 호출됩니다."""
        # 여기에 언어 변경 시 필요한 추가 처리를 구현합니다.
        pass 