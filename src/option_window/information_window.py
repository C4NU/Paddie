import os
import sys
import platform
import pathlib
import json
from pathlib import Path

from user_config import UserConfig
from resource_path import resource_path

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QPushButton, QProgressBar, QMessageBox
from update_module import UpdateManager

UI_INFORMATION = "resources/ui/information.ui"
PROGRAM_DATA = "resources/data/program_data.json"

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

		with open(program_data_path, 'r', encoding='utf-8') as f:
			program_data = json.load(f)
			self.program_name = program_data["name"]
			self.program_version = program_data["version"]
			self.program_description = program_data["description"]
			self.program_author = program_data["contact"]
			self.program_license = program_data["license"]
		
		print(f"Program Name: {self.program_name}, Version: {self.program_version}")
		self.default_font = 'Barlow-Light'

		self.update_manager = UpdateManager(self.program_version)
		
		# 업데이트 관련 UI 추가
		self.btn_check_update = QPushButton(self.tr("Check for Updates"))
		self.btn_check_update.clicked.connect(self.on_check_update)
		self.verticalLayout.addWidget(self.btn_check_update)
		
		self.progress_bar = QProgressBar()
		self.progress_bar.setVisible(False)
		self.verticalLayout.addWidget(self.progress_bar)

		self.init()

	def on_check_update(self):
		self.btn_check_update.setEnabled(False)
		self.btn_check_update.setText(self.tr("Checking..."))
		
		has_update, latest_v, url, body = self.update_manager.check_for_update()
		
		if has_update:
			# 서버 정보를 로컬 program_data.json에 동기화
			self.update_manager.sync_program_data(latest_v)
			self.label_version_text.setText(latest_v)
			
			reply = QMessageBox.question(self, self.tr("Update Available"),
										self.tr(f"A new version ({latest_v}) is available.\nDo you want to download and update?"),
										QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
			
			if reply == QMessageBox.StandardButton.Yes:
				self.btn_check_update.setText(self.tr("Downloading..."))
				self.progress_bar.setVisible(True)
				self.update_manager.start_download(url, self.update_progress, self.update_finished)
			else:
				self.btn_check_update.setEnabled(True)
				self.btn_check_update.setText(self.tr("Check for Updates"))
		else:
			QMessageBox.information(self, self.tr("No Update"), self.tr("You are using the latest version."))
			self.btn_check_update.setEnabled(True)
			self.btn_check_update.setText(self.tr("Check for Updates"))

	def update_progress(self, value):
		self.progress_bar.setValue(value)

	def update_finished(self, success, message):
		if success:
			self.btn_check_update.setText(self.tr("Installing..."))
			QMessageBox.information(self, self.tr("Download Complete"), 
									self.tr("Download finished. The app will restart to apply the update."))
			self.update_manager.apply_update(message)
		else:
			QMessageBox.warning(self, self.tr("Update Failed"), self.tr(f"Error: {message}"))
			self.btn_check_update.setEnabled(True)
			self.btn_check_update.setText(self.tr("Check for Updates"))
			self.progress_bar.setVisible(False)

	def init(self):
		# 프로그램 정보 텍스트 설정
		self.label_program_text.setText(self.program_name)
		self.label_version_text.setText(self.program_version)
		self.label_contact_text.setText(self.program_author)
		self.label_license_text.setText(self.program_license)