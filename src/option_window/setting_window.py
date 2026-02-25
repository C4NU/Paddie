import sys

from user_config import UserConfig
from resource_path import resource_path

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QDialog, QLabel

UI_SETTING = "resources/ui/settings.ui"

try:
     # UI 파일 로드
     ui_path = resource_path(UI_SETTING)
     form_class = uic.loadUiType(ui_path)[0]
     
except Exception as e:
     print(f"Resource loading failed: {str(e)}")
     sys.exit(1)

print("SETTING UI Loaded Successfully")

class SettingWindow(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # UI 요소 초기화

        self.language_combo_box: QComboBox # .ui 파일 UI 요소 (이름 동일하게 설정)
        self.language_index = UserConfig.language # 언어 설정 변수
        print(f"언어 인덱스: {self.language_index}")

        self.bind_ui() # 이벤트 핸들러 연결

        self.on_accepted = None
        self.on_config_changed = None

    def bind_ui(self):
        self.language_combo_box.currentIndexChanged.connect(self.on_language_combo_box_index_changed)
        self.language_combo_box.setToolTip("언어를 선택합니다.")
        
        # Add Detached Preview Option programmatically
        from PyQt6.QtWidgets import QCheckBox, QVBoxLayout
        self.detached_preview_checkbox = QCheckBox(self.tr("Use detached preview window"), self)
        self.detached_preview_checkbox.setToolTip(self.tr("Show preview in a separate window instead of resizing the main window."))
        
        # Try to find a layout to add the checkbox
        # If no layout, just position it (simple but hacky)
        # Based on settings.ui structure (typical for these small apps)
        layout = self.findChild(QVBoxLayout)
        if layout:
            layout.addWidget(self.detached_preview_checkbox)
        else:
            # Fallback to absolute positioning if layout not found
            self.detached_preview_checkbox.move(20, 100) # Adjust as needed
            
        self.detached_preview_checkbox.stateChanged.connect(self.on_detached_preview_changed)

    def on_detached_preview_changed(self, state):
        UserConfig.exif_detached_preview = (state == Qt.CheckState.Checked.value)
        if self.on_config_changed:
            self.on_config_changed()

    def retranslateUi(self, widget):
        # Original retranslateUi from .ui file (if it exists)
        # Note: uic loaded class has retranslateUi
        form_class.retranslateUi(self, widget)
        
        # Manually update dynamic elements if they exist
        if hasattr(self, 'detached_preview_checkbox'):
            self.detached_preview_checkbox.setText(self.tr("Use detached preview window"))
            self.detached_preview_checkbox.setToolTip(self.tr("Show preview in a separate window instead of resizing the main window."))
            self.language_combo_box.setToolTip(self.tr("언어를 선택합니다."))

    def on_call(self):
        self.__update_ui()
        self.show()

    def __update_ui(self):
        self.language_index = UserConfig.language
        self.language_combo_box.setCurrentIndex(self.language_index)
        self.detached_preview_checkbox.setChecked(UserConfig.exif_detached_preview)
        print(f"현재 언어 인덱스: {self.language_index}")
    
    def on_language_combo_box_index_changed(self, index):
        self.language_index = index

    def accept(self) -> None:
        if self.on_accepted:
            print(f"현재 인덱스: {self.language_index}")
            UserConfig.language = self.language_index
            UserConfig.save()

            self.on_accepted(self.language_index)
        super().accept()