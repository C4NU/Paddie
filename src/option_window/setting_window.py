import sys

from user_config import UserConfig
from resource_path import resource_path

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QDialog, QLabel

UI_SETTING = "resources/ui/Settings.ui"

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

        self.language_combo_box: QComboBox # .ui 파일 UI 요소 (이름 동일하게 설정)
        self.language_index = UserConfig.language # 언어 설정 변수
        print(f"언어 인덱스: {self.language_index}")

        self.setupUi(self) # UI 요소 초기화
        self.bind_ui() # 이벤트 핸들러 연결

        self.on_accepted = None

    def bind_ui(self):
        self.language_combo_box.currentIndexChanged.connect(self.on_language_combo_box_index_changed)
        self.language_combo_box.setToolTip("언어를 선택합니다.")

    def on_call(self):
        self.__update_ui()
        self.show()

    def __update_ui(self):
        self.language_index = UserConfig.language
        self.language_combo_box.setCurrentIndex(self.language_index)
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