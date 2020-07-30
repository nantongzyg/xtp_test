#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


def QueryEtfassetDB(stockcode,market,security_type,security_status, trade_status,fundid):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    # str = 'SELECT a.stock_code from xtp_stk_asset_'+date+' a,xtp_exch_sec_'+date+' b WHERE a.stock_code=b.instrument_id AND b.exch_id=' + market + ' AND b.security_type=' + security_type + ' AND a.fund_acc=\'' + fundid + '\''
    if stockcode == '999999':
        str = 'SELECT a.stock_code,c.creation_redemption_unit from xtp_stk_asset_' + date + ' a,xtp_exch_sec_' + date + ' b,xtp_etf_baseinfo_' + date + ' c WHERE a.stock_code=b.instrument_id AND a.stock_code=c.ticker AND b.exch_id=' + market + ' AND b.security_type=' +security_type+ ' and b.security_status='+security_status+' and b.trade_status='+trade_status+' AND a.fund_acc=\'' + fundid + '\''
    else:
        str = 'SELECT a.stock_code,c.creation_redemption_unit from xtp_stk_asset_' + date + ' a,xtp_exch_sec_' + date + ' b,xtp_etf_baseinfo_' + date + ' c WHERE a.stock_code=b.instrument_id AND a.stock_code=c.ticker AND b.exch_id=' + market + ' AND b.security_type=' + security_type + ' and b.security_status=' + security_status + ' and a.stock_code = ' + stockcode + ' and b.trade_status=' + trade_status + ' AND a.fund_acc=\'' + fundid + '\''
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchall()
    cur.close()
    conn.close()
    return rs



