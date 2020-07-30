#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from mysql.mysql_config import connectMysql

date = time.strftime('%Y%m%d', time.localtime(time.time()))

def query_market_by_stkcode(ticker):
    """查询etf成分股的市场，参数tiker:成分股代码"""
    sql = 'SELECT exch_id' \
          ' from xtp_exch_sec_' + date + \
          ' where security_type in (0, 1, 2)' \
            ' and security_status = 2' \
            ' and instrument_id = ' + str(ticker)
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchone()
    return rs[0]


if __name__ == '__main__':
    print query_market_by_stkcode('600000')
