#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *

# 查询etf可现金替代成分股及其溢价比例
def QueryMarketByStkcode(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    sql_str = 'SELECT exch_id' \
          ' from xtp_exch_sec_' + date + \
          ' where security_type in (0, 1, 2)' \
            ' and security_status = 2' \
            ' and instrument_id = ' + str(ticker)
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(sql_str)
        rs = cur.fetchone()
    return rs[0]

