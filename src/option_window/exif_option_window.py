import os
import sys
import platform
import pathlib
from pathlib import Path

from user_config import UserConfig
from caption_format_converter import CaptionFormatConverter

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QDialogButtonBox, QDialog, QCheckBox, QSpinBox, QPushButton, QComboBox, QPlainTextEdit, QColorDialog, QLabel, QVBoxLayout

from resource_path import resource_path

UI_EXIF_OPTION = "resources/ui/ExifOptions.ui"
UI_FONTS = "resources/Fonts"

try:
     # UI 파일 로드
     ui_path = resource_path(UI_EXIF_OPTION)
     form_class = uic.loadUiType(ui_path)[0]
          
except Exception as e:
     print(f"Resource loading failed: {str(e)}")
     sys.exit(1)

print("EXIF OPTION UI Loaded Successfully")

class ExifOptionWindow(QDialog, form_class):
	def __init__(self):
		super().__init__()

		# External EXIF data variable
		self.selected_exif_data = None

		# 기타 참조 변수
		self.default_font = 'Barlow-Light'
		self.__font_preview_size = 14
		self.text_color = QColor(0, 0, 0)
		self.background_color = QColor(255, 255, 255)
		self.font_alignment = 0
		self.image_padding = 0
		self.save_exif = False
		self.image_ratio = 0
		self.image_type = 2
		self.image_quality_option = 80
		self.easy_mode_enable = False
		self.easy_mode_oneline = False
		self.caption_format = ""
		self.auto_hide_nonedata = False

		# UI 링킹 설정 (EXIF Options)
		self.exif_option_button_box: QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
		self.image_padding_box: QComboBox
		self.save_exif_data_box: QCheckBox
		self.image_ratio_box: QComboBox
		self.image_type_box: QComboBox
		self.image_quality_spinbox: QSpinBox
		self.open_text_color_button: QPushButton
		self.open_bg_color_button: QPushButton

		# UI 링킹 설정 (Font Options)
		self.font_combo_box: QComboBox
		self.alignment_combo_box: QComboBox
		self.format_input_area: QPlainTextEdit
		self.format_preview_area: QLabel
		self.__font_preview_size: int
		self.selected_font: str
		self.__selected_font_family: str
		self.__selected_font_style: str
		self.enable_easymode_option_box: QCheckBox
		self.enable_easymode_oneline_box: QCheckBox
		self.auto_hide_nonedata_checkbox: QCheckBox
		
		# UI 불러오기
		self.setupUi(self)
		self.bind_ui()
		self.setup_ui_internal()

	def bind_ui(self):
		self.exif_option_button_box.accepted.connect(self.on_save_close)
		self.exif_option_button_box.rejected.connect(self.on_cancel_close)

		self.image_padding_box.currentIndexChanged.connect(self.on_change_padding_option)
		self.image_padding_box.setToolTip("프레임 생성 옵션")

		self.save_exif_data_box.stateChanged.connect(self.on_toggle_save_exif_data_option)
		self.save_exif_data_box.setToolTip("EXIF 저장 옵션")

		self.image_ratio_box.currentIndexChanged.connect(self.on_change_image_ratio)
		self.image_ratio_box.setToolTip("이미지 비율 선택 옵션, Padding 강제 적용")

		self.image_type_box.currentIndexChanged.connect(self.on_change_image_type)
		self.image_type_box.setToolTip("이미지 확장자 선택 옵션")

		self.image_quality_spinbox.valueChanged.connect(self.on_change_image_quality)
		self.image_quality_spinbox.setToolTip("이미지 품질 저장 옵션\n92 정도가 web에서 사용하기 제일 좋습니다.")

		self.open_text_color_button.clicked.connect(self.on_change_textcolor_picker)
		self.open_text_color_button.setToolTip("Frame 내 텍스트 색상 변경 옵션")

		self.open_bg_color_button.clicked.connect(self.on_change_bgcolor_picker)
		self.open_bg_color_button.setToolTip("Frame 색상 변경 옵션")

		self.font_combo_box.currentIndexChanged.connect(self.on_change_font)
		self.font_combo_box.setToolTip("폰트 변경 옵션")

		self.alignment_combo_box.currentIndexChanged.connect(self.on_change_alignment)
		self.alignment_combo_box.setToolTip("정렬 변경 옵션")

		self.format_input_area.textChanged.connect(self.on_format_input_area_changed)
		self.format_input_area.setToolTip("사진 밑에 삽입할 텍스트 입력")

		self.enable_easymode_option_box.stateChanged.connect(self.on_exif_easy_mode_toggled)
		self.enable_easymode_option_box.setToolTip("기존의 자동 텍스트 생성을 원할 시 체크")

		self.enable_easymode_oneline_box.stateChanged.connect(self.on_exif_easy_mode_oneline_toggled)
		self.enable_easymode_oneline_box.setToolTip("기존의 한 줄 출력을 원할 시 체크")

		self.auto_hide_nonedata_checkbox.stateChanged.connect(self.on_auto_hide_nonedata_toggled)
		self.auto_hide_nonedata_checkbox.setToolTip("데이터 오류로 NONEDATA가 뜨는 걸 자동으로 가리고자 할 때 체크.\n렌즈 데이터가 잡히지 않는 똑딱이와 렌즈교환식을 동시 쓰는 경우 등에 좋음")

	def setup_ui_internal(self):
		
		font_asset_path = resource_path(UI_FONTS)
		'''
		if platform.system() == "Windows":
			font_asset_path = os.path.join(os.getcwd(), "../resources/Fonts")
		else:
			font_asset_path = os.path.join(os.path.dirname(sys.executable), "../resources/Fonts")'
		'''

		print(f"Font_asset: {font_asset_path}")
		fonts = pathlib.Path(font_asset_path)
		print(f"Fonts: {fonts}")

		try:
			for item in fonts.iterdir():
				if item.is_file():
					continue

				for font_item in os.listdir(item):
					print(f"Fonts Item: {font_item} at:{item}")
					self.__add_font_combobox(item, font_item)
		except:
			# py 형식으로 실행할 때 macOS 오류 처리용 경로 설정
			fonts = pathlib.Path(os.path.join(os.getcwd(), "../resources/Fonts"))
			for item in fonts.iterdir():
				if item.is_file():
					continue

				for font_item in os.listdir(item):
					print(f"Fonts Item (exception): {font_item} at:{item}")
					self.__add_font_combobox(item, font_item)

	def __add_font_combobox(self, dir_path, file_name):
		font_name = os.path.splitext(file_name)[0]
		item_ext = os.path.splitext(file_name)[1][1:]
		if item_ext != 'ttf':
			return
		fullpath = os.path.join(dir_path, file_name)
		
		font_id = QFontDatabase.addApplicationFont(fullpath)
		font_file_name = os.path.basename(fullpath)

		print("font_id:", font_id)
		print("font_file_name:", font_file_name)

		if font_id >= 0:
			family = QFontDatabase.applicationFontFamilies(font_id)[0]
			print("family:", family)
			style = QFontDatabase.styles(family)[-1]
			print("style:", style)

			self.font_combo_box.addItem(font_name, userData=(fullpath, family, style))
		else:
			print(f'preview font update failed : {fullpath}')

	def __update_ui(self):
		if self.image_padding_box.currentIndex != UserConfig.exif_padding_mode:
			self.image_padding_box.setCurrentIndex(UserConfig.exif_padding_mode)

		if self.save_exif_data_box.isChecked() != UserConfig.exif_save_exifdata:
			self.save_exif_data_box.toggle()

		if self.image_ratio_box.currentIndex() != UserConfig.exif_ratio:
			self.image_ratio_box.setCurrentIndex(UserConfig.exif_ratio)

		if self.image_type_box.currentIndex() != UserConfig.exif_type:
			self.image_type_box.setCurrentIndex(UserConfig.exif_type)

		if self.image_quality_spinbox.value() != UserConfig.exif_quality:
			self.image_quality_spinbox.setValue(UserConfig.exif_quality)

		if self.font_combo_box.currentIndex() != UserConfig.exif_font_index:
			# if folder data is changed from previous run
			if UserConfig.exif_font_index >= self.font_combo_box.count():
				UserConfig.exif_font_index = 1
			self.font_combo_box.setCurrentIndex(UserConfig.exif_font_index)
			self.__update_selected_font()

		if self.alignment_combo_box.currentIndex() != UserConfig.exif_format_alignment:
			self.alignment_combo_box.setCurrentIndex(UserConfig.exif_format_alignment)

		if self.enable_easymode_oneline_box.isChecked() != UserConfig.exif_easymode_oneline:
			self.enable_easymode_oneline_box.toggle()
		
		self.format_input_area.setPlainText(UserConfig.exif_format)
		self.caption_format = UserConfig.exif_format
		self.text_color = UserConfig.exif_text_color
		self.background_color = UserConfig.exif_bg_color

		if self.enable_easymode_option_box.isChecked() != UserConfig.exif_easymode_options:
			self.enable_easymode_option_box.toggle()

		if self.auto_hide_nonedata_checkbox.isChecked() != UserConfig.exif_auto_hide_nonedata:
			self.auto_hide_nonedata_checkbox.toggle()

		self.image_padding_box.setEnabled(self.image_ratio == 0)
		self.__update_font_preview()
			
	def __update_selected_font(self):
		itemData = self.font_combo_box.itemData(self.font_combo_box.currentIndex())
		self.selected_font = itemData[0]
		self.__selected_font_family = itemData[1]
		self.__selected_font_style = itemData[2]

	def on_call(self):
		self.__update_ui()
		self.show()

	def accept(self):
		UserConfig.exif_padding_mode = self.image_padding
		UserConfig.exif_save_exifdata = self.save_exif
		UserConfig.exif_ratio = self.image_ratio
		UserConfig.exif_type = self.image_type
		UserConfig.exif_quality = self.image_quality_option
		UserConfig.exif_text_color = self.text_color
		UserConfig.exif_bg_color = self.background_color
		UserConfig.exif_font_index = self.font_combo_box.currentIndex()
		UserConfig.exif_format_alignment = self.font_alignment
		UserConfig.exif_format = self.caption_format
		UserConfig.exif_easymode_options = self.easy_mode_enable
		UserConfig.exif_easymode_oneline = self.easy_mode_oneline
		UserConfig.exif_auto_hide_nonedata = self.auto_hide_nonedata
		UserConfig.save()
		super().accept()

	def on_save_close(self):
		self.__update_selected_font()

	def on_cancel_close(self):
		self.selected_font = ""

	# Exif Padding 옵션
	def on_change_padding_option(self):
		#self.enable_padding = bool(state == Qt.CheckState.Checked.value)          
		self.image_padding = self.image_padding_box.currentIndex()
		print(f"Padding Mode Pushed, Square Mode Opt: {self.image_padding}")  

	def on_toggle_save_exif_data_option(self, state):
		self.save_exif = bool(state == Qt.CheckState.Checked.value)

	def on_change_image_ratio(self):
		self.image_ratio = self.image_ratio_box.currentIndex()
		self.image_padding_box.setEnabled(self.image_ratio == 0)

	def on_change_image_type(self):
		self.image_type = self.image_type_box.currentIndex()

	def on_change_image_quality(self):
		self.image_quality_option = self.image_quality_spinbox.value()

	def on_change_textcolor_picker(self):
		picked_color = QColorDialog.getColor(title='Pick Text Color', initial=self.text_color)
		if picked_color.isValid():
			self.text_color = picked_color
			self.__update_font_preview()
		
	def on_change_bgcolor_picker(self):
		picked_color = QColorDialog.getColor(title='Pick Background Color', initial=self.background_color)
		if picked_color.isValid():
			self.background_color = picked_color
			self.__update_font_preview()

	def on_change_font(self):
		print(f"Font Index: {self.font_combo_box.currentIndex()}")
		self.__update_selected_font()
		self.__update_font_preview()

	def on_change_alignment(self):
		self.font_alignment = self.alignment_combo_box.currentIndex()
		self.__update_font_preview()

	def on_format_input_area_changed(self):
		self.caption_format = self.format_input_area.toPlainText()
		self.__update_font_preview()

	def on_exif_easy_mode_toggled(self, state):
		self.easy_mode_enable = bool(state == Qt.CheckState.Checked.value)
		self.__update_font_preview()

	def on_exif_easy_mode_oneline_toggled(self, state):
		self.easy_mode_oneline = bool(state == Qt.CheckState.Checked.value)
		self.__update_font_preview() 

	def on_auto_hide_nonedata_toggled(self, state):
		self.auto_hide_nonedata = bool(state == Qt.CheckState.Checked.value)
		self.__update_font_preview()

	def __update_font_preview(self):
		self.format_input_area.setEnabled(not self.easy_mode_enable)
		self.enable_easymode_oneline_box.setEnabled(self.easy_mode_enable)
		self.auto_hide_nonedata_checkbox.setEnabled(not self.easy_mode_enable)

		if self.__selected_font_style:
			font = QFontDatabase.font(self.__selected_font_family, self.__selected_font_style, self.__font_preview_size)
			self.format_preview_area.setFont(font)
		else:
			self.format_preview_area.setFont(QFont(self.__selected_font_family, self.__font_preview_size))

		alignment = Qt.AlignmentFlag.AlignCenter
		if self.font_alignment == 1: alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
		elif self.font_alignment == 2: alignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

		self.format_preview_area.setAlignment(alignment)
		self.format_preview_area.setStyleSheet(f"background-color: {self.background_color.name()}; color: {self.text_color.name()};")

		if self.easy_mode_enable:
			text = CaptionFormatConverter.convert_easymode(self.easy_mode_oneline, self.selected_exif_data)
		else:
			text = CaptionFormatConverter.convert(self.format_input_area.toPlainText(), self.selected_exif_data, self.auto_hide_nonedata)
		
		self.format_preview_area.setText(text)

	def get_current_font_path(self):
		itemData = self.font_combo_box.itemData(UserConfig.exif_font_index)
		return itemData[0]
