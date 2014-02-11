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
import hierarchy

class xattr_tree(object):
    def __init__(self, path, cursor, base, xattr):
           self.path = path
           self.cu = cursor
           self.db = base
           self.xattr = xattr
           
    def get_root_subdirs(self, ids, attr):
        dirs = []
        for id in ids:
            result = xattr.get_attr(id, attr)
            if result not in ids:
                dirs.append(result)
        return dirs
    
    def get_files(self, ids, attr, value):
        files = []
        for id in ids:
            result = xattr.get_attr(id, attr)
            if result == value:
                if id not in files:
                    files.append(id)
        return files