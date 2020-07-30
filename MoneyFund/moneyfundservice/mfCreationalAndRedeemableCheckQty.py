#!/usr/bin/python
# -*- encoding: utf-8 -*-
import ServiceConfig
from log import *
import  sys
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql")
from GetSecurityType import *

#可用于申购赎回数量校验
def creational_qtyCheck(init_qty,end_qty,matchQty,nomatchQty,bsflag,stkcode):
    flag=False
    #获取证券类型，0,1,2为股票，14,15为ETF
    security_type=getSecurityType(stkcode)
    #如果是’买‘
    if bsflag=='B':
        if security_type in(0,1,2):
            if init_qty + matchQty == end_qty:
                flag=True
            else:
                flag=False
        elif security_type in(14,15):
            if init_qty == end_qty:
                flag=True
            else:
                flag=False
        else:
            logger.error('获取证券类型security_type失败，证券代码='+str(stkcode))
    # 如果是’卖‘
    elif bsflag=='S':
        if security_type in(0,1,2):
            if init_qty - matchQty - nomatchQty == end_qty:
                flag=True
            else:
                flag=False
        elif security_type in(14,15):
            if init_qty == end_qty:
                flag=True
            else:
                flag=False
        else:
            logger.error('获取证券类型security_type失败，证券代码='+str(stkcode))

    return flag


#可用于赎回数量校验
def redeemable_qtyCheck(init_qty,end_qty,matchQty,bsflag,stkcode):
    flag = False
    # 获取证券类型，0,1,2为股票，14,15为ETF
    security_type = getSecurityType(stkcode)
    # 如果是’买‘
    if bsflag == 'B':
        if security_type in (14,15):
            if init_qty + matchQty == end_qty:
                flag = True
            else:
                flag = False
        elif security_type in (0,1,2):
            if init_qty == end_qty:
                flag = True
            else:
                flag = False
        else:
            logger.error('获取证券类型security_type失败，证券代码=' + str(stkcode))
    # 如果是’卖‘
    elif bsflag == 'S':
        if security_type in (14,15):
            if init_qty - matchQty == end_qty:
                flag = True
            else:
                flag = False
        elif security_type in (0,1,2):
            if init_qty == end_qty:
                flag = True
            else:
                flag = False
        else:
            logger.error('获取证券类型security_type失败，证券代码=' + str(stkcode))

    return flag
