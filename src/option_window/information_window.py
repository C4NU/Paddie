import os
import sys
import platform
import pathlib
from pathlib import Path

from user_config import UserConfig
from resource_path import resource_path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QDialog, QLabel
from ui_loader import load_ui

UI_INFORMATION = "resources/ui/information.ui"
PROGRAM_NAME = "Paddie。"
PROGRAM_VERSION = "V 3.4.1"
PROGRAM_EMAIL = "paddie.application@gmail.com"

try:
     # UI 파일 로드
     ui_path = resource_path(UI_INFORMATION)
     
except Exception as e:
     print(f"Resource loading failed: {str(e)}")
     sys.exit(1)

print("INFORMATION UI Loaded Successfully")

class InformationWindow(QDialog):
	def __init__(self):
		super().__init__()
		
		self.default_font = 'Barlow-Light'
		self.program_name_size = 28
		self.program_version_size = 20

		self.program_name: QLabel
		self.program_version: QLabel

		load_ui(self, ui_path)
		self.program_name.setText(PROGRAM_NAME)
		self.program_version.setText(PROGRAM_VERSION)
		self.program_email.setText(PROGRAM_EMAIL)
