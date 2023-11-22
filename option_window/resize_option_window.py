# Copyright 2023 Eugene Kim (komastar) komastar.photo@gmail.com
import os
import sys
import platform

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialogButtonBox, QSpinBox, QDialog, QComboBox
from user_config import UserConfig

if platform.system() == "Windows":
    form = os.path.join(os.getcwd(), "Resources/ResizeOption.ui")
else:
    # build 완료된 exec 에서는 실행이 되지만, 단순 py 로 실행할때는 라이브러리 경로를 참조함
    form = os.path.join(os.path.dirname(sys.executable), "Resources/ResizeOption.ui")

try:
    formClass = uic.loadUiType(form)[0]
except:
    formClass = uic.loadUiType(os.path.join(os.getcwd(), "Resources/ResizeOption.ui"))[0]


class ResizeOptionWindow(QDialog, formClass):
    def __init__(self):
        super().__init__()
        
        self.base_size = 3000

        self.resize_option_button_box: QDialogButtonBox
        self.axis_option_box: QComboBox
        
        self.resize_value_box: QSpinBox
        self.axis_option = 2
        self.resize_value = self.base_size

        self.setupUi(self)
        self.bind_ui()
        self.init_options()
        # 기본 리사이징 사이즈 (3000px)

        self.__update_size_info()

        self.on_accepted = None

    def bind_ui(self):
        self.axis_option_box.currentIndexChanged.connect(self.on_axis_option_box_index_changed)
        self.axis_option_box.setToolTip("순서대로 가로/세로/장축/단축 기준으로 리사이즈 됩니다.")

        self.resize_value_box.valueChanged.connect(self.on_change_resize_value)
        self.resize_value_box.setToolTip("체크된 높이 기준으로 리사이즈 됩니다.")

    def init_options(self):
        self.axis_option_box.addItems(['Width', 'Height', 'Longest', 'Shortest'])

    def on_call(self):
        self.__update_ui()
        self.show()
          
    def __update_ui(self):
        index = UserConfig.resize_axis
        self.axis_option_box.setCurrentIndex(index)

        size = UserConfig.resize_size
        self.resize_value_box.setValue(size)

    def on_axis_option_box_index_changed(self, index):
        self.axis_option = index

    def on_change_resize_value(self):
        self.resize_value = self.resize_value_box.value()

    def __update_size_info(self):
        '''
        self.width = int(self.width_spinbox.value())
        self.height = int(self.height_spinbox.value())
        '''

    def accept(self) -> None:
        self.__update_size_info()
        if self.on_accepted:
            print(self.axis_option, self.resize_value)
            UserConfig.resize_axis = self.axis_option
            UserConfig.resize_size = self.resize_value
            UserConfig.save()

            self.on_accepted(self.axis_option, self.resize_value)
        super().accept()
