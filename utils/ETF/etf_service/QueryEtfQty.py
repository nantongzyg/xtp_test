#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import random
import traceback
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
import ServiceConfig
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *
from QueryFundidDB import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryEtfassetDB import *
from QueryEtfUnitDB import *
from QueryEtfinfoDB import *

sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *

stkQty = {
        '证券代码': '',
        '赎回－随机数量':0,
        '赎回－可用数量':0,
        '最小申赎单位':0,
        '返回结果':False,
        '错误原因':'',
        '申赎单元': 0
    }

# --- QueryStkprice(stkcode,market,security_type)
# ----入参1：stkcode str,当stkcode＝’999999‘时，会随机返回符合市场和证券类型要求证券代码
# ----入参2:market str,'1' 为上Ａ，‘２’为深Ａ
# ----入参3:security_type str,‘０‘为股票，'14'为单市场ETF，'15'为跨市场ETF
#-----入参４：BSflag：买卖标示 'B'买　'S'卖
# --- 返回值：dict类型 stkparm['证券代码'],stkparm['昨收盘价'],stkparm['涨停价'],stkparm['跌停价'],stkparm['跌停价'],stkparm['随机中间价'],

def QueryEtfQty(stkcode,market,security_type,security_status, trade_status,BSflag,expect_status,Api):
    #最大委托数量
    max_qty = 10000000
    #根据期望状态来决定最小委托数量
    min_qty = 0

    # 查询fundid
    fundacc = QueryFundidDB()
    global stkQty
    if BSflag == 'B':
        rs = QueryEtfinfoDB(stkcode,market,security_type,security_status, trade_status)
        if rs is not None:
            stkQty['证券代码'] = rs['证券代码']
            stkQty['返回结果'] = True
        else:
            stkQty['证券代码'] = ''
            stkQty['返回结果'] = False
            stkQty['错误原因'] = '不存在符合要求的持仓证券'
        if stkQty['证券代码'] != '':
            unit_rs = QueryEtfUnitDB(stkQty['证券代码'], market, security_type, security_status, trade_status, fundacc)
            stkQty['最小申赎单位'] = unit_rs[0][0]

    elif BSflag == 'S':
        if stkcode =='999999':
            try:
                # 查询符合入参要求的初始持仓证券代码和最小申赎单位List
                stkcode_list = QueryEtfassetDB(stkcode, market, security_type,security_status, trade_status,fundacc)
                # 查询符合要求的持仓
                i = 0
                while i < len(stkcode_list):
                    stkqty = QuerySellable_qty(stkcode_list[i][0], Api)
                    stkQty['证券代码'] = stkqty['证券代码']
                    stkQty['赎回－可用数量'] = stkqty['可用数量']
                    stkQty['最小申赎单位'] = stkcode_list[i][1]
                    i += 1
                    if stkQty['最小申赎单位'] != 0:
                        stkQty['申赎单元'] = stkQty['赎回－可用数量']/stkQty['最小申赎单位']
                    if stkQty['最小申赎单位'] <= stkQty['赎回－可用数量']:
                        break

            except MySQLdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                traceback.print_exc()
                stkQty['返回结果'] = False
                stkQty['错误原因'] = '数据库异常'


        else:
            stkqty = QuerySellable_qty(stkcode, Api)
            stkQty['证券代码'] = stkqty['证券代码']
            stkQty['赎回－可用数量'] = stkqty['可用数量']
            try:
                # 查询最小申赎单位
                stkcode_list = QueryEtfUnitDB(stkcode, market, security_type, security_status, trade_status,fundacc)
                stkQty['最小申赎单位'] = stkcode_list[0][0]
                if stkQty['最小申赎单位'] != 0:
                    stkQty['申赎单元'] = stkQty['赎回－可用数量'] / stkQty['最小申赎单位']
            except MySQLdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                traceback.print_exc()
                stkQty['返回结果'] = False
                stkQty['错误原因'] = '数据库异常'

        # 生成随机数量
        if stkQty['赎回－可用数量'] == 0:
            stkQty['返回结果'] = True
        elif stkQty['赎回－可用数量'] > max_qty:
            stkQty['申赎单元'] = int(random.randint(1, stkQty['申赎单元']))
            stkQty['赎回－随机数量'] = stkQty['申赎单元']*stkQty['最小申赎单位']
            stkQty['返回结果'] = True

        elif stkQty['赎回－可用数量'] >= stkQty['最小申赎单位'] and stkQty['赎回－可用数量'] <= max_qty:
            stkQty['申赎单元'] = int(random.randint(1, stkQty['申赎单元']))
            stkQty['赎回－随机数量'] = stkQty['申赎单元'] * stkQty['最小申赎单位']
            stkQty['返回结果'] = True
        elif stkQty['赎回－可用数量'] < stkQty['最小申赎单位']:
            stkQty['赎回－随机数量'] = stkQty['赎回－可用数量']
            stkQty['返回结果'] = True
        else:
            logger.error('不存在符合要求的持仓证券')
            stkQty['返回结果'] = False
            stkQty['错误原因'] = '不存在符合要求的持仓证券'


    logger.info('查询到的委托入参相关信息如下')
    dictLogging(stkQty)
    return stkQty

#根据证券代码查询持仓----stkcode
def QuerySellable_qty(stkcode,Api):
    stk_qty={
        '证券代码':stkcode,
        '可用数量':0,
    }
    ticker = {
        'ticker': ''
    }
    stkasset0 = Api.trade.QueryPositionSync(ticker)
    if stkasset0['data'].has_key(stkcode):
        stk_qty['可用数量'] = stkasset0['data'][stkcode]['position']['redeemable_qty']
    else:
        stk_qty['可用数量'] = 0

    return  stk_qty

