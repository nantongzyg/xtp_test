#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


def QueryEtfComponentsDB(ticker,underlying_instrument_id):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT a.component_share ' \
              'from xtp_etf_components_' + date + \
                  ' a, xtp_etf_baseinfo_' + date + \
          ' b where a.etf_code1 = b.etf_code1 ' \
            ' and b.ticker = "' + ticker + \
            '" and a.underlying_instrument_id = "' + underlying_instrument_id + '"'
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs[0]

def QueryEtfSubstitute(ticker,underlying_instrument_id):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT a.component_share, a.substitute_flag ' \
              'from xtp_etf_components_' + date + \
                  ' a, xtp_etf_baseinfo_' + date + \
          ' b where a.etf_code1 = b.etf_code1 ' \
            ' and b.ticker = "' + ticker + \
            '" and a.underlying_instrument_id = "' + underlying_instrument_id + '"'
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs

def QueryEtfComponentShare(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT ' \
                ' a.underlying_instrument_id, ' \
                ' a.component_share ' \
              'from xtp_etf_components_' + date + \
                  ' a, xtp_etf_baseinfo_' + date + \
          ' b where a.etf_code1 = b.etf_code1 ' \
            ' and b.ticker = ' + ticker
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchall()
    component_shares = {}
    for share in rs:
        component_shares[share[0]] = share[1]
    cur.close()
    conn.close()
    return component_shares
