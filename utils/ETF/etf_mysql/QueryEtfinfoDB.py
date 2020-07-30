#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


# --- QueryStkprice(stkcode,market,security_type)
# ----入参1：stkcode str,当stkcode＝’999999‘时，会随机返回符合市场和证券类型要求证券代码
# ----入参2:market str,'1' 为上Ａ，‘２’为深Ａ
# ----入参3:security_type str,‘０‘为股票，'14'为单市场ETF，'15'为跨市场ETF
# --- 返回值：dict类型 stkparm['证券代码'],stkparm['昨收盘价'],stkparm['涨停价'],stkparm['跌停价'],stkparm['跌停价'],stkparm['随机中间价']

def QueryEtfinfoDB(stkcode,market,security_type,security_status, trade_status):
    code = {
        '证券代码': None
    }

    date = time.strftime('%Y%m%d', time.localtime(time.time()))

    if stkcode != '999999':
        str = 'select * from xtp_exch_sec_' + date + ' a join xtp_etf_baseinfo_' + date + ' b on a.instrument_id = b.ticker where a.exch_id = ' + market + ' and a.security_type = ' + security_type + ' and a.instrument_id = ' + stkcode
    else:
        str = 'select * from xtp_exch_sec_' + date + ' a join xtp_etf_baseinfo_' + date + ' b on a.instrument_id = b.ticker where a.exch_id = ' + market + ' and a.security_type = ' + security_type + ' and a.trade_status = '+trade_status

    try:
        conn=connectMysql()
        cur = conn.cursor()
        cur.execute(str)
        etfInfo = cur.fetchall()
        if etfInfo != ():
            i = random.randint(0, len(etfInfo) - 1)
            code['证券代码'] = etfInfo[i][1]
            cur.close()
            conn.close()
        else:
            return

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return code

# 查询必须现金替代时，申赎或赎回需要的总金额
def QueryCreationRedemptionCash(etf_code1):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT ' \
          '  case when sum(creation_cash_substitute) is null then 0' \
          '    else sum(creation_cash_substitute) end as sum_creation_cash,' \
          '  case when sum(redemption_cash_substitute) is null then 0'\
          '    else sum(redemption_cash_substitute) end as sum_redemption_cash' \
          ' from xtp_etf_components_' + date + \
          ' where etf_code1 = ' + etf_code1 + \
          ' and substitute_flag = 2'
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(str)
        rs = cur.fetchall()
        code_rs = {}
        if rs is not ():
            code_rs['creation_cash_substitute'] = rs[0][0]
            code_rs['redemption_cash_substitute'] = rs[0][1]
    return code_rs

# 查询etf一级市场申购赎回代码
def QueryEtfCode1(ticker):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT etf_code1' \
          ' from xtp_etf_baseinfo_' + date + \
          ' where etf_code0 = ' + ticker
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(str)
        rs = cur.fetchone()
        code_rs = ''
        if rs is not ():
            code_rs = rs[0]
    return code_rs


