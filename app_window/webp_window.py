import os
import platform
import sys

from pathlib import Path

from option_window import WebPOptionWindow, ExifOptionWindow, ResizeOptionWindow, WatermarkOptionWindow, InformationWindow

print("Python Package Loaded")
import webp

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
    program_exec_path = os.getcwd()
    form = os.path.join(program_exec_path, "Resources/WebPConverterGUI.ui")
else:
    # build 완료된 exec 에서는 실행이 되지만, 단순 py 로 실행할때는 라이브러리 경로를 참조함
    program_exec_path = os.path.dirname(sys.executable)
    form = os.path.join(program_exec_path, "Resources/WebPConverterGUI.ui")

try:
    formClass = uic.loadUiType(form)[0]
except:
    program_exec_path = os.getcwd()
    formClass = uic.loadUiType(os.path.join(program_exec_path, "Resources/WebPConverterGUI.ui"))[0]

if platform.system() == "Windows":
    sample_file_path = os.path.join(program_exec_path, "Resources/")
else:
    # build 완료된 exec 에서는 실행이 되지만, 단순 py 로 실행할때는 라이브러리 경로를 참조함
    sample_file_path = os.path.join(program_exec_path, "Resources/")
    if Path(sample_file_path+"Sample.jpg").is_file() == True:
        print("Sample File Exists")
    else:
        sample_file_path = os.path.join(program_exec_path, "Resources/")

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

        self.information_window = InformationWindow()
        self.resize_window = ResizeOptionWindow()

        # 파일 이름 변수
        self.file_name = []

        self.setupUi(self)
        self.bind_ui()
        self.init_options()

    def bind_ui(self):
        # 실행 버튼 함수 링킹
        self.add_button.clicked.connect(self.open_file)
        self.add_button.setToolTip("파일 선택하기")
        #self.delete_button.clicked.connect(None)
        self.save_button.clicked.connect(self.on_click_save)
        self.save_button.setToolTip("파일 저장하기")
        # 파일 추가 기능 함수 링킹
        self.actionAdd_Files.triggered.connect(self.on_trigger_add_files)
        # 파일 일괄 비우기 기능 함수 링킹
        self.actionClear_List.triggered.connect(self.on_trigger_clear_files)
        # 프로그램 정보 기능 함수 링킹
        self.actionInformation.triggered.connect(self.on_trigger_information)
        # Exif Frame Preview 표시 기능 링킹
        self.preview_button.clicked.connect(self.on_click_preview)
        #self.preview_button.setEnabled(self.enable_exif_padding_option_box.isChecked())
        self.preview_button.setEnabled(False) # temporarily disabled
        # 종료 버튼 함수 링킹
        self.actionExit.triggered.connect(WebpWindow.on_trigger_exit)
        # Conversion 활성화 옵션 링킹
        self.enable_conversion_option_box.stateChanged.connect(self.on_toggle_conversion_enable)
        self.open_conversion_option_button.clicked.connect(self.on_click_conversion_option)
        self.open_conversion_option_button.setEnabled(self.enable_conversion_option_box.isChecked())
        # Watermark 활성화 옵션 링킹
        #self.enable_watermark_option_box.stateChanged.connect(None)
        self.enable_watermark_option_box.setEnabled(False)
        # Exif Padding 활성화 옵션 링킹
        self.enable_exif_padding_option_box.stateChanged.connect(self.on_toggle_exif_writing_enable)
        self.open_exif_option_button.clicked.connect(self.on_click_exif_padding_option)
        self.open_exif_option_button.setEnabled(self.enable_exif_padding_option_box.isChecked())
        # Resize 옵션 링킹
        self.enable_resize_option_box.stateChanged.connect(self.on_toggle_resize_enable)
        self.open_resize_option_button.clicked.connect(self.on_click_open_resize_option)
        self.open_resize_option_button.setEnabled(self.enable_resize_option_box.isChecked())

    #################### PyQt FUNCTIONS
    def init_options(self):
        ####################	이미지 품질 관련 옵션
        self.conversion_option = self.enable_conversion_option_box.isChecked()
        ####################	워터마크 관련 옵션
        # self.watermark = self.watermarkBox.toPlainText()
        # self.watermarkFontColor = self.watermarkFontColorBox.isChecked()
        ####################	하단 EXIF 삽입 관련 옵션
        self.exif_writing_option = self.enable_exif_padding_option_box.isChecked()
        ####################    리사이즈 옵션
        self.resize_option = self.enable_resize_option_box.isChecked()

        UserConfig.load()
        if UserConfig.resize_options:
            self.enable_resize_option_box.toggle()

        if UserConfig.conversion_options:
            self.enable_conversion_option_box.toggle()

        if UserConfig.exif_options:
            self.enable_exif_padding_option_box.toggle()

    def resizeEvent(self, event):
        geometry = self.image_list_widget.geometry()
        width = event.size().width()
        self.image_list_widget.setGeometry(geometry.x(), geometry.y(), width, geometry.height())

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

    def on_click_preview(self):
        self.converter.show_sample_exif_frame_image(file_path=sample_file_path,
                                                    file_name="Sample.jpg",
                                                    font_path=self.exif_padding_option_window.get_current_font_path(),
                                                    text_color=UserConfig.exif_text_color,
                                                    bg_color=UserConfig.exif_bg_color,
                                                    ratio_option=UserConfig.exif_ratio,
                                                    exif_padding_option=UserConfig.exif_padding,
                                                    alignment_option=UserConfig.exif_format_alignment,
                                                    caption_format=UserConfig.exif_format)

    def on_click_open_resize_option(self):
        def on_accepted_resize_option(axis_option, resize_value):
            # note(komastar) : 리사이즈 정보 쿼리 방법 1. callback
            # accept 된 경우에만 실행
            self.resize_axis_option = axis_option
            self.resize_value = resize_value

            print(f'Axis(0:Width,1:Height,2:Longest,3:Shortest) : {axis_option}, resize value: {resize_value}')

        self.resize_window.on_accepted = on_accepted_resize_option
        self.resize_window.on_call()
        # note(komastar) : 리사이즈 정보 쿼리 방법 2. access public property
        # accept 되기 전에 호출하면 제대로 된 값을 불러오지 못 할 수 있음
        # print(f'w:{self.resize_option_window.width}, h:{self.resize_option_window.height}')

    def on_click_conversion_option(self):
        self.webp_conversion_option_window.on_call()

    def on_click_watermark_option(self):
        pass #self.watermark_option_window.on_call()

    def on_click_exif_padding_option(self):
        self.exif_padding_option_window.on_call()
    
    def on_trigger_add_files(self):
        file_name_list = QFileDialog.getOpenFileNames(self, 'Open Files...', './')
        if file_name_list is None:
            print("아무 파일 선택 안됨")
        else:
            for name in file_name_list[0]:
                self.load_file(name)

    def on_trigger_clear_files(self):
        self.image_list_widget.clear()

    def on_trigger_information(self):
        self.information_window.show()

    @staticmethod
    def on_trigger_exit():
        sys.exit()

    def open_file(self):
        open_files = QFileDialog.getOpenFileNames(self, caption="Open File", directory=UserConfig.latest_load_path)

        if len(open_files) > 0:
            load_path = None

            for file in open_files[0]:
                if "" == file: continue
                if "All Files (*)" == file: continue

                if not load_path:
                    load_path = os.path.dirname(file)

                self.load_file(file)
            
            if load_path:
                UserConfig.latest_load_path = load_path
                UserConfig.save()

    def load_file(self, filePath):
        icon = QtGui.QIcon(filePath)
        item = QtWidgets.QListWidgetItem(icon, filePath)

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
            if self.conversion_option:
                for index in range(self.image_list_widget.count()):
                    self.converter.convert_image_to_webp(file_path=self.image_list_widget.item(index).text(),
                                                         save_path=save_path + '/',
                                                         save_name=self.file_name[index],
                                                         loseless_option=UserConfig.conversion_loseless,
                                                         image_quality_option=UserConfig.conversion_quality,
                                                         exif_option=UserConfig.conversion_exif,
                                                         icc_profile_option=UserConfig.conversion_icc,
                                                         exact_option=UserConfig.conversion_transparent, watermark_text="",
                                                         conversion_option=self.conversion_option,
                                                         resize_option=self.resize_option,
                                                         axis_option=UserConfig.resize_options,
                                                         resize_value=UserConfig.resize_size)

            # 02 Exif Padding 이미지로만 변환할때
            elif self.exif_writing_option:
                for index in range(self.image_list_widget.count()):
                    self.converter.convert_exif_image(file_path=self.image_list_widget.item(index).text(),
                                                      save_path=save_path + '/',
                                                      save_name=self.file_name[index],
                                                      file_format_option=UserConfig.exif_type,
                                                      font_path=self.exif_padding_option_window.get_current_font_path(),
                                                      bg_color=UserConfig.exif_bg_color,
                                                      text_color=UserConfig.exif_text_color,
                                                      ratio_option=UserConfig.exif_ratio,
                                                      exif_padding_option=UserConfig.exif_padding,
                                                      save_exif_data_option=UserConfig.exif_save_exifdata,
                                                      resize_option=self.resize_option,
                                                      axis_option=UserConfig.resize_axis,
                                                      alignment_option=UserConfig.exif_format_alignment,
                                                      resize_value=UserConfig.resize_size,
                                                      quality_option=UserConfig.exif_quality,
                                                      caption_format=UserConfig.exif_format)

            else:
                print("옵션 선택 에러 / 다시 선택해주세요")

            if platform.system() == "Windows":  # Windows
                os.startfile(save_path)
            elif platform.system() == "Darwin":  # macOS
                os.system("open " + '"' + save_path + '"')

            self.image_list_widget.clear()
            self.file_name.clear()

    # WebP 변환 옵션
    def on_toggle_conversion_enable(self, state):
        self.conversion_option = bool(state == Qt.CheckState.Checked.value)
        self.enable_exif_padding_option_box.setChecked(not state)

        checked = self.enable_conversion_option_box.isChecked()
        self.open_conversion_option_button.setEnabled(checked)
        UserConfig.conversion_options = checked
        UserConfig.save()

    # 워터마크 옵션
    def WatermarkColorOption(self, state):
        self.watermakr_option = bool(state == Qt.CheckState.Checked.value)

    # Exif 표기 옵션
    def on_toggle_exif_writing_enable(self, state):
        self.exif_writing_option = bool(state == Qt.CheckState.Checked.value)
        self.enable_conversion_option_box.setChecked(not state)

        checked = self.enable_exif_padding_option_box.isChecked()
        self.open_exif_option_button.setEnabled(checked)
        #self.preview_button.setEnabled(checked)
        UserConfig.exif_options = checked
        UserConfig.save()

    def on_toggle_resize_enable(self, state):
        self.resize_option = bool(state == Qt.CheckState.Checked.value)
        checked = self.enable_resize_option_box.isChecked()
        self.open_resize_option_button.setEnabled(checked)

        UserConfig.resize_options = checked
        UserConfig.save()

