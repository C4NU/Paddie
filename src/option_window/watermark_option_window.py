import os
import sys
import platform

from PyQt6 import uic
from PyQt6.QtWidgets import QDialogButtonBox, QDialog, QCheckBox, QSpinBox, QPushButton

if platform.system() == "Windows":
	form = os.path.join(os.getcwd(), "../resources/WatermarkOptions.ui")
else:
	# build 완료된 exec 에서는 실행이 되지만, 단순 py 로 실행할때는 라이브러리 경로를 참조함
	form = os.path.join(os.path.dirname(sys.executable), "../resources/WatermarkOptions.ui")

try:
	formClass = uic.loadUiType(form)[0]
except:
	formClass = uic.loadUiType(os.path.join(os.getcwd(), "../resources/WatermarkOptions.ui"))[0]

class WatermarkOptionWindow(QDialog, formClass):
	def __init__(self):
		super().__init__()

		