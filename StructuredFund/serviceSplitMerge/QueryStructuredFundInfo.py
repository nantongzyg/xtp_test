#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/mysql")
from QueryStructuredFundDB import QueryStructuredFundDB
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *


# --- QueryStkprice(stkcode,market,security_type)
# ----入参1：stkcode str,当stkcode＝’999999‘时，会随机返回符合市场和证券类型要求证券代码
# ----入参2:market str,'1' 为上Ａ，‘２’为深Ａ
# ----入参3:security_type str,‘０‘为股票，'14'为单市场ETF，'15'为跨市场ETF
#-----入参４：BSflag：买卖标示 'B'买　'S'卖
# --- 返回值：dict类型 stkparm['证券代码'],stkparm['昨收盘价'],stkparm['涨停价'],stkparm['跌停价'],stkparm['跌停价'],stkparm['随机中间价'],
stkPriceQty = {
    '证券代码': '',
    '返回结果': False,
    '错误原因': '',
}

def QueryStructuredFundInfo(stkcode, market, security_type, security_status,
                            trade_status, divide_status, expect_status, Api):
    stkPriceQty=GetStructuredFundInfo(stkcode,
                                      market,
                                      security_type,
                                      security_status,
                                      trade_status,
                                      divide_status)
    logger.info('查询到的委托入参相关信息如下')
    dictLogging(stkPriceQty)
    return stkPriceQty

def GetStructuredFundInfo(stkcode, market, security_type,
                          security_status, trade_status, divide_status):
    global stkPriceQty
    rs = QueryStructuredFundDB(stkcode, market, security_type,
                               security_status, trade_status, divide_status)
    stkPriceQty['证券代码'] = rs['证券代码']
    stkPriceQty['返回结果'] = True
    return stkPriceQty

