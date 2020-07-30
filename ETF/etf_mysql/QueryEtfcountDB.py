#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


def QueryEtfcountDB(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = ('SELECT sum(component_share) from xtp_etf_components_' + date +
          ' a join xtp_etf_baseinfo_'+ date +
           ' b on a.etf_code1 = b.etf_code1 where b.ticker=' + ticker +
            ' and a.substitute_flag in (0,1);')
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return float(rs[0]) if rs[0] else 0
