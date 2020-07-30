#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
from mysql_config import *
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import *


date = time.strftime('%Y%m%d', time.localtime(time.time()))
def QueryEptDayOrder():

    str='select * from xtp_ept_dayorderrec_'+ date
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchall()
    cur.close()
    conn.close()
    return rs

if __name__ == "__main__":


    QueryEptDayOrder()
