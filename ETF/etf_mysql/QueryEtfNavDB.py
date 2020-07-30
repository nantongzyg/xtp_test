#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


def QueryEtfNavDB(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT nav from xtp_etf_baseinfo_'+ date +' b where b.ticker=' + ticker + ''
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs[0]



