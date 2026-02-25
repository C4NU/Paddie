import os
import sys
import platform
import pathlib
import json
from pathlib import Path

from user_config import UserConfig
from resource_path import resource_path

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QWidget

UI_INFORMATION = "resources/ui/Information.ui"
PROGRAM_DATA = "resources/program_data.json"

try:
	# UI 파일 로드
	ui_path = resource_path(UI_INFORMATION)
	program_data_path = resource_path(PROGRAM_DATA)
	form_class = uic.loadUiType(ui_path)[0]
	
except Exception as e:
	print(f"Resource loading failed: {str(e)}")
	sys.exit(1)

print("INFORMATION UI Loaded Successfully")

class InformationWindow(QWidget, form_class):
	def __init__(self):
		super().__init__()
		self.setupUi(self) # UI 초기화

		with open(program_data_path, 'r') as f:
			program_data = json.load(f)
			self.program_name = program_data["name"]
			self.program_version = program_data["version"]
			self.program_description = program_data["description"]
			self.program_author = program_data["contact"]
			self.program_license = program_data["license"]
		
		print(f"Program Name: {self.program_name}, Version: {self.program_version}")
		self.default_font = 'Barlow-Light'

		self.init()

	def init(self):
		# 프로그램 정보 텍스트 설정
		self.label_program_text.setText(self.program_name)
		self.label_version_text.setText(self.program_version)
		self.label_contact_text.setText(self.program_author)
		self.label_license_text.setText(self.program_license)