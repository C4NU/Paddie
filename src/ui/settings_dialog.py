from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
from .translatable_widget import TranslatableWidget
from .translator import Translator

class SettingsDialog(TranslatableWidget, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        TranslatableWidget.__init__(self)
        
        # UI 파일 로드
        loadUi("resources/ui/Settings.ui", self)
        
        # 번역 키 설정
        self.set_translation_key(self.groupBox, "settings.title")
        self.set_translation_key(self.label, "settings.language")
        
        # 언어 변경 시그널 연결
        self.language_combo_box.currentTextChanged.connect(self._on_language_changed)
        
        # 현재 언어 설정
        self._update_language_combo()
        
    def _update_language_combo(self):
        """언어 콤보 박스의 현재 선택을 업데이트합니다."""
        current_lang = self.translator.get_current_language()
        lang_map = {
            "en": "English",
            "ko": "Korean",
            "ja": "Japanese"
        }
        current_text = lang_map.get(current_lang, "English")
        self.language_combo_box.setCurrentText(current_text)
        
    def _on_language_changed(self, language):
        """언어가 변경되었을 때 호출됩니다."""
        lang_map = {
            "English": "en",
            "Korean": "ko",
            "Japanese": "ja"
        }
        lang_code = lang_map.get(language, "en")
        if self.translator.set_language(lang_code):
            self.update_translations()
            # 여기에 언어 변경 이벤트를 발생시키는 코드 추가 