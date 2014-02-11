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

class xattr(object):
    def __init__(self, cursor, base):
        self.cu = cursor
        self.db = base
#        self.cu.execute("SELECT * FROM sqlite_master\
#        WHERE name = 'xattr_%s'" % self.name)
#        result = self.cu.fetchall()
#        if len(result) !=1:
#            self.cu.execute("CREATE TABLE xattr_%s(\
#                                id INTEGER NOT NULL,\
#                                value TEXT NOT NULL)"
#                                % self.name)
#            self.db.commit()
    
    def set_attr(self, id, attr, value):
        self.cu.execute("SELECT name FROM sqlite_master\
        WHERE name = 'xattr_%s'" % attr)
        result = self.cu.fetchall()
        if len(result) == 0:
            self.cu.execute("CREATE TABLE xattr_%s(\
                                id INTEGER NOT NULL,\
                                value TEXT NOT NULL)"
                                % attr)
            self.db.commit()
        self.cu.execute("SELECT id FROM xattr_%s\
        WHERE id = %d" % (attr, id))
        result = self.cu.fetchall()
        if len(result) == 0:
            self.cu.execute("INSERT INTO xattr_%s (id, value)\
            VALUES (%d, '%s')" % (attr, id, value))
        else:
            self.cu.execute("UPDATE xattr_%s SET value = '%s'\
            WHERE id = %d" % (attr, value, id))
        self.db.commit()
        
    def get_attr(self, id, attr):
        print "xattr.get_attr()", id, attr
        self.cu.execute("SELECT name FROM sqlite_master\
        WHERE name = 'xattr_%s'" % attr)
        result = self.cu.fetchall()
        if len(result)!= 1:
            return ''
        self.cu.execute("SELECT value FROM xattr_%s\
        WHERE id = %d" % (attr, id))
        result = self.cu.fetchall()
        if len(result) == 0:
#            raise NyaError("Id %d has not attribute %s" % (id, self.name), self.__class__, "get_attr")
            return ''
        return result[0][0]
    
    def get_ids(self, attr, value=""):
        if value == "":
            self.cu.execute("SELECT id FROM xattr_%s"\
                            % attr)
            result = self.cu.fetchall()
            return map( (lambda x: x[0]), result)
        self.cu.execute("SELECT id FROM xattr_%s\
        WHERE value = '%s'" % (attr, value))
        result = self.cu.fetchall()
        return map( (lambda x: x[0]), result)
    
    def del_id(self, id, attr):
        self.cu.execute("DELETE FROM xattr_%s\
        WHERE id = %d" % (attr, id))
        self.db.commit()
        
    def drop(self, attr):
        self.cu.execute("DROP TABLE xattr_%s" % attr)
        self.db.commit()
        
    def get_possible(self, id):
        self.cu.execute("SELECT name FROM sqlite_master\
        WHERE name LIKE 'xattr%'")
        tables = map( lambda x: x[0], self.cu.fetchall())
        result = []
        for table in tables:
            self.cu.execute("SELECT * FROM xattr_%s\
            WHERE id = %s" % (table, id))
            if len(self.cu.fetchall())!=0:
                result.append(table)
        return result