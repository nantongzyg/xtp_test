#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from mysql.mysql_config import connectMysql

date = time.strftime('%Y%m%d', time.localtime(time.time()))

def query_cetf_components(ticker,underlying_instrument_id):
    """查询etf单支成分股数量
    参数ticker：二级市场代码
    underlying_instrument_id：成分股代码"""
    sql = 'SELECT a.component_share ' \
              'from xtp_etf_components_' + date + \
                  ' a, xtp_etf_baseinfo_' + date + \
          ' b where a.etf_code1 = b.etf_code1 ' \
            ' and b.ticker = "' + ticker + \
            '" and a.underlying_instrument_id = "' \
          + underlying_instrument_id + '"'
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs[0]

def query_cetf_substitute(ticker,underlying_instrument_id):
    """查询etf单支成分股数量及现金替代标志
    参数ticker：etf二级市场代码
    参数underlying_instrument_id：成分股代码
    """
    sql = 'SELECT a.component_share, a.substitute_flag ' \
              'from xtp_etf_components_' + date + \
                  ' a, xtp_etf_baseinfo_' + date + \
          ' b where a.etf_code1 = b.etf_code1 ' \
            ' and b.ticker = "' + ticker + \
            '" and a.underlying_instrument_id = "' \
          + underlying_instrument_id + '"'
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs

def query_cetf_component_share(ticker):
    """查询etf的成分股代码及成分股对应数量(etf最小申购赎回时对应的该成分股数量)
    参数ticker：ETF二级市场代码  返回字典：key=成分股，value=成分股数量
    """
    sql = 'SELECT ' \
                ' a.underlying_instrument_id, ' \
                ' a.component_share ' \
              'from xtp_etf_components_' + date + \
                  ' a, xtp_etf_baseinfo_' + date + \
          ' b where a.etf_code1 = b.etf_code1 ' \
            ' and b.ticker = ' + ticker
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchall()
    component_shares = dict(rs)
    cur.close()
    conn.close()
    return component_shares

if __name__ == '__main__':
    print query_cetf_component_share('550580')
    # print query_cetf_substitute('510300','300136')
    # print query_cetf_components('510300','300136')