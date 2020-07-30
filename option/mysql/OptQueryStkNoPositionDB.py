#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
from opt_mysql_config import *


# --- QueryStkprice(stkcode,market,security_type)
# ----入参1：stkcode str,当stkcode＝’999999‘时，会随机返回符合市场和证券类型要求证券代码
# ----入参2:market str,'1' 为上Ａ，‘２’为深Ａ
# ----入参3:security_type str,‘０‘为股票，'14'为单市场ETF，'15'为跨市场ETF
# --- 返回值：dict类型 stkparm['证券代码'],stkparm['昨收盘价'],stkparm['涨停价'],stkparm['跌停价'],stkparm['跌停价'],stkparm['随机中间价']

def QueryStkNoPositionDB(stkcode,market,security_type,security_status, trade_status,fundacc):

    date = time.strftime('%Y%m%d', time.localtime(time.time()))

    if stkcode != '999999':
        str = 'select t1.instrument_id from xtp_exch_sec_' + date + ' t1 where NOT EXISTS (SELECT 1 FROM xtp_stk_asset_' + date + ' t2 WHERE t1.instrument_id = t2.stock_code and t2.fund_acc=' + fundacc + ') and t1.exch_id = ' + market + ' and t1.security_type =' + security_type + ' and t1.instrument_id=' + stkcode
    else:
        str = 'select t1.instrument_id from xtp_exch_sec_' + date + ' t1 where NOT EXISTS (SELECT 1 FROM xtp_stk_asset_' + date + ' t2 WHERE t1.instrument_id = t2.stock_code and t2.fund_acc=' + fundacc + ') and t1.exch_id = ' + market + ' and t1.security_type =' + security_type + ' and t1.security_status='+security_status+' and t1.trade_status='+trade_status
    rs1 = []
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchall()
    for i in rs:
        rs1.append(i[0])
    cur.close()
    conn.close()
    return rs1
