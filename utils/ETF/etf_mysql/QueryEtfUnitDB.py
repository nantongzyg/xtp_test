#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


def QueryEtfUnitDB(stockcode,market,security_type,security_status, trade_status,fundid):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    # str = 'SELECT a.stock_code from xtp_stk_asset_'+date+' a,xtp_exch_sec_'+date+' b WHERE a.stock_code=b.instrument_id AND b.exch_id=' + market + ' AND b.security_type=' + security_type + ' AND a.fund_acc=\'' + fundid + '\''
    str = 'SELECT c.creation_redemption_unit' \
              ' from xtp_exch_sec_' + date + ' b, ' \
              ' xtp_etf_baseinfo_' + date + ' c' \
           ' WHERE b.instrument_id = c.ticker' \
                ' AND b.exch_id = ' + market + \
                ' AND b.security_type = ' + security_type + \
                ' AND b.security_status = ' + security_status + \
                ' AND b.instrument_id = ' + stockcode + \
                ' AND b.trade_status = ' + trade_status
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchall()
    cur.close()
    conn.close()
    return rs



