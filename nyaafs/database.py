import sqlite as db

class database:
	def __init__(self, name="nyaadb"):
		self.base = db.connect(name)
		self.cursor = self.base.cursor()
		
	def tables_info(self, like="%"):
		self.cursor.execute("SELECT name FROM slite_master WHERE name IS LIKE '%s'" % like)
		return self.cursor.fetchall()

	def sql_request(self, resuest):
		self.cursor.execute(request)
		return self.cursor.fetchall()

	def close(self):
		self.base.close()

	def commit(self):
		self.base.commit()

	def rollback(self):
		self.base.rollback()

	def curclose(self):
		self.cursor.close()

	def reszise(self):
		return self.cursor.arraysize
