from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from localization import get_current_language_code
from resource_path import resource_path


PROGRAM_NAME = "Paddie。"
PROGRAM_VERSION = "3.4.1"
PROGRAM_EMAIL = "paddie.application@gmail.com"
PROGRAM_ICON = "resources/icons/icon.icns"
PROGRAM_LICENSE = "Unspecified"

LOCALIZED_TEXT = {
    "en": {
        "title": "Information",
        "tagline": (
            "A compact desktop tool for WebP conversion "
            "and EXIF frame output."
        ),
        "version": "Version",
        "contact": "Contact",
        "runtime": "Runtime",
        "runtime_value": "Python + PySide6",
        "license": "License",
        "license_value": PROGRAM_LICENSE,
        "close": "Close",
    },
    "ko": {
        "title": "정보",
        "tagline": "WebP 변환과 EXIF 프레임 출력 도구.",
        "version": "버전",
        "contact": "연락처",
        "runtime": "런타임",
        "runtime_value": "Python + PySide6",
        "license": "라이선스",
        "license_value": "별도 명시 없음",
        "close": "닫기",
    },
}


print("INFORMATION UI Loaded Successfully")


class InformationWindow(QDialog):
    def __init__(self):
        """Create the information dialog."""
        super().__init__()
        self.setObjectName("informationDialog")
        self.setFixedSize(480, 320)
        self.setSizeGripEnabled(False)

        self.icon_label = QLabel()
        self.icon_label.setObjectName("appIcon")
        self.icon_label.setFixedSize(72, 72)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        app_icon = QIcon(resource_path(PROGRAM_ICON))
        icon_pixmap = app_icon.pixmap(64, 64)
        if not icon_pixmap.isNull():
            self.icon_label.setPixmap(icon_pixmap)

        self.program_name = QLabel()
        self.program_name.setObjectName("programName")

        self.tagline_label = QLabel()
        self.tagline_label.setObjectName("tagline")
        self.tagline_label.setWordWrap(True)

        self.version_badge = QLabel()
        self.version_badge.setObjectName("versionBadge")
        self.version_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_text_layout = QVBoxLayout()
        header_text_layout.setContentsMargins(0, 0, 0, 0)
        header_text_layout.setSpacing(6)
        header_text_layout.addWidget(self.program_name)
        header_text_layout.addWidget(self.tagline_label)
        header_text_layout.addWidget(
            self.version_badge,
            0,
            Qt.AlignmentFlag.AlignLeft,
        )

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(18)
        header_layout.addWidget(self.icon_label)
        header_layout.addLayout(header_text_layout, 1)

        self.info_panel = QFrame()
        self.info_panel.setObjectName("infoPanel")

        self.version_label = QLabel()
        self.version_value = QLabel()
        self.contact_label = QLabel()
        self.contact_value = QLabel()
        self.runtime_label = QLabel()
        self.runtime_value = QLabel()
        self.license_label = QLabel()
        self.license_value = QLabel()

        for label in (
            self.version_label,
            self.contact_label,
            self.runtime_label,
            self.license_label,
        ):
            label.setObjectName("metaLabel")

        for label in (
            self.version_value,
            self.contact_value,
            self.runtime_value,
            self.license_value,
        ):
            label.setObjectName("metaValue")

        self.contact_value.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
        )

        panel_layout = QGridLayout()
        panel_layout.setContentsMargins(18, 14, 18, 14)
        panel_layout.setHorizontalSpacing(18)
        panel_layout.setVerticalSpacing(10)
        panel_layout.addWidget(self.version_label, 0, 0)
        panel_layout.addWidget(self.version_value, 0, 1)
        panel_layout.addWidget(self.contact_label, 1, 0)
        panel_layout.addWidget(self.contact_value, 1, 1)
        panel_layout.addWidget(self.runtime_label, 2, 0)
        panel_layout.addWidget(self.runtime_value, 2, 1)
        panel_layout.addWidget(self.license_label, 3, 0)
        panel_layout.addWidget(self.license_value, 3, 1)
        panel_layout.setColumnStretch(1, 1)
        self.info_panel.setLayout(panel_layout)

        self.close_button = QPushButton()
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.close)

        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.addStretch(1)
        footer_layout.addWidget(self.close_button)

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(24, 22, 24, 20)
        root_layout.setSpacing(18)
        root_layout.addLayout(header_layout)
        root_layout.addWidget(self.info_panel)
        root_layout.addLayout(footer_layout)
        self.setLayout(root_layout)

        self.setStyleSheet(
            """
            QDialog#informationDialog {
                background: #17181b;
                color: #f4f1eb;
            }
            QLabel#appIcon {
                background: #f7f4ee;
                border: 1px solid #e7dfd0;
                border-radius: 8px;
            }
            QLabel#programName {
                color: #fbf7ef;
                font-size: 34px;
                font-weight: 650;
            }
            QLabel#tagline {
                color: #b9c2c8;
                font-size: 13px;
                line-height: 18px;
            }
            QLabel#versionBadge {
                background: #e9b44c;
                border-radius: 8px;
                color: #17181b;
                font-size: 12px;
                font-weight: 700;
                padding: 5px 10px;
            }
            QFrame#infoPanel {
                background: #222429;
                border: 1px solid #343941;
                border-radius: 8px;
            }
            QLabel#metaLabel {
                color: #8fa0aa;
                font-size: 12px;
                font-weight: 650;
            }
            QLabel#metaValue {
                color: #f1ede6;
                font-size: 13px;
            }
            QPushButton#closeButton {
                background: #2c7da0;
                border: 0;
                border-radius: 7px;
                color: #ffffff;
                font-size: 13px;
                font-weight: 650;
                min-width: 82px;
                padding: 8px 14px;
            }
            QPushButton#closeButton:hover {
                background: #348eb5;
            }
            QPushButton#closeButton:pressed {
                background: #246a88;
            }
            """
        )

        self.retranslate_ui()

    def retranslate_ui(self):
        text = self._localized_text()

        self.setWindowTitle(text["title"])
        self.program_name.setText(PROGRAM_NAME)
        self.tagline_label.setText(text["tagline"])
        self.version_badge.setText(f"{text['version']} {PROGRAM_VERSION}")
        self.version_label.setText(text["version"])
        self.version_value.setText(PROGRAM_VERSION)
        self.contact_label.setText(text["contact"])
        self.contact_value.setText(PROGRAM_EMAIL)
        self.runtime_label.setText(text["runtime"])
        self.runtime_value.setText(text["runtime_value"])
        self.license_label.setText(text["license"])
        self.license_value.setText(text["license_value"])
        self.close_button.setText(text["close"])

    def _localized_text(self):
        language_code = get_current_language_code()
        return LOCALIZED_TEXT.get(language_code, LOCALIZED_TEXT["en"])
