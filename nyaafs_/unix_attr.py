#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Maxim Kovalev
#
# This file is part of NyaaFS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# $Id: unix_attr.py 78 2009-06-03 20:11:22Z Maxim.Kovalev $

import nyastat
from nyaerror import NyaError

"""
Универсальный модуль для создания таблиц соответствия между объектами,
определяемыми по ID (файлы, директории или что-то иное), и набором
значений атрибутов, отределяемых стандартом POSIX.
"""
# Макс, предлагаю для уменьшения срача котябы объеты именовать по типу 
# СловоСловоСлово
class unix_attr(object):
    def __init__(self, name, cursor, base):
        self.base = base
        self.cu = cursor
        self.name = name
        self.cu.execute("SELECT name FROM sqlite_master WHERE name\
        = '%s_uattr'" % self.name)
        result = self.cu.fetchall()
        if len(result) != 1:
            self.cu.execute("CREATE TABLE %s_uattr(\
id INTEGER NOT NULL PRIMARY KEY,\
st_dev INTEGER DEFAULT 0,\
st_ino INTEGER NOT NULL DEFAULT 0,\
st_mode INTEGER NOT NULL DEFAULT 666,\
st_nlink INTEGER NOT NULL DEFAULT 1,\
st_uid INTEGER NOT NULL DEFAULT 0,\
st_gid INTEGER NOT NULL DEFAULT 0,\
st_rdev INTEGER DEFAULT 0,\
st_size INTEGER NOT NULL DEFAULT 0,\
st_blksize INTEGER DEFAULT 0,\
st_blocks INTEGER NOT NULL DEFAULT 0,\
st_atime INTEGER NOT NULL DEFAULT 0,\
st_mtime INTEGER NOT NULL DEFAULT 0,\
st_ctime INTEGER NOT NULL DEFAULT 0)\
                " % self.name)
            # FIXED: изменен порядок следования на правильный,
            #   убраны невнятные NULL-ы
            self.base.commit()
    
    def add_item(self, id, attrs):
        #FIXME --- проверить, все ли необходимые аргументы переданы
        # raise NyaError("Не все аргументы переданы", sefl.__class__, \
                # "add_item")
        #FIXME --- проверить, нет ли уже такого элемента в таблице
        # raise NyaError("Элемент %s уже существует" % id, self.__class__, \
                # "add_item")
        #if id != 0:
        #    raise "Hui" # Никто ничего не видел..
        print "unix_attr.add_item %s %s" %(id, attrs)
        self.cu.execute("SELECT * FROM %s_uattr WHERE id = %d"%\
                        (self.name, id))
        res = self.cu.fetchall()
        if len(res) != 0:
            raise NyaError("Элемент %s уже существует" % id, self.__class__, \
                 "add_item")
        self.cu.execute("INSERT INTO %s_uattr (id) VALUES (%d)" %\
                         (self.name, id))
        self.base.commit()
        self.edit_item(id, attrs)
        self.base.commit()
    def edit_item(self, id, attrs):
        #FIXME --- проверить существоование элемента с данным id
        # raise NyaError("Элемент %s не существует" % id, self.__class__, \
                # "edit_item")
        # FIXME: attrs.keys() не пашет. нужно ручками
        self.cu.execute("SELECT * FROM %s_uattr WHERE id = %d"%\
                        (self.name, id))
        res = self.cu.fetchall()
        if len(res) == 0:
            raise NyaError("Элемент %s не существует" % id, self.__class__, \
                 "edit_item")

        
        print "unix_attr.edit_item() %s %s" %(id, attrs)
        for attr in attrs.keys():
            self.cu.execute("UPDATE %s_uattr SET '%s' = %d\
            WHERE id = %d" %\
                            (self.name, attr, attrs[attr], id))
            self.base.commit()
        print self.cu.execute("SELECT * FROM %s_uattr" % self.name).fetchall()

    def delete_item(self, id):
        #FIXME --- проверить существование элемента с таким id
        # raise NyaError("Элемент %s не существует" % id, self.__class__, \
                # "delete_item")
        self.cu.execute("DELETE FROM %s_uattr WHERE id = %d" %\
                        (self.name, id))
        self.base.commit()
        
    def drop(self):
        self.cu.execute("DROP TABLE %s_uattr" % self.name)
        # Макс, а зачем при удалении класса unix_attr сносить соответсвующую
        # атрибню? нам разве не надо ее постоянно хранить?
        self.base.commit()

    def get_attr(self, id):
        request = "SELECT * FROM %s_uattr WHERE id = %d"\
                        % (self.name, id)
        print "unix_attr.get_attr: ", request
        self.cu.execute(request)
        result = self.cu.fetchall()
        #print result
        if len(result) == 0:
            raise NyaError("No such id!", eclass=self.__class__, \
                    efunc="get_attr")

#        print result[0][1:]
        ns = nyastat.NyaStat(result[0][1:])
#        print ns
        return ns
