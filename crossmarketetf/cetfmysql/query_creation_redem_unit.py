#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append('/home/yhl2/workspace/xtp_test')
from mysql.mysql_config import connectMysql


def query_creation_redem_unit(ticker):
    """查询etf最小申赎单位"""
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    sql = 'SELECT creation_redemption_unit from xtp_etf_baseinfo_'+ date \
          +' t1 where t1.ticker=' + ticker + ''
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs[0]


if __name__ == '__main__':
    print query_creation_redem_unit('510300')



