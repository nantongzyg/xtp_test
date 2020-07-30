#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import random
import traceback
import ServiceConfig
import sys
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *
from QueryFundidDB import *
from QueryStkpriceDB import *
from QueryStkNoPositionDB import *


# --- QueryStkprice(stkcode,market,security_type)
# ----入参1：stkcode str,当stkcode＝’999999‘时，会随机返回符合市场和证券类型要求证券代码
# ----入参2:market str,'1' 为上Ａ，‘２’为深Ａ
# ----入参3:security_type str,‘０‘为股票，'14'为单市场ETF，'15'为跨市场ETF
#-----入参４：BSflag：买卖标示 'B'买　'S'卖
# --- 返回值：dict类型 stkparm['证券代码'],stkparm['昨收盘价'],stkparm['涨停价'],stkparm['跌停价'],stkparm['跌停价'],stkparm['随机中间价'],

def QueryStkNoPosition(stkcode,market,security_type,security_status, trade_status):

    stkPriceQty = {
        '证券代码': '',
        '昨收盘价': None,
        '涨停价': None,
        '跌停价': None,
        '随机中间价': None,
        '返回结果':False,
        '错误原因':'',
    }

    try:
        # 查询fundid
        fundacc = QueryFundidDB()
        # 查询符合入参要求的初始持仓证券代码List
        stkcode_list = QueryStkNoPositionDB(stkcode,market, security_type,security_status, trade_status,fundacc)
        #随机取一个代码
        idx = random.randint(0, len(stkcode_list)-1)
        stkPriceQty['证券代码'] = stkcode_list[idx]
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        traceback.print_exc()
        stkPriceQty['返回结果'] = False
        stkPriceQty['错误原因'] = '数据库异常'
    except Exception as e:
        stkPriceQty['返回结果'] = False
        stkPriceQty['错误原因'] = '不存在符合要求的持仓证券'


    # 查询价格
    if stkPriceQty['证券代码'] != '':
        stkprice = QueryStkpriceDB(stkPriceQty['证券代码'], market, security_type, security_status, trade_status)
        stkPriceQty['昨收盘价'] = stkprice['昨收盘价']
        stkPriceQty['涨停价'] = stkprice['涨停价']
        stkPriceQty['跌停价'] = stkprice['跌停价']
        stkPriceQty['随机中间价'] = stkprice['随机中间价']
        stkPriceQty['返回结果'] = True
    else:
        logger.error('不存在符合要求的持仓证券')
        stkPriceQty['返回结果'] = False
        stkPriceQty['错误原因'] = '不存在符合要求的持仓证券'

    logger.info('查询到的委托入参相关信息如下')
    dictLogging(stkPriceQty)
    return stkPriceQty

#根据证券代码查询持仓----stkcode
def QuerySellable_qty(stkcode,Api):
    stkqty={
        '证券代码':stkcode,
        '可用数量':0,
    }
    ticker = {
        'ticker': ''
    }
    stkasset0 = Api.trade.QueryPositionSync(ticker)
    if stkasset0['data'].has_key(stkcode):
        stkqty['可用数量'] = stkasset0['data'][stkcode]['position']['sellable_qty']
    else:
        stkqty['可用数量'] = 0

    return  stkqty

