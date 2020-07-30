#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
from mysql_config import *


# --- QueryStkprice(stkcode,market,security_type)
# ----入参1：stkcode str,当stkcode＝’999999‘时，会随机返回符合市场和证券类型要求证券代码
# ----入参2:market str,'1' 为上Ａ，‘２’为深Ａ
# ----入参3:security_type str,‘０‘为股票，'14'为单市场ETF，'15'为跨市场ETF
# --- 返回值：dict类型 stkparm['证券代码'],stkparm['昨收盘价'],stkparm['涨停价'],stkparm['跌停价'],stkparm['跌停价'],stkparm['随机中间价']

def QueryStkpriceDecimalDB(stkcode,market,security_type,security_status, trade_status, decimal_type):

    stkprice = {
        '证券代码': None,
        '昨收盘价': None,
        '涨停价': None,
        '跌停价': None,
        '随机中间价': None
    }

    j=2

    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    if security_type == '100':
        if stkcode != '999999':
            if decimal_type == '1':
                str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type in (\'0\',\'1\',\'2\',\'14\',\'15\') and instrument_id=' + stkcode + ' and substr(substring_index(limitup_px/10000,\'.\',-1),3,1) >= 5'
            else:
                str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type in (\'0\',\'1\',\'2\',\'14\',\'15\') and instrument_id=' + stkcode + ' and substr(substring_index(limitdown_px/10000,\'.\',-1),3,1) >= 5'
        else:
            if decimal_type == '1':
                str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type in (\'0\',\'1\',\'2\',\'14\',\'15\') and trade_status='+trade_status + ' and substr(substring_index(limitup_px/10000,\'.\',-1),3,1) >= 5'
            else:
                str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type in (\'0\',\'1\',\'2\',\'14\',\'15\') and trade_status='+trade_status + ' and substr(substring_index(limitdown_px/10000,\'.\',-1),3,1) >= 5'
    else:
        if stkcode != '999999':
            if decimal_type == '1':
                str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type =' + security_type + ' and instrument_id=' + stkcode + ' and substr(substring_index(limitup_px/10000,\'.\',-1),3,1) >= 5'
            else:
                str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type =' + security_type + ' and instrument_id=' + stkcode + ' substr(substring_index(limitdown_px/10000,\'.\',-1),3,1) >= 5'
        else:
            if decimal_type == '1':
                str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type =' + security_type + ' and security_status='+security_status+' and trade_status='+trade_status + ' and substr(substring_index(limitup_px/10000,\'.\',-1),3,1) >= 5'
            else:
                str = 'select * from xtp_exch_sec_' + date + ' where exch_id = ' + market + ' and security_type =' + security_type + ' and security_status='+security_status+' and trade_status='+trade_status + ' and substr(substring_index(limitdown_px/10000,\'.\',-1),3,1) >= 5'
    if security_type in('0','1','2'):
        j=2
    elif security_type in('14','15'):
        j=3

    try:
        conn=connectMysql()
        cur = conn.cursor()
        cur.execute(str)
        queryPrice = cur.fetchall()
        i=random.randint(0,len(queryPrice)-1)
        stkprice['证券代码'] = queryPrice[i][1]
        security_type_res = queryPrice[i][6]

        if security_type_res in(0,1,2):
            j=2
        elif security_type_res in(14,15):
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
