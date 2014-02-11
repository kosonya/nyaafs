#!/usr/bin/env python
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
# $Id: nyastat.py 71 2009-06-03 16:36:24Z Maxim.Kovalev $

#-*- coding: utf-8 -*-

import fuse
fuse.fuse_python_api = (0,2)


class    NyaStat(fuse.Stat):
    """
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
    def __init__(self, params=()):
        fuse.Stat.__init__(self)
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0
        self.st_blocks = 0
        self.st_blksize = 0
        self.st_rdev = 0
        if len(params) == 13:
            print params
            ( \
                    self.st_dev, \
                    self.st_ino, \
                    self.st_mode, \
                    self.st_nlink, \
                    self.st_uid, \
                    self.st_gid, \
                    self.st_rdev, \
                    self.st_size, \
                    self.st_blksize, \
                    self.st_blocks, \
                    self.st_atime, \
                    self.st_mtime, \
                    self.st_ctime) = params
    def __str__(self):
        return "<NyaStat %s>" % self.__dict__


    #def set(self, **kwargs):
    #    for i in kwargs.keys():
