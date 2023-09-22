import os
import platform
import sys
import pathlib

from option_window import WebPOptionWindow, ExifOptionWindow, ResizeOptionWindow, WatermarkOptionWindow

print("Python Package Loaded")
import user_config
import webp
print("User Package Loaded")

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QColorDialog, QPushButton, QPlainTextEdit
print("PyQt6 Package Loaded")

from user_config import UserConfig

if platform.system() == "Windows":
    form = os.path.join(os.getcwd(), "Resources/WebPConverterGUI.ui")
else:
    # build 완료된 exec 에서는 실행이 되지만, 단순 py 로 실행할때는 라이브러리 경로를 참조함
    form = os.path.join(os.path.dirname(sys.executable), "Resources/WebPConverterGUI.ui")

try:
    formClass = uic.loadUiType(form)[0]
except:
    formClass = uic.loadUiType(os.path.join(os.getcwd(), "Resources/WebPConverterGUI.ui"))[0]

print("UI Loaded")

class WebpApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = WebpWindow()

    def show(self):
        self.window.show()

    def exec(self):
        self.app.exec()

class WebpWindow(QMainWindow, formClass):
    default_font = 'Barlow-Light'

    def __init__(self):
        super().__init__()

        # Converter 모듈 initialize
        self.converter = webp.Converter()
        
        # Conversion UI initialize
        self.webp_conversion_option_window = WebPOptionWindow()
        # Watermark UI initialize

        # Exif Frame UI initialize
        self.exif_padding_option_window = ExifOptionWindow()

        # 파일 이름 변수
        self.file_name = []

        self.setupUi(self)
        #self.setup_ui_internal()
        self.bind_ui()
        self.init_options()

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
        self.FontComboBox.addItem(font_name, userData=fullpath)

    def bind_ui(self):
        # 실행 버튼 함수 링킹
        self.add_button.clicked.connect(self.open_file)
        #self.delete_button.clicked.connect(None)
        self.save_button.clicked.connect(self.on_click_save)
        # 파일 추가 버튼 함수 링킹
        self.actionAdd_Files.triggered.connect(self.on_trigger_add_files)
        self.actionClear_List.triggered.connect(self.on_trigger_clear_files)
        # 종료 버튼 함수 링킹
        self.actionExit.triggered.connect(WebpWindow.on_trigger_exit)
        # Conversion 활성화 옵션 링킹
        self.enable_conversion_option_box.stateChanged.connect(self.on_toggle_conversion_enable)
        self.enable_conversion_option_box.toggle()

        self.open_conversion_option_button.clicked.connect(self.on_click_conversion_option)
        # Watermark 활성화 옵션 링킹
        #self.enable_watermark_option_box.stateChanged.connect(None)
        # Exif Padding 활성화 옵션 링킹
        self.enable_exif_padding_option_box.stateChanged.connect(self.on_toggle_exif_writing_enable)

        self.open_exif_option_button.clicked.connect(self.on_click_exif_padding_option)
        #

    #################### PyQt FUNCTIONS
    def init_options(self):
        ####################	이미지 품질 관련 옵션
        self.conversion_option = self.enable_conversion_option_box.isChecked()
        #self.conversion_option_box = self.conversion_option_setting_button.
        ####################	워터마크 관련 옵션
        # self.watermark = self.watermarkBox.toPlainText()
        # self.watermarkFontColor = self.watermarkFontColorBox.isChecked()
        ####################	하단 EXIF 삽입 관련 옵션
        self.exif_writing_option = self.enable_exif_padding_option_box.isChecked()

        UserConfig.load()
        if UserConfig.background_color:
            self.__background_color = UserConfig.background_color

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()

            # 드래그 드롭시 파일 추가되는 코드
            for url in event.mimeData().urls():
                self.load_file(url.toLocalFile())

        else:
            event.ignore()

    def on_click_save(self):
        if self.image_list_widget.count() != 0:
            self.save_file()

    def on_click_open_resize_option(self):
        def on_accepted_resize_option(width, height):
            # note(komastar) : 리사이즈 정보 쿼리 방법 1. callback
            # accept 된 경우에만 실행
            print(f'width : {width}, height : {height}')

        self.resize_option_window.on_accepted = on_accepted_resize_option
        self.resize_option_window.show()
        # note(komastar) : 리사이즈 정보 쿼리 방법 2. access public property
        # accept 되기 전에 호출하면 제대로 된 값을 불러오지 못 할 수 있음
        # print(f'w:{self.resize_option_window.width}, h:{self.resize_option_window.height}')

    def on_click_conversion_option(self):
        self.webp_conversion_option_window.show()

    def on_click_exif_padding_option(self):
        self.exif_padding_option_window.show()
    
    def on_trigger_add_files(self):
        file_name_list = QFileDialog.getOpenFileNames(self, 'Open Files...', './')
        if file_name_list is None:
            print("아무 파일 선택 안됨")
        else:
            for name in file_name_list[0]:
                self.load_file(name)

    def on_trigger_clear_files(self):
        self.image_list_widget.clear()

    @staticmethod
    def on_trigger_exit():
        sys.exit()

    def watermark_option(self):
        self.watermark_text = self.watermarkBox.toPlainText()
        print(self.watermark_text)

    def open_file(self):
        open_files = QFileDialog.getOpenFileNames(self, "Open File")

        if len(open_files) > 0:
            for file in open_files[0]:
                if "" == file: continue
                if "All Files (*)" == file: continue
                self.load_file(file)

    #################### FUNCTIONS
    def load_file(self, filePath):
        # ISSUE: 파일 로딩할때 특정 이미지 파일이 누워서 로딩됨 / 혹은 저장할때?
        icon = QtGui.QIcon(filePath)
        item = QtWidgets.Qimage_list_widgetItem(icon, filePath)

        size = QtCore.QSize()
        size.setHeight(128)
        size.setWidth(128)

        item.setSizeHint(size)
        file_name = os.path.splitext(filePath)[0]
        self.file_name.append(file_name.split(sep='/')[-1])
        self.image_list_widget.addItem(item)

    def save_file(self):
        # 변환 실행 버튼 callback 함수
        # self.watermarkOption()

        save_path = QFileDialog.getExistingDirectory(caption='Save Directory',
                                                     directory=UserConfig.latest_save_path)
        UserConfig.latest_save_path = save_path
        UserConfig.save()

        if save_path:
            # 01 WebP 이미지로만 변환할 때
            print(self.__selected_font)  # macOS exec 빌드시 None
            if self.conversion_option:
                for index in range(self.image_list_widget.count()):
                    self.converter.convert_image_to_webp(file_path=self.image_list_widget.item(index).text(),
                                                         save_path=save_path + '/',
                                                         save_name=self.file_name[index],
                                                         loseless_option=self.loseless_option,
                                                         image_quality_option=self.image_quality_option,
                                                         exif_option=self.exif_option,
                                                         icc_profile_option=self.icc_profile_option,
                                                         exact_option=self.exact_option, watermark_text="",
                                                         exif_view_option=self.exif_writing_option,
                                                         conversion_option=self.conversion_option,
                                                         font_path=self.__selected_font)

            # 02 Exif Padding 이미지로만 변환할때
            elif self.exif_writing_option:
                for index in range(self.image_list_widget.count()):
                    self.converter.convert_exif_image(file_path=self.image_list_widget.item(index).text(),
                                                      save_path=save_path + '/',
                                                      save_name=self.file_name[index],
                                                      file_format_option=self.save_format_index,
                                                      font_path=self.__selected_font,
                                                      bg_color=self.__background_color,
                                                      square_padding_option=self.square_mode_option,
                                                      dark_theme_option=self.dark_mode_option,
                                                      exif_padding_option=self.padding_option,
                                                      one_line_option=self.line_text_option,
                                                      save_exif_data_option=self.save_exif_data)

            else:
                print("옵션 선택 에러 / 다시 선택해주세요")

            if platform.system() == "Windows":  # Windows
                os.startfile(save_path)
            elif platform.system() == "Darwin":  # macOS
                os.system("open " + '"' + save_path + '"')

            self.image_list_widget.clear()
            self.file_name.clear()

    def on_toggle_conversion_enable(self, state):
        self.conversion_option = bool(state == Qt.CheckState.Checked.value)
        self.enable_exif_padding_option_box.setChecked(not state)
        print(f"Conversion Pushed, Conversion Opt: {self.conversion_option}")
        #print(f"Conversion Pushed, Exif Padding Opt: {self.exif_writing_option}")


    def on_trigger_color_picker(self):
        self.__background_color = QColorDialog.getColor(title='Pick  Background Color')
        user_config.UserConfig.background_color = self.__background_color

    def on_toggle_icc_profile_option(self, state):
        self.icc_profile_option = bool(state == Qt.CheckState.Checked.value)

    def on_toggle_loseless_option(self, state):
        self.loseless_option = bool(state == Qt.CheckState.Checked.value)

    def on_change_image_quality(self):
        self.image_quality_option = self.ImageQualityBox.value()

    def on_toggle_exif_option(self, state):
        self.exif_option = bool(state == Qt.CheckState.Checked.value)

    def on_toggle_exact_option(self, state):
        self.exact_option = bool(state == Qt.CheckState.Checked.value)

    # 워터마크 옵션
    def WatermarkColorOption(self, state):
        self.watermakr_option = bool(state == Qt.CheckState.Checked.value)

    # Exif Padding 옵션
    def on_toggle_exif_writing_enable(self, state):
        self.exif_writing_option = bool(state == Qt.CheckState.Checked.value)

        self.enable_conversion_option_box.setChecked(not state)

        print(f"Exif Padding Pushed, Conversion Opt: {self.conversion_option}")
        #print(f"Exif Padding Pushed, Exif Padding Opt: {self.exif_writing_option}")
        
    def on_change_square_mode(self, state):
        self.square_mode_option = bool(state == Qt.CheckState.Checked.value)        
        print(f"Square Mode Pushed, Square Mode Opt: {self.square_mode_option}")
    
    def on_change_dark_mode(self, state):
        self.dark_mode_option = bool(state == Qt.CheckState.Checked.value)        
        print(f"Dark Mode Pushed, Dark Mode Opt: {self.dark_mode_option}")

    def on_change_padding(self, state):
        self.padding_option = bool(state == Qt.CheckState.Checked.value)        
        print(f"Enable Padding Pushed, Padding Opt: {self.padding_option}")
        
    def on_change_line_text(self, state):
        self.line_text_option = bool(state == Qt.CheckState.Checked.value)        
        print(f"Enable Line Text Pushed, Line Text Opt: {self.line_text_option}")

    def on_change_save_format(self):
        self.save_format_index = self.SaveFormatBox.currentIndex()

    def on_change_font(self):
        self.font_index = self.FontComboBox.currentIndex()
        print(f"Font Index: {self.font_index}")
        self.__selected_font = self.FontComboBox.itemData(self.font_index)
        print(f"Selected Font: {self.__selected_font}")
        self.__update_font_preview()

    def on_change_save_exif(self, state):
        self.save_exif_data = bool(state == Qt.CheckState.Checked.value)
