#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *

#查询etf最小申赎单位
def QueryCreationRedemUnitDB(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT creation_redemption_unit from xtp_etf_baseinfo_'+ date +' t1 where t1.ticker=' + ticker + ''
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs[0]



