#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


def QueryStkassetDecimalDB(market,security_type,security_status, trade_status,fundid, decimal_type):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    # str = 'SELECT a.stock_code from xtp_stk_asset_'+date+' a,xtp_exch_sec_'+date+' b WHERE a.stock_code=b.instrument_id AND b.exch_id=' + market + ' AND b.security_type=' + security_type + ' AND a.fund_acc=\'' + fundid + '\''
    if security_type == '100':
        if decimal_type == '1':
            str = 'SELECT a.stock_code from xtp_stk_asset_' + date + ' a,xtp_exch_sec_' + date + ' b WHERE a.stock_code=b.instrument_id AND b.exch_id=' + market + ' AND b.security_type in (\'0\',\'1\',\'2\',\'14\',\'15\') and b.security_status='+security_status+' and b.trade_status='+trade_status+' AND a.fund_acc=\'' + fundid + '\'' + ' and substr(substring_index(limitup_px/10000,\'.\',-1),3,1) >= 5'
        else:
            str = 'SELECT a.stock_code from xtp_stk_asset_' + date + ' a,xtp_exch_sec_' + date + ' b WHERE a.stock_code=b.instrument_id AND b.exch_id=' + market + ' AND b.security_type in (\'0\',\'1\',\'2\',\'14\',\'15\') and b.security_status='+security_status+' and b.trade_status='+trade_status+' AND a.fund_acc=\'' + fundid + '\'' + ' and substr(substring_index(limitdown_px/10000,\'.\',-1),3,1) >= 5'
    else:
        if decimal_type == '1':
            str = 'SELECT a.stock_code from xtp_stk_asset_' + date + ' a,xtp_exch_sec_' + date + ' b WHERE a.stock_code=b.instrument_id AND b.exch_id=' + market + ' AND b.security_type=' + security_type + ' and b.security_status='+security_status+' and b.trade_status='+trade_status+' AND a.fund_acc=\'' + fundid + '\'' + ' and substr(substring_index(limitup_px/10000,\'.\',-1),3,1) >= 5'
        else:
            str = 'SELECT a.stock_code from xtp_stk_asset_' + date + ' a,xtp_exch_sec_' + date + ' b WHERE a.stock_code=b.instrument_id AND b.exch_id=' + market + ' AND b.security_type=' + security_type + ' and b.security_status='+security_status+' and b.trade_status='+trade_status+' AND a.fund_acc=\'' + fundid + '\'' + ' and substr(substring_index(limitdown_px/10000,\'.\',-1),3,1) >= 5'
    rs1=[]
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchall()
    for i in rs:
        rs1.append(i[0])
    cur.close()
    conn.close()
    return rs1



