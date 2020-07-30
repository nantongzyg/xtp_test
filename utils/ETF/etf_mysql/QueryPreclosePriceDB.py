#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *

# ------------------------------------------------------------------------------------------------------------------
# 定义函数：根据证券代码获取涨停价
# ------------------------------------------------------------------------------------------------------------------
def QueryPreclosePriceDB(stkcode):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT a.preclose_px/10000 from xtp_exch_sec_' + date + ' a WHERE a.instrument_id =' + stkcode + ' AND a.security_type != 255 and a.trade_status!=255'
    try:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(str)
        rs = cur.fetchone()
        preclose_price = rs[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return preclose_price

def QueryCompnentsPreclosePriceDB(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = ('SELECT'
                ' c.instrument_id,'
                ' c.preclose_px/10000'
           ' FROM'
               ' xtp_etf_baseinfo_' + date + ' a'
           ' JOIN xtp_etf_components_' + date + ' b on'
               ' a.etf_code1 = b.etf_code1'
           ' JOIN xtp_exch_sec_' + date + ' c on'
               ' b.underlying_instrument_id = c.instrument_id'
           ' WHERE a.ticker = ' + ticker +
           ' AND b.exch_id = c.exch_id'
           ' AND c.security_type != 255 and c.trade_status!=255')
    try:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(str)
        components_precloseprice = cur.fetchall()
        components_precloseprices = {}
        for rs in components_precloseprice:
            components_precloseprices[rs[0]] = float(rs[1])
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return components_precloseprices

def QueryPreclosePriceDB(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = ('SELECT'
                ' a.preclose_px/10000'
           ' FROM'
               ' xtp_exch_sec_' + date + ' a'
           ' WHERE a.instrument_id = ' + ticker)
    precloseprice = 0
    try:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(str)
        rs = cur.fetchone()
        precloseprice = rs[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return precloseprice