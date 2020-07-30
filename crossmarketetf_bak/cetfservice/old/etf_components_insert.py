#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
import vnxtptrade
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryCreationRedemUnitDB import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from mainService import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from getUpOrDownPrice import *


#根据etf代码买入一篮子股票，只买非必用现金替代部分
def etf_add(Api,market,bsflag,etf_code,quantity,case_goal = {}):
    creation_redemption_unit = QueryCreationRedemUnitDB(etf_code)   #最小申赎单位
    quantity = int(quantity * creation_redemption_unit) #总的委托数量
    quantity_list = []
    while quantity > 1000000:
        quantity_list.append(1000000)
        quantity = quantity - 1000000
    if quantity < 1000000:
        quantity_list.append(quantity)
    elif quantity == 1000000:
        quantity_list.append(quantity)

    side = getSide(Api,bsflag)
    limitup_lx = getUpPrice(etf_code)

    comp_rs = {
        '用例测试结果': False,
        '用例错误源': '',
        '用例错误原因': '',
    }
    for etf_quantity in quantity_list:
        wt_reqs = {
            'market': market,
            'ticker': etf_code,  # 返回的股票代码有空格
            'side': side,
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
            'price':limitup_lx,
            'quantity': etf_quantity
        }

        if case_goal == {}:
            Api.trade.InsertOrder(wt_reqs)
        else:
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果'] == False:
                comp_rs['用例测试结果'] = rs['用例测试结果']
                comp_rs['用例错误源'] = rs['用例错误源']
                comp_rs['用例错误原因'] = rs['用例错误原因']
            else:
                comp_rs['用例测试结果'] = True

            return comp_rs

def getSide(Api,bsflag):
    if bsflag == 'B':
        return Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY']
    elif bsflag == 'S':
        return Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']

