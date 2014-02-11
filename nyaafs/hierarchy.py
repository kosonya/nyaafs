#-*- coding: utf-8 -*-
"""Иерархия является обобщением понятия дерева директорий. Пользователь может сам создавать свои иерархии, тогда как иерархия с именем default существует всегда и отвечает за обычное дерево директорий."""
#FIXME --- добавить возможность добавления атрибутов к директориям.
class hierarchy:
	"""Единсственный класс отвечает сразу за всю иерархию, подробнее смотри в описании модуля."""
	def __init__(self, name, cursor, base):
		"""Конструктор принимает имя иерархии, курсор базы данных и её объект-соединение. Если находит в базе иерархию с переданным именем, то подключается к ней, если же нет --- создаёт новую."""
		#FIXME --- да, чуть не забыл. Создание иерарзии требует, чтобы в базе существовала таблица sys_file_id, в которой хранится связь между ID файлов и их именами. Надо бы этот факт проверять, а в случае отсутствия выкидывать исключение.
		self.cu = cursor
		self.name = name
		self.db = base
		self.cu.execute("SELECT name FROM sqlite_master WHERE name LIKE 'hierarchy_%s_%%'" % self.name)
		#FIXME Ёбаный стыд, сраный SQLite не поддерживает сраные схемы. Это печально. Придётся делать руками быдлопространства имён с помощью подчёркиваний.
		result = self.cu.fetchall()
		if self.cu.rowcount!=3 :
			#FIXME --- Вообще-то возможны три варианта: либо нужных таблиц вообще нет, либо их правильное количество (я думал, что три, но забыл про атрибуты для директорий, возможно на самом деле должно быть четыре), либо их какое-то другое число. В первом случае такие таблицы создаются, во втором ничего не происходит, а вот для третьего надо сочинить исключение.
			self.cu.execute("CREATE TABLE hierarchy_%s_dir_id (\
id INTEGER NOT NULL,\
name TEXT,\
PRIMARY KEY(id),\
FOREIGN KEY (id)\
REFERENCES hierarchy_%s_dir_hierarchy (id))"\
				% (self.name, self.name))
			self.cu.execute("CREATE TABLE hierarchy_%s_dir_hierarchy (\
id INTEGER NOT NULL,\
parent INTEGER NOT NULL,\
PRIMARY KEY(id),\
FOREIGN KEY(parent)\
REFERENCES hierarchy_%s_dir_hierarchy (id),\
FOREIGN KEY(id)\
REFERENCES hierarchy_%s_dir_id (id))" % (self.name, self.name, self.name))
			self.cu.execute("CREATE TABLE hierarchy_%s_file_parents(\
file_id INTEGER NOT NULL,\
parent INTEGER NOT NULL,\
PRIMARY KEY(file_id),\
FOREIGN KEY(parent)\
REFERENCES hierarchy_%s_dir_id(id))"\
				% (self.name, self.name))
			self.cu.execute("""INSERT INTO hierarchy_%s_dir_id VALUES (0, 'root')""" % self.name)
			#FIXME --- для всей этой херни надо добавить исключения на случай, если хоть что-нибудь из этой цепочки не удастся сделать.
			self.db.commit()
			#По-моему, SQLite автоматом коммитит вообще все транзакции. Это херня какая-то, так что на всякий случай пишу руками везде, где это действительно нужно. Лишним не будет, а не исключено, что автоматический коммит можно отключить, это понадобится для создания нормальной журналиромоей FS

	def find_by_path(self, path):
		"""Поиск ID файла или директории по указанному абсолютному пути. Принимает список строк, первой обязательно должна быть "root", остальные --- элементы пути. Возвращает кортеж из ID, строки с именем (ну и нафига я это сделал, скажите пожалуйста?) и строки "dir" или "file" в зависимости от того, что является послежним элементом пути (собственно искомым файлом)"""
		#FIXME --- добавить исключение на случай, если первым элементом пути НЕ является строка "root"
		def file_or_dir(self, dir_id, name):
			"""Поиск файла или директории с указанным именем. ПРинимает ID директории, в которой ищем, и имя файла или директории, котор(ый|ую) ищем. Возвращает кортеж из строки "file" или "dir" в зависимости от того, что нашли (условие: в одной директории не может существовать файла и директории с одинаковыми именами), и ID"""
			#FIXME -- Вот здесь надо как-то (я ещё не придумал, как) сделать исключение для случая, когда искомого файла вообще не существует. То есть, проверяем, есть ли директория с таким именем, если нет --- есть ли файл с таким именем, а если вообще нифига нет, то надо бы исключение выкинуть
			self.cu.execute("SELECT I.id FROM hierarchy_%s_dir_id I, hierarchy_%s_dir_hierarchy H\
 WHERE H.parent = %d AND I.name = '%s' AND I.id = H.id" % (self.name, self.name, dir_id, name))
			result = self.cu.fetchall()
			if self.cu.rowcount == 1:
				return ("dir", result[0][0])
			self.cu.execute("SELECT SF.id FROM sys_file_id SF, hierarchy_%s_file_parents FP\
 WHERE FP.parent = %d AND SF.name = '%s' AND FP.file_id = SF.id" % (self.name, dir_id, name))
			result = self.cu.fetchall()
			return ("file", result[0][0])

		def add_to_request(self, request, path):
			"""Сугубо служебная функция, нужная для формаирования подчинённого SQL-запроса по переаднному пути. Будучи рекурсивной, принимает баазовый запрос, который должен давать ID директории, в которой будем искать слудующую, и путь. Возвращает запрос, который ищет следующий элемент пути в найденной директории."""
			if (len(path) <= 2):
				return request
			else:
				return ("SELECT DIH.id FROM hierarchy_%s_dir_id DID, hierarchy_%s_dir_hierarchy DIH\
 WHERE DID.name = '%s' AND DIH.parent = (%s) AND DID.id = DIH.id"\
					% (self.name, self.name, path[-1], add_to_request(self, request, path[:-1])))

		if len(path) == 1:
			#Если путь длины 1 - то это просто строка "root" (это нам гарантирует исключение, которое должно быть вставлено выше), а значит смело возвращем ID 0 (см. на конструктор --- корневая директория всегда имеет ID 0)
			return "dir", 0
		elif len(path) == 2:
			#Если в пути два элемента, то мы точно знаем, что второй является файлом или  директорией, лежащей в корневой.
			return file_or_dir(self, 0, path[-1])

		else:
			#Понеслась моча по трубам...
			request = ("SELECT DIH.id FROM hierarchy_%s_dir_id DID, hierarchy_%s_dir_hierarchy\
 DIH WHERE DIH.parent = 0 AND DID.name = '%s' AND DID.id = DIH.id" % (self.name, self.name, path[1]))
			request = add_to_request(self, request, path[:-1])
			self.cu.execute(request)
			result = self.cu.fetchall()
			#FIXME -- Надо добавить исключение на случай некорректного пути. Это как минимум. Как максимум --- два исключения. Первое ловит отсуствие той или иной директории в пути. Второе ловит случай того, что файл является не последним элементом пути.
			cwdid = result[0][0]
			return file_or_dir(self, cwdid, path[-1])

	def add_dir_to_dir(self, parent, name):
		"""Создание директории с указанным именем в указанной директории. Принимает ID родительской директории и имя директории, которую хотим создать. Ничего не возвращет (хотя, можно потом чисто по приколу сделать её возвращающей ID созданной директории, благо мы и так его ищем)."""
		#FIXME -- Здесь нужно целых три исключения. Что если не существует директории с переданным в качестве родительского ID? Что если такая директория уже существует? Что если такой файл уже существует?
		self.cu.execute("SELECT DID.id FROM hierarchy_%s_dir_id DID WHERE DID.name = '%s'" % (self.name, name))
		old_state = self.cu.fetchall()
		self.cu.execute("INSERT INTO hierarchy_%s_dir_id (name)\
VALUES ('%s')""" % (self.name, name))
		self.cu.execute("SELECT id FROM hierarchy_%s_dir_id\
 WHERE name = '%s'" % (self.name, name))
		new_state = self.cu.fetchall()
		for item in new_state:
			if item in old_state:
				continue
			else:
				added = item[0]
				break
		self.cu.execute("INSERT INTO hierarchy_%s_dir_hierarchy (id, parent)\
VALUES (%d, %d)" % (self.name, added, parent))
		self.db.commit()
	
	def read_dir(self, dir_id):
		"""Читает список файлов и поддиректорий в данной директории. Принимает ID нужной директории. Возвращает список кортежей из ID, имени и строки "file" или "dir" в зависимости от типа элемента. На будущее неплохо бы прикрутить сортировку результата."""
		#FIXME --- Исключение на случай, если указанной директории не существует.
		self.cu.execute("SELECT DID.id, DID.name FROM hierarchy_%s_dir_id DID, hierarchy_%s_dir_hierarchy DIH WHERE DID.id = DIH.id AND DIH.parent = %d" % (self.name, self.name, dir_id))
		dirs = self.cu.fetchall()
		for i in xrange(len(dirs)):
			id, name = dirs[i]
			dirs[i] = (id, name, "dir")
			#Ядрёна мать, я только сейчас понял, что я здесь сделал: я беру и меняю типы элементов списка, не разрущая сам список. О нет, я безнадёжно подсел на иглу динамической типизации, сам того не заметив ;_;
		self.cu.execute("SELECT SF.id, SF.name FROM hierarchy_%s_file_parents FP, sys_file_id SF WHERE SF.id = FP.file_id AND FP.parent = %d" % (self.name, dir_id))
		files = self.cu.fetchall()
		for i in xrange(len(files)):
			id, name  = files[i]
			files[i] = (id, name, "file")
		return (dirs + files)
	
#FIXME --- Этот модуль выглядит так, будто ему чего-то не хватает...
