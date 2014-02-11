#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab:
#
# Copyright (C) 2009
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
# $Id: nyaerror.py 68 2009-06-02 14:14:16Z Maxim.Kovalev $

"""
Это модуль для исключений.
Пока все просто и уныло.
"""
class	NyaError(Exception):
    """
    Использование:
    MySuperError(NyaError)
        pass

    try:
        raise NyaError("Shit!")
    except NyaError, e:
        print "Args = %s, message = %s" % (e.args, e.message)
        # Напечатает:
        # Args = ('Shit!',), message = Shit!" % (e.args, e.message)
        #

    try:
        if myBad:
            raise MySuperError("My")
        if nyaBad:
            raise NyaError("Nyaaa!")
    except MySuperError, e:
        # e.message = My
    except NyaError, e:
        # e.message = Nyaaa!

    Ну и так далее...

    Как то так, если не работает -- по лицу не бить!
    """
    # Есть подозрение, что задание eclass и efunc -- костыль
    # M.K.  Думаю, не лишим будет и пустое дефолтное знаечение сообщения.
    #       И что можно передвать в качестве args и kwargs?
    # V.B.  Лучше имхо не пустое, а "Урод, напиши тут нормальное описание исключеия!!"
    #       args и kwargs -- хз, на всякий случай оставил. В Exception если сунуть один аргумент,
    #       то он сохраняеться в message. И целиком все сохраняеться в self.args
    #       Я вот думаю, может еще добавть ченть типа уровней ошибки,
    #       например ERR, WARN, ARMAGEDDON, SEVERNAYA_BELAYA_LISA
    def __init__(self, msg="", eclass=None, efunc=None, **kwargs):
        Exception.__init__(self, msg)
        s = lambda x: (type(x) == str) and x or str(x)
        self.eclass = s(eclass)
        self.efunc = s(efunc)
        self.kwargs=kwargs

        if efunc != None:
            msg = self.efunc + ": " + msg
        if eclass != None:
            msg = self.eclass + ": " + msg
        self.message = msg

#class NoItem (NyaError):
#    def __init__(self, msg = "", eclass, efunc):
#        NyaError.__init__(self, msg, eclass, efunc)
        
#class ExistItem (NyaError):
#    def __init__(self, msg = "", eclass, efunc):
#       NyaError.__init__(self, msg, eclass, efunc)
#        
#class DBError (NyaError):
#    def __init__(self, msg = "", eclass, efunc):
#        NyaError.__init__(self, msg, eclass, efunc)