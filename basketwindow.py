import sqlite3
from datetime import datetime
from db import DataBase
from ui import basketUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from create_pdf import create_pdf
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem, QMessageBox

class BasketWindow(QtWidgets.QMainWindow, basketUi.Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setFixedSize(self.size())

		self.comboBox.activated.connect(self.set_image)
		self.pushButtonAdd.clicked.connect(self.append_in_basket)
		self.pushButtonBack.clicked.connect(self.open_primary_window)
		self.pushButtonCheckout.clicked.connect(self.make_an_order)
		self.pushButtonDelete.clicked.connect(self.delete_detail)
		
		

		self.db = DataBase('radio_component.db')
		data = self.db.get_all('stoc')

		for detail in data:
			d = f'{detail[0]} {detail[1]}'
			self.comboBox.addItem(d)
			#print(detail)

		self.set_tablewidget()
		self.tableWidget.setHorizontalHeaderLabels(["id", "название", "количество", "цена (руб)"])
		self.IntValidator = QIntValidator()
		self.lineEditCount.setValidator(self.IntValidator)
		self.tableWidget.resizeColumnsToContents()


	def set_image(self):
		text = self.comboBox.currentText()
		id_detail = int(text[:2])
		img = self.db.get_path_to_image('stoc', id_detail)
		pixmap = QPixmap(img[0][0])
		self.labelImage.setPixmap(pixmap)

		count = self.check_count_in_basket(id_detail)
		self.lineEditCount.setPlaceholderText(f"на складе: {count}")
		
	def set_tablewidget(self):
		data = self.db.get_all('basket')
		if len(data) == 0:
			row = 0
			vol = 0
		else:
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

	def append_in_basket(self):
		text = self.comboBox.currentText()
		id_detail = int(text[:2])

		detail = self.db.get_part_by_id('stoc', id_detail)

		#пытаемся получить количетво
		while True:
			try:
				count = int(self.lineEditCount.text())
				break
			except ValueError:
				msg = QMessageBox()
				msg.setMinimumHeight(500)
				msg.setIcon(QMessageBox.Warning)
				msg.setWindowTitle("Количество")
				msg.setInformativeText("Вы не ввели количество!")
				msg.exec()
				return True

		#пытаемся добавить новую деталь на склад
		try:
			count_in_stoc = self.db.get_count('stoc', id_detail) - self.db.get_count('basket', id_detail)
			#print(count_in_stoc)
			if count_in_stoc < count:
				msg = QMessageBox()
				msg.setMinimumHeight(500)
				msg.setIcon(QMessageBox.Warning)
				msg.setWindowTitle("Количество")
				msg.setInformativeText("На складе мень деталей!")
				msg.exec()
			else:	
				#       id         name              price
				data = (detail[0], detail[1], count, detail[5])
				self.db.append_in_basket(data)

				img = '/img/безшовные-раскосные-прямые-линии-печать-ткани-тонны-моря-узкие-149741474.jpg'
				pixmap = QPixmap(img)
				self.labelImage.setPixmap(pixmap)
				
				self.lineEditCount.clear()
				self.set_tablewidget()
		#если пользователь пытается добавить уже существующий компонент, то просто обновляем кол-во
		except sqlite3.IntegrityError:
			self.db.update_count('basket', detail[0], count)
			self.set_tablewidget()

	def delete_detail(self):
		if self.tableWidget.currentColumn() == 0:
			id_component = str(self.tableWidget.currentItem().text())
			self.db.delete_form_db('basket', int(id_component))
		self.set_tablewidget()


	def open_primary_window(self):
		#это не красиво и так делать не надо
		from primarywindow import PrimaryWindow
		self.primary = PrimaryWindow()
		self.primary.show()
		self.close()

	def clear_basket(self):
		self.db.delete_all('basket')

	def check_count_in_basket(self, id_detail):
		try:
			return  self.db.get_count('stoc', id_detail) - self.db.get_count('basket', id_detail)
		except TypeError:
			return self.db.get_count('stoc', id_detail)
	
	def make_an_order(self):
		data = self.db.get_all('basket')
		self.db.update_stoc(data)
		self.write_in_story()
		create_pdf(data)
		self.clear_basket()
		self.set_tablewidget()

		msg = QMessageBox()
		msg.setMinimumHeight(500)
		msg.setIcon(QMessageBox.Information)
		msg.setWindowTitle("Заказ")
		msg.setInformativeText("Составлен чек для распечтки")
		msg.exec()

	def write_in_story(self):
		id_component = int(self.db.get_len_db('story'))+1
		time = datetime.now()
		order = self.db.get_all('basket')
		data = (int(id_component), str(time), str(order))
		#print(time)
		self.db.append_in_story(data)
