#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import random
import traceback
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/service")
import ServiceConfig
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql")
from mfQueryFundidDB import *
from mfQueryStkassetDB import *
from mfQueryStkpriceDB import *
from mfQueryAllotmentStkInfoDB import *

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
    '昨收盘价': None,
    '涨停价': None,
    '跌停价': None,
    '随机中间价': None,
    '卖－随机数量': 0,
    '卖－可用数量': 0,
    '返回结果': False,
    '错误原因': '',
}


def QueryStkPriceQty(stkcode,market,security_type,security_status, trade_status,BSflag,expect_status,Api):
    global stkPriceQty
    #初始化'卖－可用数量'
    stkPriceQty['卖－可用数量'] = 0
    #最大委托数量
    max_qty = ServiceConfig.MAX_QTY
    #根据期望状态来决定最小委托数量
    if expect_status in('部成','部撤已报','部撤'):
        min_qty=ServiceConfig.PART_MIN_QTY
    else:
        min_qty=ServiceConfig.ORTHER_MIN_QTY

    if BSflag == 'B':
        stkPriceQty=GetStkPriceQty(stkcode,market,security_type,security_status, trade_status)

    elif BSflag == 'S':
        # 查询fundid
        fundacc = QueryFundidDB()
        #security_type 12:逆回购,1000:配股，逆回购不需要持仓
        if security_type == '12':
            stkPriceQty=GetStkPriceQty(stkcode,market,security_type,security_status, trade_status)
            logger.info('查询到的委托入参相关信息如下')
            dictLogging(stkPriceQty)
            return stkPriceQty
        #普通买卖业务
        elif stkcode =='999999' and security_type not in ('12','1000') :
            try:
                # 查询符合入参要求的初始持仓证券代码List
                stkcode_list = QueryStkassetDB(market, security_type,security_status, trade_status,fundacc)
                # 查询符合要求的持仓
                i = 0
                while stkPriceQty['卖－可用数量'] < min_qty and i < len(stkcode_list):
                    stkqty = QuerySellable_qty(stkcode_list[i], Api)
                    stkPriceQty['证券代码'] = stkqty['证券代码']
                    stkPriceQty['卖－可用数量'] = stkqty['可用数量']
                    i += 1

            except MySQLdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                traceback.print_exc()
                stkPriceQty['返回结果'] = False
                stkPriceQty['错误原因'] = '数据库异常'
        elif stkcode =='999999' and security_type == '1000':
            tickers = QueryAllotmentStkInfoDB(fundacc, market)
            for stkcode in tickers:
                stkqty = QuerySellable_qty(stkcode[0], Api)
                stkPriceQty['证券代码'] = stkqty['证券代码']
                stkPriceQty['卖－可用数量'] = stkqty['可用数量']
                if stkPriceQty['卖－可用数量']>0:
                    stkPriceQty['返回结果'] = True
                    stkPriceQty['错误原因'] = ''
                    break
                else:
                    stkPriceQty['返回结果'] = False
                    stkPriceQty['错误原因'] = '没有持仓'

        else:
            stkqty = QuerySellable_qty(stkcode,Api)
            stkPriceQty['证券代码'] = stkqty['证券代码']
            stkPriceQty['卖－可用数量'] = stkqty['可用数量']

        #1000表示配股
        if security_type != '1000':
            # 生成随机数量
            if stkPriceQty['卖－可用数量'] == 0:
                stkPriceQty['返回结果'] = False
                stkPriceQty['错误原因'] = '没有持仓'
            elif stkPriceQty['卖－可用数量'] > max_qty:
                stkPriceQty['卖－随机数量'] = int(round(random.randint(min_qty, max_qty), -2))
                stkPriceQty['返回结果'] = True
            elif stkPriceQty['卖－可用数量'] >= 200 and stkPriceQty['卖－可用数量'] <= max_qty:
                stkPriceQty['卖－随机数量'] = int(round(random.randint(min_qty, stkPriceQty['卖－可用数量']), -2))
                stkPriceQty['返回结果'] = True
            elif stkPriceQty['卖－可用数量'] < 200:
                stkPriceQty['卖－随机数量'] = stkPriceQty['卖－可用数量']
                stkPriceQty['返回结果'] = True
            # 查询价格
            if stkPriceQty['证券代码'] !='':
                stkprice = QueryStkpriceDB(stkPriceQty['证券代码'], market, security_type, security_status, trade_status)
                stkPriceQty['昨收盘价'] = stkprice['昨收盘价']
                stkPriceQty['涨停价'] = stkprice['涨停价']
                stkPriceQty['跌停价'] = stkprice['跌停价']
                stkPriceQty['随机中间价'] = stkprice['随机中间价']
            else:
                logger.error('不存在符合要求的持仓证券')
                stkPriceQty['返回结果'] = False
                stkPriceQty['错误原因'] = '不存在符合要求的持仓证券'

    logger.info('查询到的委托入参相关信息如下')
    dictLogging(stkPriceQty)
    return stkPriceQty

def GetStkPriceQty(stkcode, market, security_type, security_status, trade_status):
    global stkPriceQty
    rs = QueryStkpriceDB(stkcode, market, security_type, security_status, trade_status)
    stkPriceQty['证券代码'] = rs['证券代码']
    stkPriceQty['昨收盘价'] = rs['昨收盘价']
    stkPriceQty['涨停价'] = rs['涨停价']
    stkPriceQty['跌停价'] = rs['跌停价']
    stkPriceQty['随机中间价'] = rs['随机中间价']
    stkPriceQty['返回结果'] = True
    return stkPriceQty

#根据证券代码查询持仓----stkcode
def QuerySellable_qty(stkcode, Api):
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

