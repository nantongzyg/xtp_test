#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from mysql.mysql_config import *

date = time.strftime('%Y%m%d', time.localtime(time.time()))
print date

sys.path.append('/home/yhl2/workspace/xtp_test/utils')
def query_cetf_nav(ticker):
    """
    查询Etf单位净值
    :param ticker: etf二级市场代码
    :return:
    """
    sql = ('SELECT nav from xtp_etf_baseinfo_'+ date +' b where b.ticker='
           + ticker + '')
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs[0]



if __name__ == '__main__':
    print query_cetf_nav('510300')
