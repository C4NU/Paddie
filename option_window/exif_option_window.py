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
		self.exif_option_button_box: QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
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
		self.save_format = 'JPEG'

		self.backup_enable_padding = self.enable_padding
		self.backup_enable_dark_mode = self.enable_dark_mode
		self.backup_enable_one_line = self.enable_one_line
		self.backup_enable_square_mode = self.enable_square_mode
		self.backup_save_exif = self.save_exif
		self.backup_save_format = self.save_format

		# 옵션 값 설정 (FONT)

		# UI 불러오기
		self.setupUi(self)
		self.bind_ui()

	def bind_ui(self):
		self.exif_option_button_box.accepted.connect(self.on_save_close)
		self.exif_option_button_box.rejected.connect(self.on_cancel_close)

		#self.enable_padding_box.stateChanged.connect(self.on_toggle_padding_option)
		#self.enable_padding_box.setToolTip("무손실 저장 옵션")

		#self.enable_dark_mode_box.stateChanged.connect(self.on_toggle_dark_mode_option)
		#self.enable_dark_mode_box.setToolTip("Exif 저장 옵션")

		#self.enable_one_line_box.stateChanged.connect(self.on_toggle_one_line_option)
		#self.enable_one_line_box.setToolTip("ICC Profile 저장 옵션")

		#self.enable_square_mode_box.stateChanged.connect(self.on_toggle_square_mode_option)
		#self.enable_square_mode_box.setToolTip("몰?루... 저장 옵션")

		#self.save_exif_data_box.stateChanged.connect(self.on_)
		#self.save_exif_data_box.setToolTip("이미지 품질 저장 옵션 \n 92 정도가 web에서 사용하기 제일 좋습니다.")

	# DEBUG LOGGER FUNCTIONS
	def debug_log(self, options=int):
		if options == 0:
			print(f"Padding Option: {self.enable_padding}")
			print(f"Exif Option: {self.enable_dark_mode}")
			print(f"One line Option: {self.enable_one_line}")
			print(f"Square Option: {self.enable_square_mode}")
			print(f"Save Exif Option: {self.save_exif}")
			print(f"Save Format: {self.save_format}")
		elif options == 1:
			print(f"Padding Option: {self.enable_padding}")
		elif options == 2:
			print(f"Exif Option: {self.enable_dark_mode}")
		elif options == 3:
			print(f"One line Option: {self.enable_one_line}")
		elif options == 4:
			print(f"Square Option: {self.enable_square_mode}")
		elif options == 5:
			print(f"Save Exif Option: {self.save_exif}")
		elif options == 6:
			print(f"Save Format: {self.save_format}")
		elif options == 99:
			print(f"Backup Padding Option: {self.backup_enable_padding}")
			print(f"Backup Exif Option: {self.backup_enable_dark_mode}")
			print(f"Backup One line Option: {self.backup_enable_one_line}")
			print(f"Backup Square Option: {self.backup_enable_square_mode}")
			print(f"Backup Save Exif Option: {self.backup_save_exif}")
			print(f"Backup Save Format: {self.backup_save_format}")
		else:
			print("Wrong Debug Mode")

	def __update_ui(self):
		if self.loseless_option_box.isChecked() != self.loseless_option:
			self.loseless_option_box.toggle()

		if self.exif_option_box.isChecked() != self.exif_option:
			self.exif_option_box.toggle()

		if self.icc_profile_option_box.isChecked() != self.icc_profile_option:
			self.icc_profile_option_box.toggle()

		if self.exact_option_box.isChecked() != self.exact_option:
			self.exact_option_box.toggle()

		if self.image_quality_spinbox.value() != self.image_quality_option:
			self.image_quality_spinbox.setValue(self.image_quality_option)

	def on_call(self):
		self.__update_ui()
		self.show()

	def on_save_close(self):
		self.backup_enable_padding = self.enable_padding
		self.backup_enable_dark_mode = self.enable_dark_mode
		self.backup_enable_one_line = self.enable_one_line
		self.backup_enable_square_mode = self.enable_square_mode
		self.backup_save_exif = self.save_exif
		self.backup_save_format = self.save_format
		self.debug_log(0)
	
	def on_cancel_close(self):
		self.enable_padding = self.backup_enable_padding
		self.enable_dark_mode = self.backup_enable_dark_mode
		self.enable_one_line = self.backup_enable_one_line
		self.enable_square_mode = self.backup_enable_square_mode
		self.save_exif = self.backup_save_exif
		self.save_format = self.backup_save_format
		self.debug_log(0)