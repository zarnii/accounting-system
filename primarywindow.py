import sys
#import sqlite3
from stocwindow import StocWindow
from basketwindow import BasketWindow
from ui import primaryUi
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet 

class PrimaryWindow(QtWidgets.QMainWindow, primaryUi.Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setFixedSize(self.size())

		self.pushButtonInStoc.clicked.connect(self.open_stoc_window)
		self.pushButtonCheckout.clicked.connect(self.open_bascket_window)

	def open_stoc_window(self):
		self.stoc = StocWindow()
		self.stoc.show()
		self.close()

	def open_bascket_window(self):
		self.basket = BasketWindow()
		self.basket.show()
		self.close()

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)

	window = PrimaryWindow()
	window.show()

	apply_stylesheet(app, theme='dark_blue.xml')
	sys.exit(app.exec())