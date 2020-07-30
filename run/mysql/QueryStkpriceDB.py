#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
from mysql_config import *


date = time.strftime('%Y%m%d', time.localtime(time.time()))

# --- QueryStkprice(stkcode,market,security_type)
# ----入参1：stkcode str,当stkcode＝’999999‘时，会随机返回符合市场和证券类型要求证券代码
# ----入参2:market str,'1' 为上Ａ，‘２’为深Ａ
# ----入参3:security_type str,‘０‘为股票，'14'为单市场ETF，'15'为跨市场ETF
# --- 返回值：dict类型 stkparm['证券代码'],stkparm['昨收盘价'],stkparm['涨停价'],stkparm['跌停价'],stkparm['跌停价'],stkparm['随机中间价']

def QueryStkpriceDB(stkcode,market,security_type,security_status, trade_status):
    stkprice = {
        '证券代码': None,
        '昨收盘价': None,
        '涨停价': None,
        '跌停价': None,
        '随机中间价': None
    }
    # 保留精度
    j=2

    # 100表示查询股票和etf
    if security_type == '100':
        if stkcode != '999999':
            str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type in (\'0\',\'1\',\'2\',\'14\',\'15\') and instrument_id=' + stkcode
        else:
            str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type in (\'0\',\'1\',\'2\',\'14\',\'15\') and trade_status='+trade_status
    # 14-单市场etf， 15-跨市场etf
    elif security_type in ('14', '15'):
        if stkcode != '999999':
            str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type =' + security_type + ' and instrument_id=' + stkcode
        else:
            str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type =' + security_type + \
                  ' and security_status=' + security_status + ' and trade_status=' + trade_status + ' and (instrument_id like "159%" or instrument_id like "510%")'
    #
    else:
        if stkcode != '999999':
            str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type =' + security_type + ' and instrument_id=' + stkcode
        else:
            str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type =' + security_type + ' and security_status='+security_status+' and trade_status='+trade_status

    try:
        conn=connectMysql()
        cur = conn.cursor()
        cur.execute(str)
        queryPrice = cur.fetchall()
        i=random.randint(0,len(queryPrice)-1)
        stkprice['证券代码'] = queryPrice[i][1]
        security_type_res = queryPrice[i][6]

        # 股票
        if security_type_res in(0, 1, 2):
            j=2
        # 14-单市场etf，15-跨市场etf，24-分级子基金
        elif security_type_res in(14, 15, 24):
            j=3

        #--昨收盘价---
        stkprice['昨收盘价']=round(float(queryPrice[i][5]) / 10000, j)

        # --涨停价---
        stkprice['涨停价'] = round(float(queryPrice[i][3]) / 10000, j)

        # --跌停价---
        stkprice['跌停价'] = round(float(queryPrice[i][4]) / 10000, j)

        #---随机中间价--
        sj= random.randint(queryPrice[i][4], queryPrice[i][3])
        stkprice['随机中间价'] = round(float(sj) / 10000, j)

        cur.close()
        conn.close()

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return stkprice

def QueryStkSz():
    sql = '''
        select instrument_id, limitup_px from xtp_exch_sec_%s where exch_id = 2 
and security_type = 0
and security_status = 2 
and trade_status = 0
    ''' % (date)
    conn=connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    queryPrice = cur.fetchall()
    return queryPrice

def QueryStkSh():
    sql = '''
        select instrument_id, limitup_px from xtp_exch_sec_%s where exch_id = 1 
and security_type = 0
and security_status = 2 
and trade_status = 0
    ''' % (date)
    conn=connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    queryPrice = cur.fetchall()
    return queryPrice

