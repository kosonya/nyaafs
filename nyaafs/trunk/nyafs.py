#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
#
# Copyright (C) 2009 Vladimir Badaev
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
# $Id: nyafs.py 7 2009-05-15 19:13:07Z Vladimir.Badaev $


# imports

# import errno
import fuse
fuse.fuse_python_api = (0,2)

import sqlite3 as db

#
#	NyaDB
#
class	NyaDB(object):
    """
    Класс для работы с базой данных.
    ПреАльфа :)
    """
    def __init__(self):
        """
        Конструктор. Можно добавить пару парамнтров типа имени базы и тд.
        """
        pass
    def __del__(self):
        """
        Деструктор.
        """
        pass

    def getFileAttr(self, path):
        """
        Возвращает NyaStat файла path.
        """
        pass
    def setFileAttr(self, path, nyaStat):
        """
        Изменяет атрибуты файла.
        """
        pass
    def getRealFile(self, path, mode=None):
        """
        Возвращает путь к файлу на хост-фс, по пути path.
        Возможно еще будет нужна проверка прав доступа и тп.
        """
        pass
    def getFilesFromDir(self, path):
        """
        Возвращает список файлов из директории path.
        Возможно как (имя, NyaStat).
        """
        pass
    def newFile(self, path, type, stat):
        """
        ХЗ точно, наверно это будет раз пять переколбашено.
        Ориентировочно: создать новый файл, характеризуемый путем, типом(файл, дирректория етц), и статом.
        """
        pass

    def getFileXAttr(self, *hz):
        """
        Получить расширеные атрибуты файла. Надо поманить, ВТФ оно вообще есть.
        Кста, возможно потом понадобиться функция для получения списка xattr-ов.
        """
        pass
    def setFileXAttr(self, *hz):
        """
        Изменить xattr-ы.
        """
        pass




#
#   NyaStat
#
class	NyaStat(fuse.Stat):
    """
    Стандартная информация о файле, см. stat(2)
    Содержит:
    struct stat {
        dev_t     st_dev;     /* ID of device containing file */
        ino_t     st_ino;     /* inode number */
        mode_t    st_mode;    /* protection */
	    nlink_t   st_nlink;   /* number of hard links */
	    uid_t     st_uid;     /* user ID of owner */
	    gid_t     st_gid;     /* group ID of owner */
	    dev_t     st_rdev;    /* device ID (if special file) */
	    off_t     st_size;    /* total size, in bytes */
	    blksize_t st_blksize; /* blocksize for file system I/O */
	    blkcnt_t  st_blocks;  /* number of 512B blocks allocated */
	    time_t    st_atime;   /* time of last access */
	    time_t    st_mtime;   /* time of last modification */
	    time_t    st_ctime;   /* time of last status change */
    };

    """
    pass


#
#   NyaFile
#
class   NyaFile(object):
    """
    Класс представляет интерфейс к файлу.
    """
    def __init__(self, path, flags, mode=None):
        """
        """
        pass
    def read(self, length, offset, fh=None):
        """
        Чтение из файла.
        """
        pass
    def write(self, buf, offset, fh=None):
        """
        Внезапно запись в файл.
        """
        pass

    def fgetattr(self, fh=None):
        """
        """
        pass

    def ftruncate(self, len, fh=None):
        """
        """
        pass

    def flush(self, fh=None):
        """
        """
        pass

    def release(self, fh=None):
        """
        """
        pass

    def fsync(self, fdatasync, fh=None):
        """
        """
        pass



#
#   NyaFS
#
class   NyaFS(object):
    """
    """

    def __init__(self):
        """
        """
        pass
    def getattr(self, path):
        """
        """
        pass
    def readlink(self, path): 
        """
        """
        pass
    def mknod(self, path, mode, rdev):
        """
        """
        pass
    def mkdir(self, path, mode):
        """
        """
        pass
    def unlink(self, path):
        """
        """
        pass
    def symlink(self, target, name):
        """
        """
        pass
    def rename(self, old, new):
        """
        """
        pass
    def link(self, target, name):
        """
        """
        pass
    def fsinit(self):
        """
        """
        pass


	
