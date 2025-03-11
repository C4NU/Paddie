import os
import sys
import platform
import pathlib
from pathlib import Path

from user_config import UserConfig
from resource_path import resource_path

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QDialog, QLabel

UI_INFORMATION = "ui/Information.ui"

try:
    # UI 파일 로드
    ui_path = resource_path(UI_INFORMATION)
    form_class = uic.loadUiType(ui_path)[0]
    
except Exception as e:
    print(f"Resource loading failed: {str(e)}")
    sys.exit(1)

print("UI Loaded Successfully")

class InformationWindow(QDialog, form_class):
	def __init__(self):
		super().__init__()
		
		self.default_font = 'Barlow-Light'
		self.program_name_size = 28
		self.program_version_size = 20

		self.program_name: QLabel
		self.program_version: QLabel

		self.setupUi(self)