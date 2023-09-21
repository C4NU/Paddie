import os
import sys
import platform

from PyQt6 import uic
from PyQt6.QtWidgets import QDialogButtonBox, QDialog, QCheckBox, QSpinBox, QPushButton

if platform.system() == "Windows":
	form = os.path.join(os.getcwd(), "Resources/ConversionOptions.ui")
else:
	# build 완료된 exec 에서는 실행이 되지만, 단순 py 로 실행할때는 라이브러리 경로를 참조함
	form = os.path.join(os.path.dirname(sys.executable), "Resources/ConversionOptions.ui")

try:
	formClass = uic.loadUiType(form)[0]
except:
	formClass = uic.loadUiType(os.path.join(os.getcwd(), "Resources/ConversionOptions.ui"))[0]

class WebPOptionWindow(QDialog, formClass):
	def __init__(self):
		super().__init__()

		# UI 링킹 설정
		self.webp_option_button_box: QDialogButtonBox
		self.loseless_option_box: QCheckBox
		self.exif_option_box: QCheckBox
		self.icc_profile_option_box: QCheckBox
		self.exact_option_box: QCheckBox

		self.image_quality_spinbox: QSpinBox
		self.open_resize_option_button: QPushButton
		self.setupUi(self)
		
		# boolean 옵션 값 설정
		self.conversion_option = True  # webp 변환하는지 선택
		self.loseless_option = False
		self.image_quality_option = 80
		self.exif_option = False
		self.icc_profile_option = False
		self.exact_option = False

	def __update_option_info(self):
		self.loseless_option = self.loseless_option.isChecked()
		self.exif_option = self.exact_option_box.isChecked()
		self.icc_profile_option = self.icc_profile_option_box.isChecked()
		self.exact_option = self.exact_option_box.isChecked()

		self.image_quality_option = int(self.image_quality_spinbox.value())