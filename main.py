from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5 import uic
########################################
import sys	# 시스템 모듈
import os
from fileinput import filename
########################################
import WebP_module as webp	# WebP 변환 모듈
########################################

#
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
		self.setupUi(self)
		self.buttonBox.clicked.connect(self.okButtonClicked)
		self.actionAdd_Files.triggered.connect(self.addFileButtonClicked)
		self.actionExit.triggered.connect(self.exitButtonClicked)

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
		fname = QFileDialog.getOpenFileName(self, 'Open File', './')
		self.LoadFile(fname[0])

	def exitButtonClicked(self):
		exit()
		
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
		savePath = QFileDialog.getSaveFileName(None, 'Save File', self.fileName[0])
		if savePath[0]:
			strSavePath = savePath[0]
			strSavePath = strSavePath[:strSavePath.rfind("/")]
			for index in range(self.listWidget.count()):
				self.converter.ConvertImage(self.listWidget.item(index).text(), strSavePath+'/', self.fileName[index])
		
		self.listWidget.clear()
		self.fileName.clear()

def main():
	app = QApplication(sys.argv) 
	myWindow = WindowClass() 
	myWindow.show()
	app.exec_()

if __name__ == "__main__" :
	main()