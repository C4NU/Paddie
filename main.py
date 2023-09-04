# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5 import uic
########################################
import sys	# 시스템 모듈
import os
import platform
import subprocess
import logging
########################################
import WebP_module as webp	# WebP 변환 모듈
########################################


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_path, relative_path)

form = resource_path("WebPConverterGUI.ui")
formClass = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, formClass) :
	def __init__(self) :
		super().__init__()
		self.converter = webp.Converter()
		self.fileName = []
		self.loselessOpt = True
		self.imageQualityOpt = 120
		self.exifOpt = True
		self.iccProfileOpt = False
		self.exactOpt = False
		self.watermark = []

		self.setupUi(self)
		
		# 실행 버튼 함수 링킹
		self.buttonBox.clicked.connect(self.okButtonClicked)
		# 파일 추가 버튼 함수 링킹
		self.actionAdd_Files.triggered.connect(self.addFileButtonClicked)
		# 종료 버튼 함수 링킹
		self.actionExit.triggered.connect(self.exitButtonClicked)
		# Loseless 옵션 링킹
		self.LoselessOptionBox.stateChanged.connect(self.LoselessOption)
		# 이미지 퀄리티 옵션 링킹
		self.ImageQualityBox.valueChanged.connect(self.ImageQualityOption)
		# Exif 정보 저장 옵션 링킹
		self.ExifOptionBox.stateChanged.connect(self.ExifOption)
		self.ExactOptionBox.stateChanged.connect(self.ExactOption)
		self.ICCProfileOptionBox.stateChanged.connect(self.IccProfileOption)

		# Watermark 옵션
		self.watermarkFontColorBox.stateChanged.connect(self.WatermarkColorOption)
		self.InitOptions()

	#################### PyQt5 FUNCTIONS
	def InitOptions(self):
		####################	이미지 품질 관련 옵션
		self.loselessOpt = self.LoselessOptionBox.isChecked()
		self.imageQualityOpt = self.ImageQualityBox.value()
		self.exifOption = self.ExifOptionBox.isChecked()
		self.iccProfileOpt = self.ICCProfileOptionBox.isChecked()
		self.exactOpt = self.ExactOptionBox.isChecked()
		####################	워터마크 관련 옵션
		self.watermark = self.watermarkBox.toPlainText()
		self.watermarkFontColor = self.watermarkFontColorBox.isChecked()

	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		if event.mimeData().hasUrls():
			event.setDropAction(Qt.CopyAction)
			event.accept()

			self.links = []
			# 드래그 드롭시 파일 추가되는 코드
			for url in event.mimeData().urls():
				self.LoadFile(url.toLocalFile())

		else:
			event.ignore()

	def okButtonClicked(self):
		if self.listWidget.count() != 0:
			self.SaveFile()

	def addFileButtonClicked(self):
		fname = QFileDialog.getOpenFileNames(self, 'Open Files...', './')
		if fname == None:
			print("아무 파일 선택 안됨")
		else:
			for name in fname[0]:
				self.LoadFile(name)

	def exitButtonClicked(self):
		sys.exit()

	def watermarkOption(self):
		self.watermark = self.watermarkBox.toPlainText()
		print(self.watermark)
		
	#################### FUNCTIONS
	def LoadFile(self, filePath):
		icon = QtGui.QIcon(filePath)
		item = QtWidgets.QListWidgetItem(icon, filePath)
				
		size = QtCore.QSize()
		size.setHeight(128)
		size.setWidth(128)
				
		item.setSizeHint(size)
		fileName = os.path.splitext(filePath)[0]
		self.fileName.append(fileName.split(sep='/')[-1])
		self.listWidget.addItem(item)

	def SaveFile(self):
		# 변환 실행 버튼 callback 함수
		self.watermarkOption()
		savePath = QFileDialog.getSaveFileName(None, 'Save File', self.fileName[0])
		
		if savePath[0]:
			strSavePath = savePath[0]
			strSavePath = strSavePath[:strSavePath.rfind("/")]
			for index in range(self.listWidget.count()):
				self.converter.ConvertImage(self.listWidget.item(index).text(), strSavePath+'/', 
				self.fileName[index], self.loselessOpt, self.imageQualityOpt, self.exifOpt, self.iccProfileOpt, self.exactOpt, self.watermark)
		
			if(platform.system() == "Windows"):	#Windows
				os.startfile(strSavePath)
			elif(platform.system() == "Darwin"):	#macOS
				subprocess.run(["open", strSavePath])

			self.listWidget.clear()
			self.fileName.clear()
		
		else:
			return

	def IccProfileOption(self, state):
		if state == Qt.Checked:
			self.iccProfileOpt = True
		else:
			self.iccProfileOpt = False

	def LoselessOption(self, state):
		#Qt.checked -> True는 2, False는 0
		if state == Qt.Checked:
			self.loselessOpt = True
		else:
			self.loselessOpt = False

	def ImageQualityOption(self):
		self.imageQualityOpt = self.imageQualityOpt = self.ImageQualityBox.value()

	def ExifOption(self, state):
		if state == Qt.Checked:
			self.exifOpt = True
		else:
			self.exifOpt = False

	def ExactOption(self, state):
		if state == Qt.Checked:
			self.exactOpt = True
		else:
			self.exactOpt = False

	def WatermarkColorOption(self, state):
		if state == Qt.Checked:
			self.watermarkOption = True
		else:
			self.watermarkOption = False
			
def main():
	app = QApplication(sys.argv) 
	myWindow = WindowClass() 
	myWindow.show()
	app.exec_()

if __name__ == "__main__" :
	main()