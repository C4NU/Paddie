import os
import platform
import sys
import pathlib
import webp

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog

if platform.system() == "Windows":
    form = os.path.join(os.getcwd(), "WebPConverterGUI.ui")
else:
    # build 완료된 exec 에서는 실행이 되지만, 단순 py 로 실행할때는 라이브러리 경로를 참조함
    form = os.path.join(os.path.dirname(sys.executable), "WebPConverterGUI.ui")

try:
    formClass = uic.loadUiType(form)[0]
except:
    formClass = uic.loadUiType(os.path.join(os.getcwd(), "WebPConverterGUI.ui"))[0]

class WebpApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = WebpWindow()

    def show(self):
        self.window.show()

    def exec(self):
        self.app.exec_()


class WebpWindow(QMainWindow, formClass):
    default_font = 'Barlow-Light'

    def __init__(self):
        super().__init__()

        self.FontComboBox = None
        self.listWidget = None
        self.actionClear_List = None

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
        self.exif_padding_option = False  # Exif Padding 을 enable 할 지에 대한 변수
        self.save_format_index = 0  # JPG, PNG, WebP 파일 형식중 고른 값에 대한 변수

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
        # Watermark 옵션
        # self.watermarkFontColorBox.stateChanged.connect(self.WatermarkColorOption)
        # Exif Padding 활성화 옵션 링킹
        self.EnableExifPadding.stateChanged.connect(self.on_toggle_exif_padding_enable)
        self.FontComboBox.currentIndexChanged.connect(self.on_change_font)
        self.SaveFormatBox.currentIndexChanged.connect(self.on_change_save_format)

    #################### PyQt5 FUNCTIONS
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
        self.exif_padding_option = self.EnableExifPadding.isChecked()
        self.save_format_index = self.SaveFormatBox.currentIndex()
        self.font_index = self.FontComboBox.currentIndex()
        default_font_index = self.FontComboBox.findText(WebpWindow.default_font)
        self.FontComboBox.setCurrentIndex(default_font_index)
        self.__selected_font = self.FontComboBox.itemData(self.font_index)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
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
        
        save_path = QFileDialog.getExistingDirectory(None, 'Save Directory')

        if save_path:
            # 01 WebP 이미지로만 변환할 때
            print(self.__selected_font) # macOS exec 빌드시 None
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
                                                            exif_view_option=self.exif_padding_option,
                                                            conversion_option=self.conversion_option,
                                                            font_path=self.__selected_font)

            # 02 Exif Padding 이미지로만 변환할때
            elif self.exif_padding_option:
                for index in range(self.listWidget.count()):
                    self.converter.convert_exif_image(file_path=self.listWidget.item(index).text(),
                                                        save_path=save_path + '/',
                                                        save_name=self.file_name[index],
                                                        file_format_option=self.save_format_index,
                                                        font_path=self.__selected_font)

            else:
                print("옵션 선택 에러 / 다시 선택해주세요")

            if platform.system() == "Windows":  # Windows
                os.startfile(save_path)
            elif platform.system() == "Darwin":  # macOS
                os.system("open " + '"' + save_path + '"')

            self.listWidget.clear()
            self.file_name.clear()


    def on_toggle_conversion_enable(self, state):
        self.conversion_option = bool(state == Qt.Checked)
        self.EnableExifPadding.setChecked(not state)

        print(f"Conversion Pushed, Conversion Opt: {self.conversion_option}")
        print(f"Conversion Pushed, Exif Padding Opt: {self.exif_padding_option}")

        if self.conversion_option == False:
            if self.icc_profile_option == True:
                self.icc_profile_option = False
                self.ICCProfileOptionBox.toggle()

            if self.loseless_option == True:
                self.loseless_option = False
                self.LoselessOptionBox.toggle()

            if self.exif_option == True:
                self.exif_option = False
                self.ExifOptionBox.toggle()

            if self.exact_option == True:
                self.exact_option = False
                self.ExactOptionBox.toggle()
            

    def on_toggle_icc_profile_option(self, state):
        self.icc_profile_option = bool(state == Qt.Checked)

    def on_toggle_loseless_option(self, state):
        self.loseless_option = bool(state == Qt.Checked)

    def on_change_image_quality(self):
        self.image_quality_option = self.ImageQualityBox.value()

    def on_toggle_exif_option(self, state):
        self.exif_option = bool(state == Qt.Checked)

    def on_toggle_exact_option(self, state):
        self.exact_option = bool(state == Qt.Checked)

    # 워터마크 옵션
    def WatermarkColorOption(self, state):
        self.watermakr_option = bool(state == Qt.Checked)

    # Exif Padding 옵션
    def on_toggle_exif_padding_enable(self, state):
        self.exif_padding_option = bool(state == Qt.Checked)
        self.ConversionEnableBox.setChecked(not state)
        print(f"Exif Padding Pushed, Conversion Opt: {self.conversion_option}")
        print(f"Exif Padding Pushed, Exif Padding Opt: {self.exif_padding_option}")

    def on_change_save_format(self):
        self.save_format_index = self.SaveFormatBox.currentIndex()

    def on_change_font(self):
        self.font_index = self.FontComboBox.currentIndex()
        print(f"Font Index: {self.font_index}")
        self.__selected_font = self.FontComboBox.itemData(self.font_index)
        print(f"Selected Font: {self.__selected_font}")
