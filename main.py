from PyQt5.QtWidgets import QMainWindow, QApplication	# PyQt5 모듈
from PyQt5.QtGui import QIcon	# PyQt5 icon 모듈

import sys	# 시스템 모듈
import os

import WebP_module as webp	# WebP 변환 모듈


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