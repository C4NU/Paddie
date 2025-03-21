import os
import sys
import platform

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialogButtonBox, QDialog, QCheckBox, QSpinBox, QPushButton

from user_config import UserConfig
from resource_path import resource_path

UI_CONVERSION_OPTION = "resources/ui/ConversionOptions.ui"

try:
     # UI 파일 로드
     ui_path = resource_path(UI_CONVERSION_OPTION)
     form_class = uic.loadUiType(ui_path)[0]

except Exception as e:
     print(f"Resource loading failed: {str(e)}")
     sys.exit(1)

print("CONVERSION OPTION UI Loaded Successfully")

class WebPOptionWindow(QDialog, form_class):
	def __init__(self):
		super().__init__()

		# UI 링킹 설정
		self.webp_option_button_box: QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
		self.loseless_option_box: QCheckBox
		self.exif_option_box: QCheckBox
		self.icc_profile_option_box: QCheckBox
		self.exact_option_box: QCheckBox

		self.image_quality_spinbox: QSpinBox
		self.open_resize_option_button: QPushButton

		# boolean 옵션 값 설정
		self.loseless_option = False
		self.exif_option = False
		self.icc_profile_option = False
		self.exact_option = False
		self.image_quality_option = 80

		self.setupUi(self)
		self.bind_ui()

	def bind_ui(self):
		self.webp_option_button_box.accepted.connect(self.on_save_close)
		self.webp_option_button_box.rejected.connect(self.on_cancel_close)

		self.loseless_option_box.stateChanged.connect(self.on_toggle_loseless_option)
		self.loseless_option_box.setToolTip("무손실 저장 옵션")

		self.exif_option_box.stateChanged.connect(self.on_toggle_exif_option)
		self.exif_option_box.setToolTip("Exif 저장 옵션")

		self.icc_profile_option_box.stateChanged.connect(self.on_toggle_icc_profile_option)
		self.icc_profile_option_box.setToolTip("ICC Profile 저장 옵션")

		self.exact_option_box.stateChanged.connect(self.on_toggle_exact_option)
		self.exact_option_box.setToolTip("몰?루... 저장 옵션")

		self.image_quality_spinbox.valueChanged.connect(self.on_change_image_quality)
		self.image_quality_spinbox.setToolTip("이미지 품질 저장 옵션\n92 정도가 web에서 사용하기 제일 좋습니다.")

	# DEBUG LOGGER FUNCTIONS
	def debug_log(self, options=int):
		if options == 0:
			print(f"Loseless Option: {self.loseless_option}")
			print(f"Exif Option: {self.exif_option}")
			print(f"Icc Profile Option: {self.icc_profile_option}")
			print(f"Transparent RGB Option : {self.exact_option}")
			print(f"Image Quality : {self.image_quality_option}")
		elif options == 1:
			print(f"Loseless Option: {self.loseless_option}")
		elif options == 2:
			print(f"Exif Option: {self.exif_option}")
		elif options == 3:
			print(f"Icc Profile Option: {self.icc_profile_option}")
		elif options == 4:
			print(f"Transparent RGB Option : {self.exact_option}")
		elif options == 5:
			print(f"Image Quality : {self.image_quality_option}")
		elif options == 6:
			print(f"Backup Loseless Option: {self.backup_loseless_option}")
			print(f"Backup Exif Option: {self.backup_exif_option}")
			print(f"Backup Icc Profile Option: {self.backup_icc_profile_option}")
			print(f"Backup Transparent RGB Option : {self.backup_exact_option}")
			print(f"Backup Image Quality : {self.backup_image_quality_option}")
		else:
			print("Wrong Debug Mode")

	# UI INTERACTION FUNCTIONS
	def on_toggle_loseless_option(self, state):
		self.loseless_option = bool(state == Qt.CheckState.Checked.value)
		self.debug_log(1)

	def on_toggle_exif_option(self, state):
		self.exif_option = bool(state == Qt.CheckState.Checked.value)
		self.debug_log(2)

	def on_toggle_icc_profile_option(self, state):
		self.icc_profile_option = bool(state == Qt.CheckState.Checked.value)
		self.debug_log(3)

	def on_toggle_exact_option(self, state):
		self.exact_option = bool(state == Qt.CheckState.Checked.value)
		self.debug_log(4)

	def on_change_image_quality(self):
		self.image_quality_option = self.image_quality_spinbox.value()
		self.debug_log(5)
	
	def __update_ui(self):
		if self.loseless_option_box.isChecked() != UserConfig.conversion_loseless:
			self.loseless_option_box.toggle()

		if self.exif_option_box.isChecked() != UserConfig.conversion_exif:
			self.exif_option_box.toggle()

		if self.icc_profile_option_box.isChecked() != UserConfig.conversion_icc:
			self.icc_profile_option_box.toggle()

		if self.exact_option_box.isChecked() != UserConfig.conversion_transparent:
			self.exact_option_box.toggle()

		if self.image_quality_spinbox.value() != UserConfig.conversion_quality:
			self.image_quality_spinbox.setValue(UserConfig.conversion_quality)

	def on_call(self):
		self.__update_ui()
		self.show()

	def on_save_close(self):
		self.debug_log(0)

		UserConfig.conversion_loseless = self.loseless_option
		UserConfig.conversion_exif = self.exif_option
		UserConfig.conversion_icc = self.icc_profile_option
		UserConfig.conversion_transparent = self.exact_option
		UserConfig.conversion_quality = self.image_quality_option
		UserConfig.save()

		self.accept()
	
	def on_cancel_close(self):
		self.debug_log(0)
		self.reject()