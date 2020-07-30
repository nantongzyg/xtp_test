#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append('/home/yhl2/workspace/xtp_test')
from mysql.mysql_config import connectMysql


def query_cetf_basketcount(ticker):
    """查询跨市场etf成分股数量"""
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    sql = 'SELECT count(*) from xtp_etf_components_' + date + \
          ' a join xtp_etf_baseinfo_'+ date + \
          ' b on a.etf_code1 = b.etf_code1 where b.ticker=' + ticker + ''
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs[0]


if __name__ == '__main__':
    print query_cetf_basketcount('510300')





