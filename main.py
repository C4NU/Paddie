from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import sys	# 시스템 모듈
import os

import WebP_module as webp	# WebP 변환 모듈

formClass = uic.loadUiType("WebPConverterGUI.ui")[0]

class WindowClass(QMainWindow, formClass) :
	def __init__(self) :
		super().__init__()
		self.converter = webp.Converter()
		self.setupUi(self)
		self.listWidget.itemClicked.connect(self.chkItemClicked)
		self.buttonBox.clicked.connect(self.okButtonClicked)

	def chkItemClicked(self):
		print(self.listWidget.currentItem().text())

	def addListWidget(self):
		self.addItemText = self.line_addItem.text()
		self.listWidget.addItem(self.addItemText)

	def insertListWidget(self) :
		self.insertRow = self.spin_insertRow.value()
		self.insertText = self.line_insertItem.text()
		self.listWidget.insertItem(self.insertRow, self.insertText)

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
				if url.isLocalFile():
					self.links.append(str(url.toLocalFile()))
				else:
					self.links.append(str(url.toString()))
			self.listWidget.addItems(self.links)
		else:
			event.ignore()

	def okButtonClicked(self):
		for index in range(self.listWidget.count()):
			print(self.listWidget.item(index).text())
			self.converter.ConvertImage(self.listWidget.item(index).text())
		
		self.listWidget.clear()
	'''
	def dropEvent(self, event):
		files = [u.toLocalFile() for u in event.mimeData().urls()]
		for f in files:
			self.converter.ConvertImage(f)
	'''

if __name__ == "__main__" :
	#QApplication : 프로그램을 실행시켜주는 클래스
	app = QApplication(sys.argv) 

	#WindowClass의 인스턴스 생성
	myWindow = WindowClass() 

	#프로그램 화면을 보여주는 코드
	myWindow.show()

	#프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
	app.exec_()
'''
class MainWidget(QMainWindow):
	def __init__(self):
		super().__init__()
		self.converter = webp.Converter()
		self.initUI()

	def initUI(self):
		self.setWindowTitle("WebP Converter")
		self.setWindowIcon(QIcon('Resources/Icon@64X64_02.ico'))
		self.resize(720, 480)
		self.setAcceptDrops(True)

	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		files = [u.toLocalFile() for u in event.mimeData().urls()]
		for f in files:
			self.converter.ConvertImage(f)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'Resources/Icon@64X64_01.ico')
	app.setWindowIcon(QIcon(path))

	ui = MainWidget()
	ui.show()
	sys.exit(app.exec_())
'''