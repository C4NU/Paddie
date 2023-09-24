import os
import sys
import platform
import pathlib

import user_config

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QDialogButtonBox, QDialog, QCheckBox, QSpinBox, QPushButton, QComboBox, QPlainTextEdit, QColorDialog

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
		self.save_format_index = 0	# 0: JPEG, 1: PNG, 2: WebP

		self.backup_enable_padding = self.enable_padding
		self.backup_enable_dark_mode = self.enable_dark_mode
		self.backup_enable_one_line = self.enable_one_line
		self.backup_enable_square_mode = self.enable_square_mode
		self.backup_save_exif = self.save_exif
		self.backup_save_format_index = self.save_format_index

		# 옵션 값 설정 (FONT)

		# UI 불러오기
		self.setupUi(self)
		self.bind_ui()
		self.setup_ui_internal()

	def bind_ui(self):
		self.exif_option_button_box.accepted.connect(self.on_save_close)
		self.exif_option_button_box.rejected.connect(self.on_cancel_close)

		self.enable_padding_box.stateChanged.connect(self.on_toggle_padding_option)
		self.enable_padding_box.setToolTip("프레임 생성 옵션")

		self.enable_dark_mode_box.stateChanged.connect(self.on_toggle_dark_mode_option)
		self.enable_dark_mode_box.setToolTip("폰트 색상 지정 옵션")

		self.enable_one_line_box.stateChanged.connect(self.on_toggle_one_line_option)
		self.enable_one_line_box.setToolTip("1줄 저장 옵션")

		self.enable_square_mode_box.stateChanged.connect(self.on_toggle_square_mode_option)
		self.enable_square_mode_box.setToolTip("1:1 비율 저장 옵션")

		self.save_exif_data_box.stateChanged.connect(self.on_toggle_save_exif_data_option)
		self.save_exif_data_box.setToolTip("EXIF 저장 옵션")

		self.save_format_box.currentIndexChanged.connect(self.on_change_save_format)
		self.save_format_box.setToolTip("이미지 확장자 선택 옵션")

	def setup_ui_internal(self):
		if platform.system() == "Windows":
			font_asset_path = os.path.join(os.getcwd(), "Resources/Fonts")
		else:
			font_asset_path = os.path.join(os.path.dirname(sys.executable), "Resources/Fonts")

		print(f"Font_asset: {font_asset_path}")
		fonts = pathlib.Path(font_asset_path)
		print(f"Fonts: {fonts}")

		try:
			for item in fonts.iterdir():
				if item.is_file():
					continue

				for font_item in os.listdir(item):
					print(f"Fonts Item: {font_item}")
					self.__add_font_combobox(item, font_item)
		except:
			# py 형식으로 실행할 때 macOS 오류 처리용 경로 설정
			fonts = pathlib.Path(os.path.join(os.getcwd(), "Resources/Fonts"))
			for item in fonts.iterdir():
				if item.is_file():
					continue

				for font_item in os.listdir(item):
					self.__add_font_combobox(item, font_item)

	def __add_font_combobox(self, dir_path, file_name):
		font_name = os.path.splitext(file_name)[0]
		item_ext = os.path.splitext(file_name)[1][1:]
		if item_ext != 'ttf':
			return
		fullpath = os.path.join(dir_path, file_name)
		self.font_combo_box.addItem(font_name, userData=fullpath)

	# DEBUG LOGGER FUNCTIONS
	def debug_log(self, options=int):
		if options == 0:
			print(f"Padding Option: {self.enable_padding}")
			print(f"Exif Option: {self.enable_dark_mode}")
			print(f"One line Option: {self.enable_one_line}")
			print(f"Square Option: {self.enable_square_mode}")
			print(f"Save Exif Option: {self.save_exif}")
			print(f"Save Format: {self.save_format_index}")
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
			print(f"Save Format: {self.save_format_index}")
		elif options == 99:
			print(f"Backup Padding Option: {self.backup_enable_padding}")
			print(f"Backup Exif Option: {self.backup_enable_dark_mode}")
			print(f"Backup One line Option: {self.backup_enable_one_line}")
			print(f"Backup Square Option: {self.backup_enable_square_mode}")
			print(f"Backup Save Exif Option: {self.backup_save_exif}")
			print(f"Backup Save Format: {self.backup_save_format_index}")
		else:
			print("Wrong Debug Mode")

	def __update_ui(self):
		if self.enable_padding_box.isChecked() != self.enable_padding:
			self.enable_padding_box.toggle()

		if self.enable_dark_mode_box.isChecked() != self.enable_dark_mode:
			self.enable_dark_mode_box.toggle()

		if self.enable_one_line_box.isChecked() != self.enable_one_line:
			self.enable_one_line_box.toggle()

		if self.enable_square_mode_box.isChecked() != self.enable_square_mode:
			self.enable_square_mode_box.toggle()

		def __update_font_preview(self):
			font_id = QFontDatabase.addApplicationFont(self.__selected_font)
			font_file_name = os.path.basename(self.__selected_font)
			if font_id > 0:
				families = QFontDatabase.applicationFontFamilies(font_id)
				styles = QFontDatabase.styles(families[0])
				style = None
				for item in styles:
					if item in font_file_name:
						style = item

				if style:
					font = QFontDatabase.font(families[0], style, self.__font_preview_size)
					self.font_preview_line_edit.setFont(font)
				else:
					self.font_preview_line_edit.setFont(QFont(families[0], self.__font_preview_size))
			else:
				print(f'preview font update failed : {self.__selected_font}')

	def on_call(self):
		self.__update_ui()
		self.show()

	def on_save_close(self):
		self.backup_enable_padding = self.enable_padding
		self.backup_enable_dark_mode = self.enable_dark_mode
		self.backup_enable_one_line = self.enable_one_line
		self.backup_enable_square_mode = self.enable_square_mode
		self.backup_save_exif = self.save_exif
		self.backup_save_format_index = self.save_format_index
		self.debug_log(0)
	
	def on_cancel_close(self):
		self.enable_padding = self.backup_enable_padding
		self.enable_dark_mode = self.backup_enable_dark_mode
		self.enable_one_line = self.backup_enable_one_line
		self.enable_square_mode = self.backup_enable_square_mode
		self.save_exif = self.backup_save_exif
		self.save_format_index = self.backup_save_format_index
		self.debug_log(0)

	# Exif Padding 옵션
	def on_toggle_padding_option(self, state):
		self.enable_padding = bool(state == Qt.CheckState.Checked.value)        
		print(f"Padding Mode Pushed, Square Mode Opt: {self.enable_padding}")

	# 폰트 색상
	def on_toggle_dark_mode_option(self, state):
		self.enable_dark_mode = bool(state == Qt.CheckState.Checked.value)        
		print(f"Dark Mode Pushed, Dark Mode Opt: {self.enable_dark_mode}")

	def on_toggle_square_mode_option(self, state):
		self.enable_square_mode = bool(state == Qt.CheckState.Checked.value)        

	def on_toggle_one_line_option(self, state):
		self.enable_one_line = bool(state == Qt.CheckState.Checked.value)        

	def on_toggle_save_exif_data_option(self, state):
		self.save_exif = bool(state == Qt.CheckState.Checked.value)

	def on_change_save_format(self):
		self.save_format_index = self.save_format_box.currentIndex()

	def on_change_font(self):
		self.font_index = self.FontComboBox.currentIndex()
		print(f"Font Index: {self.font_index}")
		self.__selected_font = self.FontComboBox.itemData(self.font_index)
		print(f"Selected Font: {self.__selected_font}")
		self.__update_font_preview()

	def on_trigger_color_picker(self):
		self.__background_color = QColorDialog.getColor(title='Pick  Background Color')
		#user_config.UserConfig.background_color = self.__background_color