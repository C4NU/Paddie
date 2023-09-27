import os
import sys
import platform
import pathlib

import user_config
from user_config import UserConfig

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QDialog, QLabel

if platform.system() == "Windows":
	form = os.path.join(os.getcwd(), "Resources/Information.ui")
else:
	# build 완료된 exec 에서는 실행이 되지만, 단순 py 로 실행할때는 라이브러리 경로를 참조함
	form = os.path.join(os.path.dirname(sys.executable), "Resources/Information.ui")

try:
	formClass = uic.loadUiType(form)[0]
except:
	formClass = uic.loadUiType(os.path.join(os.getcwd(), "Resources/Information.ui"))[0]

class InformationWindow(QDialog, formClass):
	def __init__(self):
		super().__init__()
		
		self.default_font = 'Barlow-Light'
		self.program_name_size = 28
		self.program_version_size = 20

		self.program_name: QLabel
		self.program_version: QLabel

		self.setupUi(self)