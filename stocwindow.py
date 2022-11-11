import os
import sqlite3
from db import DataBase
from ui import addUi
from ui import stocUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem, QFileDialog, QMessageBox


class StocWindow(QtWidgets.QMainWindow, stocUi.Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setFixedSize(self.size())
		self.tableWidget.itemClicked.connect(self.set_image)
		self.pushButtonBack.clicked.connect(self.open_primary_window)
		self.pushButtonAdd.clicked.connect(self.open_add_window)
		self.pushButtonDelete.clicked.connect(self.delete_detail)
		self.pushButtonRefresh.clicked.connect(self.set_tablewidget)
		self.set_tablewidget()
		self.tableWidget.setHorizontalHeaderLabels(["id", "название", "материал", "описание", "количество",
													"цена (руб)", "пуить к изображению"])
		self.tableWidget.resizeColumnsToContents()


	def set_tablewidget(self):
		self.db = DataBase('radio_component.db')
		self.data = self.db.get_all('stoc')
		#получение длины столбцов и строк
		if len(self.data) == 0:
			row = 0
			vol = 0
		else:
			row = len(self.data)
			vol = len(self.data[0])

		self.tableWidget.setColumnCount(vol)
		self.tableWidget.setRowCount(row)

		#Запрет на изменение данных в таблице
		self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

		#Заполнение таблины
		for i in range(row):
			for j in range(vol):
				temp_data = self.data[i][j]
				data1 = QTableWidgetItem(str(temp_data))
				self.tableWidget.setItem(i,j, data1)
		self.show()

	def open_primary_window(self):
		#это не красиво и так делать не надо
		from primarywindow import PrimaryWindow
		self.primary = PrimaryWindow()
		self.primary.show()
		self.close()

	def open_add_window(self):
		self.add = AddWindow()
		self.add.show()
		#print(self.tableWidget.currentColumn())

	def set_image(self):
		if self.tableWidget.currentColumn() == 0:
			id_component = str(self.tableWidget.currentItem().text())
			path_to_image = self.db.get_path_to_image('stoc', id_component)
			pixmap = QPixmap(path_to_image[0][0])
			self.labelImage.setPixmap(pixmap)
		else:
			row = self.tableWidget.currentRow()
			id_component = str(self.tableWidget.item(row, 0).text())
			path_to_image = self.db.get_path_to_image('stoc', id_component)
			pixmap = QPixmap(path_to_image[0][0])
			self.labelImage.setPixmap(pixmap)

	def delete_detail(self):
		if self.tableWidget.currentColumn() == 0:
			id_component = str(self.tableWidget.currentItem().text())

			msg = QMessageBox()
			msg.setMinimumHeight(500)
			msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
			msg.setIcon(QMessageBox.Warning)
			msg.setWindowTitle("Удалить")
			msg.setInformativeText("Вы хотите удалить безвозвратно элемент?")
			returnvalue = msg.exec()

			if returnvalue == QMessageBox.Yes:
				self.db.delete_form_db('stoc', int(id_component))
		self.set_tablewidget()


class AddWindow(QtWidgets.QMainWindow, addUi.Ui_AddWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.pushButton.clicked.connect(self.add_detail)
		self.pushButtonAddImage.clicked.connect(self.add_image)
		self.comboBox.activated.connect(self.set_image)
		self.IntValidator = QIntValidator()
		self.lineEdit.setValidator(self.IntValidator)
		self.lineEdit_2.setValidator(self.IntValidator)

		self.db = DataBase('radio_component.db')
		self.data = self.db.get_all('dataset')

		#заполнение combobox
		for detail in self.data:
			d = f'{detail[0]} {detail[1]}'
			self.comboBox.addItem(d)
			#print(detail)


	def set_image(self):
		text = self.comboBox.currentText()
		id_detail = int(text[:2])
		img = self.db.get_path_to_image('dataset', id_detail)
		pixmap = QPixmap(img[0][0])
		self.labelImage.setPixmap(pixmap)


	def add_detail(self):
		text = self.comboBox.currentText()
		id_detail = int(text[:2])
		
		detail = self.db.get_part_by_id('dataset', id_detail)

		#пытаемся получить количетво
		while True:
			try:
				count = int(self.lineEdit.text())
				price = int(self.lineEdit_2.text())
				break
			except ValueError:
				msg = QMessageBox()
				msg.setMinimumHeight(500)
				msg.setIcon(QMessageBox.Warning)
				msg.setWindowTitle("Количество")
				msg.setInformativeText("Вы не ввели количество!")
				msg.exec()
				return True

		#пытаемся добавить изображениек детали
		try:
			image = file_name
		except NameError:
			image = detail[4]

		#пытаемся добавить новую деталь на склад
		try:
			#       id         name       material   description
			data = (detail[0], detail[1], detail[2], detail[3], count, price, image)
			self.db.append_in_db('stoc', data)
			self.labelImage.clear()
			self.lineEdit.clear()
		#если пользователь пытается добавить уже существующий компонент, то просто обновляем кол-во
		except sqlite3.IntegrityError:
			self.db.update_count('stoc', detail[0], count)

	
	def add_image(self):
		global file_name
		file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
		pixmap = QPixmap(file_name)
		self.labelImage.setPixmap(pixmap)
