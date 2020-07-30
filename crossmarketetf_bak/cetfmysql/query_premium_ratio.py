#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from mysql.mysql_config import *

def query_premium_ratio(etf_code1):
    """
    查询etf可现金替代成分股及其溢价比例
    :param etf_code1: etf一级市场代码
    :return:((code1,decimal(0.100),成分股数),(code2,decimal(0.100),成分股数)...)
    """
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    sql = ('SELECT underlying_instrument_id, premium_ratio / 100000, ' +
              'component_share from xtp_etf_components_' + date +
              ' where substitute_flag = 1' +
              ' and etf_code1 = ' + str(etf_code1))
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
    return rs

if __name__ == '__main__':
    print query_premium_ratio('510301')