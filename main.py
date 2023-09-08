# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5 import uic
########################################
import sys	# 시스템 모듈
import os
import platform
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

		self.loselessOpt = False
		self.imageQualityOpt = 80
		self.exifOpt = False
		self.iccProfileOpt = False
		self.exactOpt = False
		
		self.conversionOption = False	# webp 변환하는지 선택
		
		# Exif Options 관련 변수
		self.exifPaddingOpt = False	# Exif Padding 을 enable 할 지에 대한 변수
		self.saveFormatIndex = 0	# JPG, PNG, WebP 파일 형식중 고른 값에 대한 변수
		
		#self.watermark = []

		self.setupUi(self)
		
		# 실행 버튼 함수 링킹
		self.SaveButton.clicked.connect(self.okButtonClicked)
		# 파일 추가 버튼 함수 링킹
		self.actionAdd_Files.triggered.connect(self.addFileButtonClicked)
		# 종료 버튼 함수 링킹
		self.actionExit.triggered.connect(self.exitButtonClicked)

		self.ConversionEnableBox.stateChanged.connect(self.ConvsersionState)
		# Loseless 옵션 링킹
		self.LoselessOptionBox.stateChanged.connect(self.LoselessOption)
		# 이미지 퀄리티 옵션 링킹
		self.ImageQualityBox.valueChanged.connect(self.ImageQualityOption)
		# Exif 정보 저장 옵션 링킹
		self.ExifOptionBox.stateChanged.connect(self.ExifOption)
		self.ExactOptionBox.stateChanged.connect(self.ExactOption)
		self.ICCProfileOptionBox.stateChanged.connect(self.IccProfileOption)

		# Watermark 옵션
		#self.watermarkFontColorBox.stateChanged.connect(self.WatermarkColorOption)

		# ExifView 옵션
		self.EnableExifPadding.stateChanged.connect(self.ExifPaddingOption)
		self.SaveFormatBox.currentIndexChanged.connect(self.ExifSaveFormatOption)
		self.InitOptions()

	#################### PyQt5 FUNCTIONS
	def InitOptions(self):
		####################	이미지 품질 관련 옵션
		self.conversionOption = self.ConversionEnableBox.isChecked()
		####################	이미지 품질 관련 옵션
		self.loselessOpt = self.LoselessOptionBox.isChecked()
		self.imageQualityOpt = self.ImageQualityBox.value()
		self.exifOpt = self.ExifOptionBox.isChecked()
		self.iccProfileOpt = self.ICCProfileOptionBox.isChecked()
		self.exactOpt = self.ExactOptionBox.isChecked()
		####################	워터마크 관련 옵션
		#self.watermark = self.watermarkBox.toPlainText()
		#self.watermarkFontColor = self.watermarkFontColorBox.isChecked()
		####################	하단 EXIF 삽입 관련 옵션
		self.exifPaddingOpt = self.EnableExifPadding.isChecked()
		self.saveFormatIndex = self.SaveFormatBox.currentIndex()

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
		# ISSUE: 파일 로딩할때 특정 이미지 파일이 누워서 로딩됨 / 혹은 저장할때?
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
		#self.watermarkOption()
		savePath = QFileDialog.getSaveFileName(None, 'Save File', self.fileName[0])
		
		try:
			if savePath[0]:
				strSavePath = savePath[0]
				strSavePath = strSavePath[:strSavePath.rfind("/")]
			
				# 01 WebP 이미지로만 변환할 때
				if self.conversionOption == True:
					for index in range(self.listWidget.count()):
						self.converter.ConvertImageToWebP(self.listWidget.item(index).text(), strSavePath+'/', 
						self.fileName[index], self.loselessOpt, self.imageQualityOpt, exifOpt=self.exifOpt, iccProfileOpt=self.iccProfileOpt, exactOpt=self.exactOpt, watermarkText="", exifViewOpt=self.exifPaddingOpt,
						conversionOpt = self.conversionOption)

				# 02 Exif Padding 이미지로만 변환할때
				elif self.exifPaddingOpt == True:
					for index in range(self.listWidget.count()):
						self.converter.ConvertExifImage(filePath=self.listWidget.item(index).text(), savePath=strSavePath+'/', 
						saveName=self.fileName[index], fileFormatOpt=self.saveFormatIndex)

				else:
					print("옵션 선택 에러 / 다시 선택해주세요")

				if(platform.system() == "Windows"):	#Windows
					os.startfile(strSavePath)
				elif(platform.system() == "Darwin"):	#macOS
					os.system("open "+'"'+strSavePath+'"')

				self.listWidget.clear()
				self.fileName.clear()
		except:
			if(platform.system() == "Windows"):
				pass#os.system('pause')
			elif(platform.system() == "Darwin"):
				input("엔터를 눌러 진행...")
			return

	def ConvsersionState(self, state):
		if state == Qt.Checked:
			self.conversionOption = True
		else:
			self.conversionOption = False

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
		self.imageQualityOpt = self.ImageQualityBox.value()

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

	# 워터마크 옵션
	def WatermarkColorOption(self, state):
		if state == Qt.Checked:
			self.watermarkOption = True
		else:
			self.watermarkOption = False

	# Exif Padding 옵션
	def ExifPaddingOption(self, state):
		if state == Qt.Checked:
			self.exifPaddingOpt = True
		else:
			self.exifPaddingOpt = False
	
	def ExifSaveFormatOption(self):
		self.saveFormatIndex = self.SaveFormatBox.currentIndex()

def main():
	try:
		os.chdir(sys._MEIPASS)
		print(sys._MEIPASS)
	except:
		os.chdir(os.getcwd())
		
	app = QApplication(sys.argv) 
	myWindow = WindowClass() 
	myWindow.show()
	app.exec_()

if __name__ == "__main__" :
	main()