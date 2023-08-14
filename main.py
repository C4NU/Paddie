import sys	# Module
from PyQt5.QtWidgets import QApplication, QWidget	# PyQt5 GUI Module

import WebP_module


class MyApp(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
        
	def initUI(self):
		self.setWindowTitle('My First Application')
		self.move(300, 300)
		self.resize(400, 200)
		self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())