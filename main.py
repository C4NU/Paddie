# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PyQt5.QtWidgets import *
from PyQt5 import uic
########################################
import sys  # 시스템 모듈
import os
########################################
import webp_window as Webp
from utils import resource_path
########################################


form = resource_path("WebPConverterGUI.ui")
formClass = uic.loadUiType(form)[0]


def main():
    try:
        os.chdir(sys._MEIPASS)
        print(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())

    app = QApplication(sys.argv)
    app_window = Webp.WebpWindow()
    app_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
