# Copyright 2023 Eugene Kim (komastar) komastar.photo@gmail.com
import os
import sys
import platform

from PyQt6 import uic
from PyQt6.QtWidgets import QDialogButtonBox, QSpinBox, QDialog

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

        self.resize_option_button_box: QDialogButtonBox
        self.width_spinbox: QSpinBox
        self.height_spinbox: QSpinBox
        self.setupUi(self)

        self.width = 0
        self.height = 0
        self.__update_size_info()

        self.on_accepted = None

    def __update_size_info(self):
        self.width = int(self.width_spinbox.value())
        self.height = int(self.height_spinbox.value())

    def accept(self) -> None:
        self.__update_size_info()
        if self.on_accepted:
            self.on_accepted(self.width, self.height)
        super().accept()
