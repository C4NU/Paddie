import os
import platform
import sys

from pathlib import Path

from option_window import WebPOptionWindow, ExifOptionWindow, ResizeOptionWindow, WatermarkOptionWindow, InformationWindow, SettingWindow
from app_window.preview_window import PreviewWindow

print("Python Package Loaded")
import converter

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt, QLocale, QTranslator
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QColorDialog, QPushButton, QPlainTextEdit, QLabel, QMessageBox
from update_module import UpdateManager
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QThread, pyqtSignal

# Define constants directly here since relative import from src root might be tricky without package restructuring
# ideally this should be `from constants import ...` but let's keep it simple for this file structure
WINDOW_WIDTH_SHORT = 461
WINDOW_HEIGHT = 764
PREVIEW_AREA_MARGIN = 10
UI_MAIN = "resources/ui/webpconvertergui.ui"
SAMPLE_FILE_PATH = "resources/"

print("PyQt6 Package Loaded")

from user_config import UserConfig
from resource_path import resource_path


UserConfig.load()

app = QApplication(sys.argv)
system_locale = QLocale.system().name()  # 예: 'ko_KR'
lang_code = system_locale[:2]  

translator = QTranslator()

# 0: Auto (System Locale), 1: Korean, 2: Japanese, 3: Chinese, 4: English
lang_index = UserConfig.language

load_code = 'en'
if lang_index == 1:
    load_code = 'ko'
elif lang_index == 2:
    load_code = 'ja'
elif lang_index == 3:
    load_code = 'zh'
elif lang_index == 4:
    load_code = 'en'
else:
    # Auto (0) or invalid value: Detect from system locale
    if lang_code in ['ko', 'ja', 'zh']:
        load_code = lang_code
    else:
        load_code = 'en'

# If loading default English when system is Korean, but somehow failed
if load_code == 'en' and lang_code == 'ko':
    # Force Korean if system is clearly Korean but index was 0 or invalid
    load_code = 'ko'

translated_loaded = translator.load(resource_path(f'resources/translations_{load_code}.qm'))
if translated_loaded:
    app.installTranslator(translator)
else:
    # Fallback to English if the specific QM file is missing
    if load_code != 'en':
        translator.load(resource_path('resources/translations_en.qm'))
        app.installTranslator(translator)

# 26 ~ 41줄 까지 resource sample.jpg 파일 경로 설정 코드 수정 필요함
try:
    # UI 파일 로드
    ui_path = resource_path(UI_MAIN)
    sample_file_path = resource_path(SAMPLE_FILE_PATH)
    form_class = uic.loadUiType(ui_path)[0]
        
except (FileNotFoundError, ValueError, OSError) as e:
    print(f"Resource loading failed: {str(e)}")
    sys.exit(1)

print("Main UI Loaded Successfully")



import converter

class WebpApp:
    def __init__(self):
        # app is already created at the module level
        self.app = app
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
        self.setting_window = SettingWindow()
        self.setting_window.on_accepted = self.on_setting_accepted
        self.setting_window.on_config_changed = self.show_or_refresh_preview
        
        self.resize_window = ResizeOptionWindow()

        # 파일 이름 변수
        self.file_paths = []
        self.file_names = []

        # Preview 영역
        self.window_width_short = WINDOW_WIDTH_SHORT
        self.window_height = WINDOW_HEIGHT
        self.preview_area_margin = PREVIEW_AREA_MARGIN
        self.preview_area = QLabel(self)
        self.detached_preview_window = PreviewWindow()
        
        # set window size fixed
        # self.size() does not work in init phase (return 640 x 480)
        self.hide_preview()

        self.setupUi(self)
        self.bind_ui()
        self.init_options()
        
        # macOS 등에서 메뉴바 접근이 어려운 경우를 위해 버튼 추가 (setupUi 이후에 호출해야 함)
        self.create_settings_button()
        
        # 백그라운드 업데이트 체크
        self.check_update_background()

    def check_update_background(self):
        """앱 시작 시 백그라운드에서 업데이트를 체크합니다."""
        self.startup_update_manager = UpdateManager(self.information_window.program_version)
        # 긴급한 작업을 방해하지 않기 위해 약간의 딜레이 후 체크하거나 별도 스레드 권장
        # 여기서는 단순함을 위해 정보를 가져오는 부분만 호출
        def on_check_finished():
            has_update, latest_v, url, body = self.startup_update_manager.check_for_update()
            if has_update:
                reply = QMessageBox.question(self, self.tr("Update Available"),
                                            self.tr(f"A new version ({latest_v}) is available. Do you want to update now?\n\n{body}"),
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    self.on_trigger_information() # 정보 창을 열어 업데이트 진행 유도
                    self.information_window.on_check_update() # 자동으로 업데이트 체크 버튼 누름
        
        # 단순 구현을 위해 QTimer 등을 쓸 수 있지만 여기서는 직접 호출 (네트워크 블락 주의)
        # 실전에서는 QThread 사용 권장. UpdateManager에 이미 QThread 로직이 있으므로 활용 가능
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, on_check_finished) # 2초 후 체크

    def create_settings_button(self):
        """설정 버튼을 프로그램 우측 하단에 동적으로 추가합니다."""
        from PyQt6.QtWidgets import QPushButton
        self.pref_button = QPushButton(self.centralwidget)
        self.pref_button.setGeometry(300, 697, 40, 31) # 위치 조정 필요할 수 있음
        self.pref_button.setText("⚙️")
        self.pref_button.setToolTip(self.tr("Settings"))
        self.pref_button.clicked.connect(self.on_trigger_preferences)

    def on_setting_accepted(self, index):
        """설정이 변경되었을 때 호출됩니다."""
        self.change_language(index)

    def change_language(self, lang_index):
        """프로그램 재시작 없이 언어를 변경합니다."""
        load_code = 'en'
        if lang_index == 1: load_code = 'ko'
        elif lang_index == 2: load_code = 'ja'
        elif lang_index == 3: load_code = 'zh'
        elif lang_index == 4: load_code = 'en'
        else:
            system_locale = QLocale.system().name()[:2]
            load_code = system_locale if system_locale in ['ko', 'ja', 'zh'] else 'en'

        new_translator = QTranslator()
        if new_translator.load(resource_path(f'resources/translations_{load_code}.qm')):
            # 기존 트랜슬레이터 제거 후 새 트랜슬레이터 설치
            global translator
            app_inst = QtWidgets.QApplication.instance()
            app_inst.removeTranslator(translator)
            translator = new_translator
            app_inst.installTranslator(translator)
            
            # 모든 활성 UI 요소 재번역
            self.retranslate_all_ui()
            print(f"Language changed to: {load_code}")

    def retranslate_all_ui(self):
        """모든 윈도우의 UI를 현재 언어로 다시 로드합니다."""
        # 메인 윈도우
        self.retranslateUi(self)
        
        # 설정 버튼 등 동적 생성 요소 갱신
        self.pref_button.setToolTip(self.tr("Settings"))
        
        # 서브 윈도우들
        windows = [
            self.webp_conversion_option_window,
            self.exif_padding_option_window,
            self.information_window,
            self.setting_window,
            self.resize_window,
            self.detached_preview_window
        ]
        
        for win in windows:
            if hasattr(win, 'retranslateUi'):
                win.retranslateUi(win)
            # PreviewWindow 같은 커스텀 클래스의 경우 제목 등 수동 갱신
            if isinstance(win, PreviewWindow):
                win.setWindowTitle(self.tr("Paddie - Preview"))


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
        # 프로그램 설정 기능 함수 링킹
        self.actionPref.triggered.connect(self.on_trigger_preferences)
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
        made_file_path = os.path.join(resource_path(SAMPLE_FILE_PATH), made_file_name)

        if os.path.exists(made_file_path):
            os.remove(made_file_path)

        made_image = self.converter.convert_exif_image(file_path=selected_path,
                                                       save_path=resource_path(SAMPLE_FILE_PATH),
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
        sample_webp_path = made_file_path + ".webp"
        
        if UserConfig.exif_detached_preview:
            # Detached preview mode
            self.hide_internal_preview()
            self.detached_preview_window.set_image(sample_webp_path)
            self.detached_preview_window.show()
            self.detached_preview_window.raise_()
        else:
            # Internal preview mode
            if self.detached_preview_window.isVisible():
                self.detached_preview_window.hide()
                
            self.setFixedSize(self.window_width_short + self.preview_area_margin + image_width, max(image_height + 30, self.window_height))
            pixmap = QPixmap(sample_webp_path)
            self.preview_area.setPixmap(pixmap)
            self.preview_area.setVisible(True)
            self.preview_area.setGeometry(self.window_width_short + self.preview_area_margin, 0, image_width, image_height)
        
    def hide_internal_preview(self):
        self.preview_area.setVisible(False)
        self.setFixedSize(self.window_width_short, self.window_height)

    def hide_preview(self):
        self.hide_internal_preview()
        if self.detached_preview_window:
            self.detached_preview_window.hide()

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

    def on_trigger_preferences(self):
        self.setting_window.show()

    @staticmethod
    def on_trigger_exit():
        sys.exit()

    def open_file(self) -> None:
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

    def delete_file(self) -> None:
        selected_index = self.image_list_widget.currentRow()
        if selected_index < 0 or selected_index >= self.image_list_widget.count():
            return
        
        # Remove the selected item from the list
        deleted_item = self.image_list_widget.takeItem(selected_index)
        deleted_file_path = self.file_paths.pop(selected_index)
        deleted_file_name = self.file_names.pop(selected_index)
        print(f"Deleted item at index {selected_index}: {deleted_file_path} ({deleted_file_name})")

        
    

    def load_file(self, filePath: str) -> None:
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

    def path_string_with_width(self, text: str, width: int) -> str:
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

    def save_file(self) -> None:
        if self.save_original_path and self.image_list_widget.count() > 0:
            file_path = self.file_paths[self.image_list_widget.currentRow()]
            save_path = os.path.dirname(file_path)
        else:
            save_path = QFileDialog.getExistingDirectory(caption='Save Directory',
                                                        directory=UserConfig.latest_save_path)
            UserConfig.latest_save_path = save_path
            UserConfig.save()

        if save_path:
            mode = None
            if self.conversion_option:
                mode = 'conversion'
            elif self.exif_writing_option:
                mode = 'exif'
            else:
                print("옵션 선택 에러 / 다시 선택해주세요")
                return

            config_options = {
                'conversion_loseless': UserConfig.conversion_loseless,
                'conversion_quality': UserConfig.conversion_quality,
                'conversion_exif': UserConfig.conversion_exif,
                'conversion_icc': UserConfig.conversion_icc,
                'conversion_transparent': UserConfig.conversion_transparent,
                'resize_option': self.resize_option,
                'resize_options': UserConfig.resize_options,
                'resize_size': UserConfig.resize_size,
                'exif_type': UserConfig.exif_type,
                'exif_bg_color': UserConfig.exif_bg_color,
                'exif_text_color': UserConfig.exif_text_color,
                'exif_ratio': UserConfig.exif_ratio,
                'exif_padding_mode': UserConfig.exif_padding_mode,
                'exif_save_exifdata': UserConfig.exif_save_exifdata,
                'resize_axis': UserConfig.resize_axis,
                'exif_format_alignment': UserConfig.exif_format_alignment,
                'exif_quality': UserConfig.exif_quality,
                'exif_format': UserConfig.exif_format,
                'exif_easymode_options': UserConfig.exif_easymode_options,
                'exif_easymode_oneline': UserConfig.exif_easymode_oneline,
                'exif_auto_hide_nonedata': UserConfig.exif_auto_hide_nonedata
            }
            font_path = self.exif_padding_option_window.get_current_font_path()

            self.worker = converter.ConversionWorker(mode, self.file_paths.copy(), self.file_names.copy(), save_path, config_options, font_path)
            self.worker.progress.connect(self.on_progress)
            self.worker.finished_conversion.connect(self.on_conversion_finished)
            self.worker.error.connect(self.on_conversion_error)
            
            self.save_button.setEnabled(False)
            if self.save_button.buttons():
                self.save_button.buttons()[0].setText("변환 중...")
            self.worker.start()

    def on_progress(self, value):
        if self.save_button.buttons():
            self.save_button.buttons()[0].setText(f"변환 중... {value}%")

    def on_conversion_finished(self, save_path):
        self.save_button.setEnabled(True)
        if self.save_button.buttons():
            self.save_button.buttons()[0].setText("Save")
        
        if platform.system() == "Windows":  # Windows
            os.startfile(save_path)
        elif platform.system() == "Darwin":  # macOS
            os.system("open " + '"' + save_path + '"')

        self.on_trigger_clear_files()

    def on_conversion_error(self, error_msg):
        self.save_button.setEnabled(True)
        if self.save_button.buttons():
            self.save_button.buttons()[0].setText("Save")
        print(f"변환 중 오류 발생: {error_msg}")
        QMessageBox.warning(self, "오류", f"변환 중 오류가 발생했습니다: {error_msg}")

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

