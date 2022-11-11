import sqlite3

class DataBase():
	def __init__(self, database):
		self.database = database
		self.conn = sqlite3.connect(self.database)
		self.cursor = self.conn.cursor()

	def append_in_db(self, table, value):
		#id, name, material, description, count, price, path_to_img
		self.cursor.execute(f"INSERT INTO {table} VALUES(?,?,?,?,?,?,?);", value)
		self.conn.commit()

	def append_in_basket(self, value):
		self.cursor.execute(f"INSERT INTO basket VALUES(?,?,?,?);", value)
		self.conn.commit()

	def append_in_story(self, value):
		self.cursor.execute(f'INSERT INTO story VALUES(?,?,?);', value)
		self.conn.commit()

	def delete_form_db(self, table, id_component):
		self.cursor.execute(f"DELETE FROM {table} WHERE id = {id_component}")
		self.conn.commit()

	def delete_all(self, table):
		self.cursor.execute(f"DELETE FROM {table}")
		self.conn.commit()
		
	def update_count(self, table, id_component, value):
		self.cursor.execute(f"SELECT count FROM {table} WHERE id = {id_component}")
		count = int(self.cursor.fetchone()[0]) + int(value)
		self.cursor.execute(f"UPDATE {table} SET count = {count} WHERE id = {id_component}")
		self.conn.commit()

	def update_stoc(self, data):
		for i in data:
			id_component = i[0]
			count = self.get_count('basket', id_component)
			self.cursor.execute(f'SELECT count FROM stoc WHERE id = {id_component}')
			count = int(self.cursor.fetchone()[0]) - count
			if count == 0:
				self.cursor.execute(f"DELETE from stoc WHERE id = {id_component}")
			else:
				self.cursor.execute(f"UPDATE stoc SET count = {count} WHERE id = {id_component}")
			self.conn.commit()

	def get_part_by_id(self, table, id_component):
		self.cursor.execute(f"SELECT * FROM {table} WHERE id = {id_component}")
		return self.cursor.fetchone()
		
	def get_count(self, table, id_component):
		try:
			self.cursor.execute(f"SELECT count FROM {table} WHERE id = {id_component}")
			return self.cursor.fetchone()[0]
		except TypeError:
			return 0

	def get_len_db(self, table):
		self.cursor.execute(f'SELECT COUNT(id) from {table}')
		return self.cursor.fetchall()[0][0]

	def get_all(self, table):
		self.cursor.execute(f"SELECT * FROM {table}")
		return self.cursor.fetchall()

	def get_name(self, table):
		self.cursor.execute(f"SELECT name FROM {table}")
		return self.cursor.fetchall()

	def get_path_to_image(self, table, id_component):
		self.cursor.execute(f"SELECT path_to_img FROM {table} WHERE id = {id_component}")
		return self.cursor.fetchall()


#db = DataBase('radio_component.db')
#data = db.get_all('basket')
#db.update_stoc(data)

		