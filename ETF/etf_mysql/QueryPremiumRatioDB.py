#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *

# 查询etf可现金替代成分股及其溢价比例
def QueryPremiumRatioDB(etf_code1):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    sql_str = 'SELECT underlying_instrument_id, premium_ratio / 100000, component_share' \
          ' from xtp_etf_components_' + date + \
          ' where substitute_flag = 1' \
            ' and etf_code1 = ' + str(etf_code1)
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(sql_str)
        rs = cur.fetchall()
    return rs
