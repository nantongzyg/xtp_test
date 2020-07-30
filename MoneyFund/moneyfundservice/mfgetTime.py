#!/usr/bin/python
# -*- encoding: utf-8 -*-
import datetime
import time

#获取当前时间，返回值为Int,年月日时分秒
def getTimeInt():
    a = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    nowInt =int(a)
    return nowInt

#获取当前（时间）秒，返回值为Int,秒
def getTimeSecondInt():
    a = datetime.datetime.strftime(datetime.datetime.now(), '%S')
    nowInt = int(a)
    return nowInt

#获取当前时间戳(秒), 返回值为Int
def getTimestampInt():
    sec = int(time.time())
    return sec
