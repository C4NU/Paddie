import os
import sys
import platform

from PyQt6 import uic
from PyQt6.QtWidgets import QDialogButtonBox, QDialog, QCheckBox, QSpinBox, QPushButton, QComboBox, QPlainTextEdit

if platform.system() == "Windows":
	form = os.path.join(os.getcwd(), "Resources/ExifOptions.ui")
else:
	# build 완료된 exec 에서는 실행이 되지만, 단순 py 로 실행할때는 라이브러리 경로를 참조함
	form = os.path.join(os.path.dirname(sys.executable), "Resources/ExifOptions.ui")

try:
	formClass = uic.loadUiType(form)[0]
except:
	formClass = uic.loadUiType(os.path.join(os.getcwd(), "Resources/ExifOptions.ui"))[0]

class ExifOptionWindow(QDialog, formClass):
	def __init__(self):
		super().__init__()

		# UI 링킹 설정 (EXIF Options)
		self.enable_padding_box: QCheckBox
		self.enable_dark_mode_box: QCheckBox
		self.enable_one_line_box: QCheckBox
		self.enable_square_mode_box: QCheckBox
		self.save_exif_data_box: QCheckBox
		self.save_format_box: QComboBox
		self.open_color_picker_button: QPushButton

		# UI 링킹 설정 (Font Options)
		self.font_combo_box: QComboBox
		self.font_preview_line_edit: QPlainTextEdit

		# 옵션 값 설정 (EXIF)
		self.enable_padding = False
		self.enable_dark_mode = False
		self.enable_one_line = False
		self.enable_square_mode = False
		self.save_exif = False
		self.save_format = None
		
		# 옵션 값 설정 (FONT)
		
		self.show()
		
		def __update_option_info(self):
			self.enable_padding = self.enable_padding_box.isChecked()
			self.enable_dark_mode = self.enable_dark_mode_box.isChecked()
			self.enable_one_line = self.enable_one_line_box.isChecked()
			self.enable_square_mode = self.enable_square_mode_box.isChecked()
			self.save_exif = self.save_exif_data_box.isChecked()
			

