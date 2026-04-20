import os
import sys
import platform

from PySide6.QtWidgets import QDialogButtonBox, QDialog, QCheckBox, QSpinBox, QPushButton

from resource_path import resource_path
from ui_loader import load_ui

UI_WATERMARK_OPTION = "resources/ui/watermarkoptions.ui"

try:
     # UI 파일 로드
     ui_path = resource_path(UI_WATERMARK_OPTION)

except Exception as e:
     print(f"Resource loading failed: {str(e)}")
     sys.exit(1)

print("WATERMARK OPTION UI Loaded Successfully")

class WatermarkOptionWindow(QDialog):
     def __init__(self):
          super().__init__()
          load_ui(self, ui_path)
