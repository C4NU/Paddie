# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PyQt5.QtWidgets import *
from PyQt5 import uic
########################################
import sys  # 시스템 모듈
import os
########################################
import webp_window as Webp
########################################


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


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
