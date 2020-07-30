#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from mysql.mysql_config import connectMysql

date = time.strftime('%Y%m%d', time.localtime(time.time()))

def query_cetf_components_info(ticker,market_id):
    """
    根据二级市场代码获取所有成分股的信息
    :param ticker: etf二级市场代码
    :param market_id: etf市场，1是上海，2是深圳
    :return:
    """
    market_id = str(market_id)
    sql = ('SELECT underlying_instrument_id, substitute_flag,' +
              ' component_share, premium_ratio, preclose_px/10000,' +
              ' creation_cash_substitute, estimate_cash_component,' +
              ' redemption_cash_substitute, underlying_instrument_source' +
          ' from xtp_etf_components_' + date + ' a, xtp_etf_baseinfo_' + date +
                ' b, xtp_exch_sec_' + date + ' c' +
          ' where a.etf_code1 = b.etf_code1' +
          ' and a.underlying_instrument_id = c.instrument_id' +
          ' and b.ticker = "' + ticker + '"' +
          ' and b.exch_id = "' + market_id + '"' +
          ' and c.security_type in (0, 1, 2)')
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchall()
    cur.close()
    conn.close()
    return rs

def query_cetf_components_code(ticker):
    """根据一级市场代码查询出ETF所有成分股代码
    ticker：etf一级市场代码"""
    sql = ('SELECT'
              ' underlying_instrument_id'
          ' from'
              ' xtp_etf_components_' + date + ' c'
          ' join'
              ' xtp_exch_sec_' + date + ' e'
          ' on c.underlying_instrument_id = e.instrument_id'
          ' where'
              ' c.etf_code1 = ' + ticker +
          ' and e.security_type in (0, 1, 2)'
          ' and e.security_status = 2')
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        code_rs = []
        if rs is not ():
            for code in rs:
                code_rs.append(code[0])
    return code_rs



def query_cetf_code1code2(ticker):
    """获取etf '一级市场申购赎回代码' 和 '资金划转代码'"""
    sql = 'SELECT etf_code1, etf_code2' \
          ' from xtp_etf_baseinfo_' + date + \
          ' where etf_code0 = ' + ticker
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        code_rs = {}
        if rs is not ():
            code_rs['etf_code1'] = rs[0][0]
            code_rs['etf_code2'] = rs[0][1]
    return code_rs

if __name__ == '__main__':
    # print query_cetf_components_code('510301')
    # print query_cetf_code1code2('530720')
    print query_cetf_components_info('512700',1)


