import os
import sys
import platform

from PyQt6 import uic
from PyQt6.QtWidgets import QDialogButtonBox, QDialog, QCheckBox, QSpinBox, QPushButton

from resource_path import resource_path

UI_WATERMARK_OPTION = "resources/ui/WatermarkOptions.ui"

try:
    # UI 파일 로드
    ui_path = resource_path(UI_WATERMARK_OPTION)
    form_class = uic.loadUiType(ui_path)[0]

except Exception as e:
    print(f"Resource loading failed: {str(e)}")
    sys.exit(1)

print("WATERMARK OPTION UI Loaded Successfully")

class WatermarkOptionWindow(QDialog, form_class):
	def __init__(self):
		super().__init__()

		