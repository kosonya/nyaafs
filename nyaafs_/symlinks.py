#!/usr/bin/env python
#-*- coding: utf-8 -*-
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
# $Id$

from nyaerror import NyaError
import errno

class symlimks(object):
    def __init__(self, cursor, base):
        self.db = base
        self.cu = cursor
        self.cu.execute("""SELECT name FROM sqlite_master WHERE \
name = 'sys_symlinks'""")
        result = self.cu.fetchall()
        #FIXME какая то фигня, он все равно пытается создать таблицу
        if len(result) ==0:
            self.cu.execute("""CREATE TABLE sys_symliks(\
id INTEGER NOT NULL PRIMARY KEY,\
dir_id INTEGER NOT NULL,\
name TEXT NOT NULL,\
target TEXT NOT NULL)""")
            self.db.commit()
        
    def drop(self):
        self.cu.execute("""DROP TABLE sys_symlinks""")
        self.db.commit()
        
    def add_link(self, dir_id, name, target):
        self.cu.execute("SELECT * FROM sys_symlinks\
        WHERE dir_id = %d AND name = '%s'" % (dir_id, name))
        result = self.cu.fetchall()
        if len(result) != 0:
            raise NyaError("Link allready exists!", self.__class__, "add_link", fatal = False, errno=errno.EEXIST)
        self.cu.execute("INSERT INTO sys_symlinks\
        dir_id, name, target) VALUES (%d, '%s', '%s')"\
        % (dir_id, name, target))
        self.db.commit()
            
    def del_link(self, dir_id, name):
        self.cu.execute("DELETE FROM sys_symlinks\
        WHERE dir_id = %d AND name = '%s'"\
        % (dir_id, name))
        self.db.commit()
        
    def follow_link(self, dir_id, name):
        self.cu.execute("SELECT target FROM sys_symlinks\
        WHERE dir_id = %d AND name = '%s'"\
        % (dir_id, name))
        result = self.cu.fetchall()
        if len(result) == 0:
            raise NyaError("No such link", self.__class__, "follow_link", fatal = False, errno = errno.ENOEXIST)
        return result[0][0]