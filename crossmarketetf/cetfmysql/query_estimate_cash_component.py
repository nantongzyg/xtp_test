#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append('/home/yhl2/workspace/xtp_test')
from mysql.mysql_config import connectMysql


def query_estimate_cash_component(ticker):
    """查询预估现金差额"""
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    sql = 'SELECT estimate_cash_component / 10000.0' \
          ' from xtp_etf_baseinfo_' + date + \
          ' where etf_code0 = ' + ticker
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchone()
        estimate_cash_component = float(rs[0]) if rs else 0
    return estimate_cash_component

if __name__ == '__main__':
    print query_estimate_cash_component('510300')
