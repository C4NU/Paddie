import os
import platform
import sys

from pathlib import Path

from option_window import WebPOptionWindow, ExifOptionWindow, ResizeOptionWindow, WatermarkOptionWindow, InformationWindow

print("Python Package Loaded")
import converter


from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QColorDialog, QPushButton, QPlainTextEdit
from PyQt6.QtGui import QPixmap
print("PyQt6 Package Loaded")

from user_config import UserConfig
from resource_path import resource_path

UI_MAIN = "resources/ui/WebPConverterGUI.ui"
SAMPLE_FILE_PATH = "resources/"

# 26 ~ 41줄 까지 resource sample.jpg 파일 경로 설정 코드 수정 필요함
try:
    # UI 파일 로드
    ui_path = resource_path(UI_MAIN)
    sample_file_path = resource_path(SAMPLE_FILE_PATH)
    form_class = uic.loadUiType(ui_path)[0]
        
except Exception as e:
    print(f"Resource loading failed: {str(e)}")
    sys.exit(1)

print("Main UI Loaded Successfully")

class WebpApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = WebpWindow()

    def show(self):
        self.window.show()

    def exec(self):
        self.app.exec()

class WebpWindow(QMainWindow, form_class):
    default_font = 'Barlow-Light'

    def __init__(self):
        super().__init__()

        # Converter 모듈 initialize
        self.converter = converter.Converter()
        
        # Conversion UI initialize
        self.webp_conversion_option_window = WebPOptionWindow()
        # Watermark UI initialize

        # Exif Frame UI initialize
        self.exif_padding_option_window = ExifOptionWindow()
        self.exif_padding_option_window.accepted.connect(self.show_or_refresh_preview)

        self.information_window = InformationWindow()
        self.resize_window = ResizeOptionWindow()

        # 파일 이름 변수
        self.file_paths = []
        self.file_names = []

        # Preview 영역
        self.window_width_short = 461
        self.window_height = 764
        self.preview_area_margin = 10
        self.preview_area = QLabel(self)
        
        # set window size fixed
        # self.size() does not work in init phase (return 640 x 480)
        self.hide_preview()

        self.setupUi(self)
        self.bind_ui()
        self.init_options()

    def bind_ui(self):
        # 실행 버튼 함수 링킹
        self.add_button.clicked.connect(self.open_file)
        self.add_button.setToolTip("파일 선택하기")
        self.delete_button.clicked.connect(self.delete_file)
        self.delete_button.setToolTip("선택된 파일 삭제하기")
        self.save_button.clicked.connect(self.on_click_save)
        self.save_button.setToolTip("파일 저장하기")
        # 파일 추가 기능 함수 링킹
        self.actionAdd_Files.triggered.connect(self.on_trigger_add_files)
        # 파일 일괄 비우기 기능 함수 링킹
        self.actionClear_List.triggered.connect(self.on_trigger_clear_files)
        # 프로그램 정보 기능 함수 링킹
        self.actionInformation.triggered.connect(self.on_trigger_information)
        # 종료 버튼 함수 링킹
        self.actionExit.triggered.connect(WebpWindow.on_trigger_exit)
        # 목록 선택 이벤트 링킹
        self.image_list_widget.itemSelectionChanged.connect(self.on_image_list_widget_selection_changed)
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
        # Exif Preview 활성화 옵션 링킹
        self.enable_exif_preview_box.stateChanged.connect(self.on_toggle_exif_preview)
        # Resize 옵션 링킹
        self.enable_resize_option_box.stateChanged.connect(self.on_toggle_resize_enable)
        self.open_resize_option_button.clicked.connect(self.on_click_open_resize_option)
        self.open_resize_option_button.setEnabled(self.enable_resize_option_box.isChecked())
        # 원본 사진 위치 저장 옵션 링킹
        self.save_original_path_checkbox.stateChanged.connect(self.on_toggle_save_original_path)

    #################### PyQt FUNCTIONS
    def init_options(self):
        ####################	이미지 품질 관련 옵션
        self.conversion_option = self.enable_conversion_option_box.isChecked()
        ####################	워터마크 관련 옵션
        # self.watermark = self.watermarkBox.toPlainText()
        # self.watermarkFontColor = self.watermarkFontColorBox.isChecked()
        ####################	하단 EXIF 삽입 관련 옵션
        self.exif_writing_option = self.enable_exif_padding_option_box.isChecked()
        self.exif_show_preview = self.enable_exif_preview_box.isChecked()
        ####################    리사이즈 옵션
        self.resize_option = self.enable_resize_option_box.isChecked()
        ####################    원본 위치 저장 옵션
        self.save_original_path = self.save_original_path_checkbox.isChecked()

        UserConfig.load()
        if UserConfig.resize_options:
            self.enable_resize_option_box.toggle()

        if UserConfig.conversion_options:
            self.enable_conversion_option_box.toggle()

        if UserConfig.exif_options:
            self.enable_exif_padding_option_box.toggle()
            
        if UserConfig.exif_show_preview:
            self.enable_exif_preview_box.toggle()

        if UserConfig.save_original_path:
            self.save_original_path_checkbox.toggle()

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
        
    def on_image_list_widget_selection_changed(self):
        self.show_or_refresh_preview()
        
    def show_or_refresh_preview(self):
        if not self.exif_writing_option or not self.exif_show_preview or self.conversion_option or self.image_list_widget.currentRow() < 0:
            self.hide_preview()
            return
        
        selected_path = self.file_paths[self.image_list_widget.currentRow()]
        made_file_name = "sample_output"
        made_file_path = os.path.join(sample_file_path, made_file_name)

        if os.path.exists(made_file_path):
            os.remove(made_file_path)

        made_image = self.converter.convert_exif_image(file_path=selected_path,
                                                       save_path=sample_file_path,
                                                       save_name=made_file_name,
                                                       file_format_option=2, # webp
                                                       font_path=self.exif_padding_option_window.get_current_font_path(),
                                                       bg_color=UserConfig.exif_bg_color,
                                                       text_color=UserConfig.exif_text_color,
                                                       ratio_option=UserConfig.exif_ratio,
                                                       exif_padding_option=UserConfig.exif_padding_mode,
                                                       save_exif_data_option=False,
                                                       resize_option=True,
                                                       axis_option=2, # longest
                                                       alignment_option=UserConfig.exif_format_alignment,
                                                       resize_value=800,
                                                       quality_option=80,
                                                       caption_format=UserConfig.exif_format,
                                                       easymode_option=UserConfig.exif_easymode_options,
                                                       easymode_oneline=UserConfig.exif_easymode_oneline,
                                                       auto_hide_nonedata=UserConfig.exif_auto_hide_nonedata)
        
        if made_image is None:
            self.hide_preview()
            return

        image_width, image_height = made_image.size
        self.setFixedSize(self.window_width_short + self.preview_area_margin + image_width, max(image_height + 30, self.window_height))
        
        pixmap = QPixmap(made_file_path + ".webp")
        
        self.preview_area.setPixmap(pixmap)
        self.preview_area.setVisible(True)
        self.preview_area.setGeometry(self.window_width_short + self.preview_area_margin, 0, image_width, image_height)

        
    def hide_preview(self):
        self.preview_area.setVisible(False)
        self.setFixedSize(self.window_width_short, self.window_height)

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
        selected_item_index = self.image_list_widget.currentRow()
        if selected_item_index < 0 or selected_item_index >= self.image_list_widget.count():
            self.exif_padding_option_window.selected_exif_data = None
        else:
            file_path = self.file_paths[selected_item_index]
            self.exif_padding_option_window.selected_exif_data = self.converter.get_exif_data_on_path(file_path)

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
        self.file_paths.clear()
        self.file_names.clear()
        self.hide_preview()

    def on_trigger_information(self):
        self.information_window.show()

    @staticmethod
    def on_trigger_exit():
        sys.exit()

    def open_file(self):
        open_files = QFileDialog.getOpenFileNames(self, caption="Open File", directory=UserConfig.latest_load_path)

        if len(open_files) > 0:
            load_path = None

            # select first item of added lists
            latest_index = self.image_list_widget.count()
            for file in open_files[0]:
                if "" == file: continue
                if "All Files (*)" == file: continue

                if not load_path:
                    load_path = os.path.dirname(file)

                self.load_file(file)
            self.image_list_widget.setCurrentItem(self.image_list_widget.item(latest_index))
            
            if load_path:
                UserConfig.latest_load_path = load_path
                UserConfig.save()

    def delete_file(self):
        selected_index = self.image_list_widget.currentRow()
        if selected_index < 0 or selected_index >= self.image_list_widget.count():
            return
        
        # Remove the selected item from the list
        deleted_item = self.image_list_widget.takeItem(selected_index)
        deleted_file_path = self.file_paths.pop(selected_index)
        deleted_file_name = self.file_names.pop(selected_index)
        print(f"Deleted item at index {selected_index}: {deleted_file_path} ({deleted_file_name})")

        
    

    def load_file(self, filePath):
        icon = QtGui.QIcon(filePath)
        #todo: manipulate string
        widget_item_text = self.path_string_with_width(filePath, 54)
        item = QtWidgets.QListWidgetItem(icon, widget_item_text)

        size = QtCore.QSize()
        size.setHeight(128)
        size.setWidth(128)

        item.setSizeHint(size)
        self.file_paths.append(filePath)
        file_name = os.path.splitext(filePath)[0]
        self.file_names.append(file_name.split(sep='/')[-1])
        self.image_list_widget.addItem(item)

    def path_string_with_width(self, text, width):
        if '/' in text:
            split_character = '/'
        elif '\\' in text:
            split_character = '\\'
        else: return text

        words = text.split(split_character)
        lines = []
        line = ""
        for word in words:
            if len(line) + len(word) + 1 <= width:
                line += word + split_character
            else:
                lines.append(line)
                line = word + split_character
        
        lines.append(line[:-1])
        result = '\n'.join(lines)
        return result

    def save_file(self):
        # 변환 실행 버튼 callback 함수
        # self.watermarkOption()

        if self.save_original_path and self.image_list_widget.count() > 0:
            file_path = self.file_paths[self.image_list_widget.currentRow()]
            save_path = os.path.dirname(file_path)
        else:
            save_path = QFileDialog.getExistingDirectory(caption='Save Directory',
                                                        directory=UserConfig.latest_save_path)
            UserConfig.latest_save_path = save_path
            UserConfig.save()

        if save_path:
            # 01 WebP 이미지로만 변환할 때
            if self.conversion_option:
                for index in range(self.image_list_widget.count()):
                    self.converter.convert_image_to_webp(file_path=self.file_paths[index],
                                                         save_path=save_path + '/',
                                                         save_name=self.file_names[index],
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
                    self.converter.convert_exif_image(file_path=self.file_paths[index],
                                                      save_path=save_path + '/',
                                                      save_name=self.file_names[index],
                                                      file_format_option=UserConfig.exif_type,
                                                      font_path=self.exif_padding_option_window.get_current_font_path(),
                                                      bg_color=UserConfig.exif_bg_color,
                                                      text_color=UserConfig.exif_text_color,
                                                      ratio_option=UserConfig.exif_ratio,
                                                      exif_padding_option=UserConfig.exif_padding_mode,
                                                      save_exif_data_option=UserConfig.exif_save_exifdata,
                                                      resize_option=self.resize_option,
                                                      axis_option=UserConfig.resize_axis,
                                                      alignment_option=UserConfig.exif_format_alignment,
                                                      resize_value=UserConfig.resize_size,
                                                      quality_option=UserConfig.exif_quality,
                                                      caption_format=UserConfig.exif_format,
                                                      easymode_option=UserConfig.exif_easymode_options,
                                                      easymode_oneline=UserConfig.exif_easymode_oneline,
                                                      auto_hide_nonedata=UserConfig.exif_auto_hide_nonedata)

            else:
                print("옵션 선택 에러 / 다시 선택해주세요")

            if platform.system() == "Windows":  # Windows
                os.startfile(save_path)
            elif platform.system() == "Darwin":  # macOS
                os.system("open " + '"' + save_path + '"')

            self.on_trigger_clear_files()

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
        self.enable_exif_preview_box.setEnabled(checked)
        
        if checked and self.enable_exif_preview_box.isChecked():
            self.show_or_refresh_preview()
        else:
            self.hide_preview()
        
        UserConfig.exif_options = checked
        UserConfig.save()

    def on_toggle_exif_preview(self, state):
        self.exif_show_preview = bool(state == Qt.CheckState.Checked.value)

        checked = self.enable_exif_preview_box.isChecked()
        if checked:
            self.show_or_refresh_preview()
        else:
            self.hide_preview()
        
        UserConfig.exif_show_preview = checked
        UserConfig.save()

    def on_toggle_resize_enable(self, state):
        self.resize_option = bool(state == Qt.CheckState.Checked.value)
        checked = self.enable_resize_option_box.isChecked()
        self.open_resize_option_button.setEnabled(checked)

        UserConfig.resize_options = checked
        UserConfig.save()

    def on_toggle_save_original_path(self, state):
        self.save_original_path = bool(state == Qt.CheckState.Checked.value)
        UserConfig.save_original_path = self.save_original_path_checkbox.isChecked()
        UserConfig.save()

