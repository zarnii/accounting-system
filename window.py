import sys
import os
import sqlite3
import mainform

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QTableWidget, QTableWidgetItem, QAbstractItemView)
from PyQt5.QtGui import QIcon


class Window(QtWidgets.QMainWindow, mainform.Ui_MainWindow):


	def __init__(self):
		super().__init__()
		self.setupUi(self)

		#self.initUI()

		#подключение к бд (попробовать вынести в другую def)
		conn = sqlite3.connect('radio_component.db')
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM radio_component")
		data = cursor.fetchall()

		#получение длины столбцов и строк
		row = len(data)
		vol = len(data[0])

		self.tableWidget.setColumnCount(vol)
		self.tableWidget.setRowCount(row)

		#Запрет на изменение данных в таблице
		self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

		#Заполнение таблины
		for i in range(row):
			for j in range(vol):
				temp_data = data[i][j]
				data1 = QTableWidgetItem(str(temp_data))
				self.tableWidget.setItem(i,j, data1)
		self.show()



if __name__ == '__main__':
	app = QApplication(sys.argv)

	#Запуск формы главного окна
	window = Window()
	window.show()
	

	#Запуск
	sys.exit(app.exec())