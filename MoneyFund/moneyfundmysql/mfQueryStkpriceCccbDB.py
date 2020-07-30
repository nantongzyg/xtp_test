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

def QueryStkpriceCccbDB(stkcode,market,security_type,security_status, trade_status, cccb_flag, fundacc):

    stkprice = {
        '证券代码': None,
        '昨收盘价': None,
        '涨停价': None,
        '跌停价': None,
        '随机中间价': None
    }

    j=2

    date = time.strftime('%Y%m%d', time.localtime(time.time()))

    #持仓成本校验，T+1买入或卖出
    if cccb_flag == '1':
        if stkcode != '999999':
            str = 'select * from xtp_exch_sec_' + date + ' a join xtp_stk_asset_' + date + ' b on a.instrument_id = b.stock_code where a.exch_id = ' + market + ' and a.security_type =' + security_type + ' and b.stock_code=' + stkcode + ' and b.stk_avl_qty >= 100 and b.fund_acc = \'' + fundacc + '\''

        else:
            str = 'select * from xtp_exch_sec_' + date + ' a join xtp_stk_asset_' + date + ' b on a.instrument_id = b.stock_code where a.exch_id = ' + market + ' and a.security_type =' + security_type + ' and a.security_status='+security_status+' and a.trade_status='+trade_status + ' and b.stk_avl_qty >= 100 and b.fund_acc = \'' + fundacc + '\''
    #持仓成本校验，T+0买入或卖出
    else:
        if stkcode != '999999':
            str = 'select * from xtp_exch_sec_' + date + ' a where not exists (select 1 from xtp_stk_asset_' + date + ' b where a.instrument_id = b.stock_code and b.fund_acc = \'' + fundacc + '\') and a.exch_id = ' + market + ' and a.security_type =' + security_type + ' and a.instrument_id=' + stkcode

        else:
            str = 'select * from xtp_exch_sec_' + date + ' a where not exists (select 1 from xtp_stk_asset_' + date + ' b where a.instrument_id = b.stock_code and b.fund_acc = \'' + fundacc + '\') and a.exch_id = ' + market + ' and a.security_type =' + security_type + ' and a.security_status='+security_status+' and a.trade_status='+trade_status
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
