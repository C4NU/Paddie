import os
import platform
import sys
import pathlib
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

        self.save_exif_data = None
        self.FontComboBox = None
        self.listWidget = None
        self.actionClear_List = None
        self.open_color_picker_button: QPushButton
        self.font_preview_line_edit: QPlainTextEdit
        self.__font_preview_size: int
        self.__font_preview_size = 24

        self.__selected_font = None
        self.font_index = 0
        self.watermakr_option = None
        self.watermark_text = None
        self.converter = webp.Converter()
        self.file_name = []

        self.loseless_option = False
        self.image_quality_option = 80
        self.exif_option = False
        self.icc_profile_option = False
        self.exact_option = False

        self.conversion_option = True  # webp 변환하는지 선택

        # Exif Options 관련 변수
        self.exif_writing_option = False  # Exif Padding 을 enable 할 지에 대한 변수
        self.square_mode_option = False
        self.dark_mode_option = False
        self.padding_option = False       
        self.line_text_option = False 
        self.save_format_index = 0  # JPG, PNG, WebP 파일 형식중 고른 값에 대한 변수
        self.__background_color = None

        # self.watermark = []

        self.setupUi(self)
        self.setup_ui_internal()
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
        self.addButton.clicked.connect(self.open_file)
        self.SaveButton.clicked.connect(self.on_click_save)
        # 파일 추가 버튼 함수 링킹
        self.actionAdd_Files.triggered.connect(self.on_trigger_add_files)
        self.actionClear_List.triggered.connect(self.on_trigger_clear_files)
        # 종료 버튼 함수 링킹
        self.actionExit.triggered.connect(WebpWindow.on_trigger_exit)
        # 변환 활성화 trigger 함수 링킹
        self.ConversionEnableBox.stateChanged.connect(self.on_toggle_conversion_enable)
        self.ConversionEnableBox.toggle()
        # Loseless 옵션 링킹
        self.LoselessOptionBox.stateChanged.connect(self.on_toggle_loseless_option)
        # 이미지 퀄리티 옵션 링킹
        self.ImageQualityBox.valueChanged.connect(self.on_change_image_quality)
        # Exif 정보 저장 옵션 링킹
        self.ExifOptionBox.stateChanged.connect(self.on_toggle_exif_option)
        self.ExactOptionBox.stateChanged.connect(self.on_toggle_exact_option)
        self.ICCProfileOptionBox.stateChanged.connect(self.on_toggle_icc_profile_option)
        self.open_color_picker_button.clicked.connect(self.on_trigger_color_picker)
        # Watermark 옵션
        # self.watermarkFontColorBox.stateChanged.connect(self.WatermarkColorOption)
        # Exif Padding 활성화 옵션 링킹
        self.EnableExifWriting.stateChanged.connect(self.on_toggle_exif_writing_enable)
        self.EnableSquareMode.stateChanged.connect(self.on_change_square_mode)
        self.EnableDarkMode.stateChanged.connect(self.on_change_dark_mode)
        self.EnablePadding.stateChanged.connect(self.on_change_padding)
        self.EnableLineText.stateChanged.connect(self.on_change_line_text)
        self.FontComboBox.currentIndexChanged.connect(self.on_change_font)
        self.SaveFormatBox.currentIndexChanged.connect(self.on_change_save_format)
        self.SaveExifDataBox.stateChanged.connect(self.on_change_save_exif)

    #################### PyQt FUNCTIONS
    def init_options(self):
        ####################	이미지 품질 관련 옵션
        self.conversion_option = self.ConversionEnableBox.isChecked()
        ####################	이미지 품질 관련 옵션
        self.loseless_option = self.LoselessOptionBox.isChecked()
        self.image_quality_option = self.ImageQualityBox.value()
        self.exif_option = self.ExifOptionBox.isChecked()
        self.icc_profile_option = self.ICCProfileOptionBox.isChecked()
        self.exact_option = self.ExactOptionBox.isChecked()
        ####################	워터마크 관련 옵션
        # self.watermark = self.watermarkBox.toPlainText()
        # self.watermarkFontColor = self.watermarkFontColorBox.isChecked()
        ####################	하단 EXIF 삽입 관련 옵션
        self.exif_writing_option = self.EnableExifWriting.isChecked()
        self.square_mode_option = self.EnableSquareMode.isChecked()
        self.dark_mode_option = self.EnableDarkMode.isChecked()
        self.padding_option = self.EnablePadding.isChecked()
        self.line_text_option = self.EnableLineText.isChecked()
        self.save_format_index = self.SaveFormatBox.currentIndex()
        self.font_index = self.FontComboBox.currentIndex()
        default_font_index = self.FontComboBox.findText(WebpWindow.default_font)
        self.FontComboBox.setCurrentIndex(default_font_index)
        self.save_exif_data = self.SaveExifDataBox.isChecked()
        self.__selected_font = self.FontComboBox.itemData(self.font_index)
        UserConfig.load()
        self.__background_color = UserConfig.background_color
        
        self.EnablePadding.setEnabled(False)
        self.EnableDarkMode.setEnabled(False)
        self.EnableSquareMode.setEnabled(False)
        self.EnableLineText.setEnabled(False)
        self.SaveExifDataBox.setEnabled(False)

        self.__update_font_preview()

    def __update_font_preview(self):
        font_id = QFontDatabase.addApplicationFont(self.__selected_font)
        if font_id > 0:
            families = QFontDatabase.applicationFontFamilies(font_id)
            font_temp = families[0]
            self.font_preview_line_edit.setFont(QFont(font_temp, self.__font_preview_size))
        else:
            print(f'preview font update failed : {self.__selected_font}')

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
        if self.listWidget.count() != 0:
            self.save_file()

    def on_trigger_add_files(self):
        file_name_list = QFileDialog.getOpenFileNames(self, 'Open Files...', './')
        if file_name_list is None:
            print("아무 파일 선택 안됨")
        else:
            for name in file_name_list[0]:
                self.load_file(name)

    def on_trigger_clear_files(self):
        self.listWidget.clear()

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
        item = QtWidgets.QListWidgetItem(icon, filePath)

        size = QtCore.QSize()
        size.setHeight(128)
        size.setWidth(128)

        item.setSizeHint(size)
        file_name = os.path.splitext(filePath)[0]
        self.file_name.append(file_name.split(sep='/')[-1])
        self.listWidget.addItem(item)

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
                for index in range(self.listWidget.count()):
                    self.converter.convert_image_to_webp(file_path=self.listWidget.item(index).text(),
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
                for index in range(self.listWidget.count()):
                    self.converter.convert_exif_image(file_path=self.listWidget.item(index).text(),
                                                      save_path=save_path + '/',
                                                      save_name=self.file_name[index],
                                                      file_format_option=self.save_format_index,
                                                      font_path=self.__selected_font,
                                                      bg_color=self.__background_color,
                                                      square_padding_option=self.square_mode_option,
                                                      dark_theme_option=self.dark_mode_option,
                                                      exif_padding_option=self.padding_option,
                                                      one_line_option=self.line_text_option,
                                                      save_exif_data_option=self.save_exif_data                                                      
                                                      )

            else:
                print("옵션 선택 에러 / 다시 선택해주세요")

            if platform.system() == "Windows":  # Windows
                os.startfile(save_path)
            elif platform.system() == "Darwin":  # macOS
                os.system("open " + '"' + save_path + '"')

            self.listWidget.clear()
            self.file_name.clear()

    def on_toggle_conversion_enable(self, state):
        self.conversion_option = bool(state == Qt.CheckState.Checked.value)
        self.EnableExifWriting.setChecked(not state)
        print(f"Conversion Pushed, Conversion Opt: {self.conversion_option}")
        print(f"Conversion Pushed, Exif Padding Opt: {self.exif_writing_option}")

        if not self.conversion_option:
            self.LoselessOptionBox.setEnabled(False)
            self.ExifOptionBox.setEnabled(False)
            self.ICCProfileOptionBox.setEnabled(False)
            self.ExactOptionBox.setEnabled(False)

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

        self.ConversionEnableBox.setChecked(not state)
        self.LoselessOptionBox.setEnabled(not state)
        self.ExifOptionBox.setEnabled(not state)
        self.ICCProfileOptionBox.setEnabled(not state)
        self.ExactOptionBox.setEnabled(not state)

        self.EnableSquareMode.setEnabled(bool(state))
        self.EnableDarkMode.setEnabled(bool(state))
        self.EnablePadding.setEnabled(bool(state))
        self.EnableLineText.setEnabled(bool(state))
        self.SaveExifDataBox.setEnabled(bool(state))

        print(f"Exif Padding Pushed, Conversion Opt: {self.conversion_option}")
        print(f"Exif Padding Pushed, Exif Padding Opt: {self.exif_writing_option}")
        
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
