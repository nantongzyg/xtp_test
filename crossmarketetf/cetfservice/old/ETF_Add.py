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
from etf_utils import split_etf_quantity


# etf二级市场买入
def etf_add(Api, market, etf_code, quantity):
    creation_redemption_unit = QueryCreationRedemUnitDB(etf_code)   # 最小申赎单位
    quantity = int(quantity * creation_redemption_unit) # 总的委托数量
    quantity_list = split_etf_quantity(quantity)  # 若etf买卖数量大于最大值，则做拆分

    limitup_lx = getUpPrice(etf_code)

    for etf_quantity in quantity_list:
        wt_reqs = {
            'market': market,
            'order_client_id': 2,
            'ticker': etf_code,  # 返回的股票代码有空格
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
            'price':limitup_lx,
            'quantity': etf_quantity
        }
        Api.trade.InsertOrder(wt_reqs)

