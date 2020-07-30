#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *

# 查询预估现金差额
def QueryEstimateCashComponent(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT estimate_cash_component / 10000.0' \
          ' from xtp_etf_baseinfo_' + date + \
          ' where etf_code0 = ' + ticker
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(str)
        rs = cur.fetchone()
        estimate_cash_component = float(rs[0]) if rs is not () else 0
    return estimate_cash_component
