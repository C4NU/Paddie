from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QLabel, QVBoxLayout

from ui_loader import translate_ui_text
from user_config import UserConfig


LANGUAGE_LABELS = [
    "Auto",
    "Korean",
    "Japanese",
    "Chinese",
    "English",
]


class SettingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.on_language_changed = None
        self.setFixedSize(320, 120)

        self.language_label = QLabel()
        self.language_combo_box = QComboBox()
        self.language_combo_box.addItems(LANGUAGE_LABELS)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow(self.language_label, self.language_combo_box)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)
        self.setLayout(layout)
        self.retranslate_ui()

    def on_call(self):
        self.language_combo_box.setCurrentIndex(UserConfig.language)
        self.exec()

    def accept(self):
        previous_language = UserConfig.language
        selected_language = self.language_combo_box.currentIndex()
        if selected_language != previous_language:
            if self.on_language_changed:
                self.on_language_changed(selected_language)
            else:
                UserConfig.language = selected_language
                UserConfig.save()

        super().accept()

    def retranslate_ui(self):
        self.setWindowTitle(translate_ui_text("WebPConverter", "Preferences"))
        self.language_label.setText(translate_ui_text("Dialog", "Language"))
        self.language_combo_box.setToolTip(translate_ui_text("Dialog", "Select the language used by Paddie."))

        for index, label in enumerate(LANGUAGE_LABELS):
            self.language_combo_box.setItemText(index, translate_ui_text("Dialog", label))
