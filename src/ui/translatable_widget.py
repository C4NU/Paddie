from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from .translator import Translator

class TranslatableWidget(QWidget):
    language_changed = pyqtSignal(str)  # 언어 변경 시그널
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.translator = Translator()
        self.translation_keys = {}
        
    def set_translation_key(self, widget, key):
        """위젯의 번역 키를 설정합니다."""
        self.translation_keys[widget] = key
        self._update_widget_text(widget)
        
    def _update_widget_text(self, widget):
        """위젯의 텍스트를 현재 언어로 업데이트합니다."""
        if widget in self.translation_keys:
            key = self.translation_keys[widget]
            if hasattr(widget, 'setText'):
                widget.setText(self.translator.translate(key))
            elif hasattr(widget, 'setTitle'):
                widget.setTitle(self.translator.translate(key))
                
    def update_translations(self):
        """모든 위젯의 번역을 업데이트합니다."""
        for widget in self.translation_keys:
            self._update_widget_text(widget)
        # 언어 변경 시그널 발생
        self.language_changed.emit(self.translator.get_current_language()) 