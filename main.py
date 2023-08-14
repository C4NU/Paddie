from PyQt5.QtWidgets import QMainWindow, QApplication	# PyQt5 모듈
from PyQt5.QtGui import QIcon	# PyQt5 icon 모듈

import sys	# 시스템 모듈

import WebP_module as webp	# WebP 변환 모듈


class MainWidget(QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle("WebP Converter")
		self.setWindowIcon(QIcon('Icon.ico'))
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
			print(f)
			webp.Converter.ConvertImage(f)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ui = MainWidget()
	ui.show()
	sys.exit(app.exec_())