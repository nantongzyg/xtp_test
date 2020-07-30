#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


def QueryBasketCountDB(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT count(*) from xtp_etf_components_' + date + ' a join xtp_etf_baseinfo_'+ date +' b on a.etf_code1 = b.etf_code1 where b.ticker=' + ticker + ''
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs[0]



