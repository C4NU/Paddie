import os
import platform
import sys

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog

import webp_module as webp
from main import formClass


class MainWindow(QMainWindow, formClass):
    def __init__(self):
        super().__init__()
        self.__watermark_option = None
        self.__webp_converter = webp.Converter()
        self.__file_name = []
        self.__loseless_option = True
        self.__image_quality_option = 120
        self.__exif_option = True
        self.__icc_profile_option = False
        self.__transparent_rgb_option = False
        self.__conversion_option = True  # webp 변환하는지 선택
        self.__exif_padding_option = False
        # self.__watermark_option = []

        self.setupUi(self)

        self.bind_ui()

        self.InitOptions()

    def bind_ui(self):
        # 실행 버튼 함수 링킹
        self.SaveButton.clicked.connect(self.on_click_save)
        # 파일 추가 버튼 함수 링킹
        self.actionAdd_Files.triggered.connect(self.on_add_files)
        # 종료 버튼 함수 링킹
        self.actionExit.triggered.connect(MainWindow.on_click_exit)
        self.ConversionEnableBox.stateChanged.connect(self.on_toggle_conversion_enable)
        # Loseless 옵션 링킹
        self.LoselessOptionBox.stateChanged.connect(self.on_toggle_loseless_option)
        # 이미지 퀄리티 옵션 링킹
        self.ImageQualityBox.valueChanged.connect(self.on_change_image_quality)
        # Exif 정보 저장 옵션 링킹
        self.ExifOptionBox.stateChanged.connect(self.on_toggle_exif_option)
        self.TransparentRGBBox.stateChanged.connect(self.on_toggle_transparent_rgb)
        self.ICCProfileOptionBox.stateChanged.connect(self.on_toggle_icc_profile_option)
        # Watermark 옵션
        # self.watermarkFontColorBox.stateChanged.connect(self.WatermarkColorOption)
        # ExifView 옵션
        self.EnableExifPadding.stateChanged.connect(self.on_toggle_exif_padding)

    #################### PyQt5 FUNCTIONS
    def InitOptions(self):
        ####################	이미지 품질 관련 옵션
        self.__conversion_option = self.ConversionEnableBox.isChecked()
        ####################	이미지 품질 관련 옵션
        self.__loseless_option = self.LoselessOptionBox.isChecked()
        self.__image_quality_option = self.ImageQualityBox.value()
        self.__exif_option = self.ExifOptionBox.isChecked()
        self.__icc_profile_option = self.ICCProfileOptionBox.isChecked()
        self.__transparent_rgb_option = self.TransparentRGBBox.isChecked()
        ####################	워터마크 관련 옵션
        # self.__watermark_option = self.watermarkBox.toPlainText()
        # self.__watermark_font_color = self.watermarkFontColorBox.isChecked()
        ####################	하단 EXIF 삽입 관련 옵션
        self.__exif_padding_option = self.EnableExifPadding.isChecked()

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
        if self.FileListWidget.count() != 0:
            self.save_file()

    def on_add_files(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open Files...', './')
        if fname == None:
            print("아무 파일 선택 안됨")
        else:
            for name in fname[0]:
                self.load_file(name)

    @staticmethod
    def on_click_exit():
        sys.exit()

    # def watermark_option(self):
    # 	self.watermark = self.watermarkBox.toPlainText()
    # 	print(self.watermark)

    #################### FUNCTIONS
    def load_file(self, filePath):
        icon = QtGui.QIcon(filePath)
        item = QtWidgets.QListWidgetItem(icon, filePath)

        size = QtCore.QSize()
        size.setHeight(128)
        size.setWidth(128)

        item.setSizeHint(size)
        file_name = os.path.splitext(filePath)[0]
        self.__file_name.append(file_name.split(sep='/')[-1])
        self.FileListWidget.addItem(item)

    def save_file(self):
        # 변환 실행 버튼 callback 함수
        # self.watermarkOption()
        save_path = QFileDialog.getSaveFileName(None, 'Save File', self.__file_name[0])

        if save_path[0]:
            str_save_path = save_path[0]
            str_save_path = str_save_path[:str_save_path.rfind("/")]

            # self.watermark#
            for index in range(self.FileListWidget.count()):
                self.__webp_converter.convert_image(self.FileListWidget.item(index).text()
                                                    , str_save_path + '/'
                                                    , self.__file_name[index]
                                                    , self.__loseless_option
                                                    , self.__image_quality_option
                                                    , exif_opt=self.__exif_option
                                                    , icc_profile_opt=self.__icc_profile_option
                                                    , transparent_rgb=self.__transparent_rgb_option
                                                    , watermark_text=""
                                                    , exif_view_opt=self.__exif_padding_option
                                                    , conversion_opt=self.__conversion_option)

            if platform.system() == "Windows":  # Windows
                os.startfile(str_save_path)
            elif platform.system() == "Darwin":  # macOS
                os.system("open " + '"' + str_save_path + '"')

            self.FileListWidget.clear()
            self.__file_name.clear()

        else:
            return

    # note : conversion options begin
    def on_toggle_conversion_enable(self, state):
        self.__conversion_option = bool(state == Qt.Checked)

    def on_toggle_loseless_option(self, state):
        # Qt.checked -> True는 2, False는 0
        self.__loseless_option = bool(state == Qt.Checked)

    def on_toggle_exif_option(self, state):
        self.__exif_option = bool(state == Qt.Checked)

    def on_toggle_icc_profile_option(self, state):
        self.__icc_profile_option = bool(state == Qt.Checked)

    def on_toggle_transparent_rgb(self, state):
        self.__transparent_rgb_option = bool(state == Qt.Checked)

    def on_change_image_quality(self):
        self.__image_quality_option = self.ImageQualityBox.value()

    # note : conversion options end

    # note : watermark option begin
    def on_toggle_watermark_option(self, state):
        self.__watermark_option = bool(state == Qt.Checked)

    # note : watermark option end

    # note : exif option begin
    def on_toggle_exif_padding(self, state):
        self.__exif_padding_option = bool(state == Qt.Checked)
    # note : exif option end
