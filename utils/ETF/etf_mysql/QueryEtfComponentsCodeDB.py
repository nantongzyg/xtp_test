#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtpapi import *

def QueryEtfComponentsInfoDB(ticker,market_id):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    if market_id == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
        market_id = '1'
    else:
        market_id = '2'
    str = 'SELECT underlying_instrument_id, substitute_flag,' \
              ' component_share, premium_ratio, preclose_px/10000,' \
              ' creation_cash_substitute, estimate_cash_component,' \
              ' redemption_cash_substitute' \
          ' from xtp_etf_components_' + date + ' a, xtp_etf_baseinfo_' + date + \
                ' b, xtp_exch_sec_' + date + ' c' \
          ' where a.etf_code1 = b.etf_code1' \
          ' and a.underlying_instrument_id = c.instrument_id' \
          ' and b.ticker = "' + ticker + '"' \
          ' and b.exch_id = "' + market_id + '"' \
          ' and c.security_type in (0, 1, 2)'
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchall()
    cur.close()
    conn.close()
    return rs

# 获取etf成分股代码
def QueryEtfComponentsCodeDB(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = ('SELECT'
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
        cur.execute(str)
        rs = cur.fetchall()
        code_rs = []
        if rs is not ():
            for code in rs:
                code_rs.append(code[0])
    return code_rs

QueryEtfComponentsCodeDB('139809')

# 查询证券状态（是否可交易）
def QueryStkSecurityStatusDB(stk_code):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = ('SELECT'
              ' security_status'
          ' from'
              ' xtp_exch_sec_' + date + ' e'
          ' where'
              ' e.instrument_id = ' + stk_code +
          ' and e.security_type in (0, 1, 2)')
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(str)
        rs = cur.fetchone()
    return rs[0]


# 获取etf'一级市场申购赎回代码'和'资金划转代码'
def QueryEtfCode1Code2DB(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT etf_code1, etf_code2' \
          ' from xtp_etf_baseinfo_' + date + \
          ' where etf_code0 = ' + ticker
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(str)
        rs = cur.fetchall()
        code_rs = {}
        if rs is not ():
            code_rs['etf_code1'] = rs[0][0]
            code_rs['etf_code2'] = rs[0][1]
    return code_rs




