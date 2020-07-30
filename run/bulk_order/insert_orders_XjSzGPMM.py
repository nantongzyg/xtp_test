#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import json
import random
import time
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from QueryStkpriceDB import QueryStkSz
from QueryStkpriceDB import QueryStkSh

# 总下单数
order_count = 10
# 下单计数
count = 0
# 存放撤单用的原xtpid
xtpids = []

stk_sz = QueryStkSz()
stk_info_sz = [ele for ele in stk_sz][0:10]

stk_sh = QueryStkSh()
stk_info_sh = [ele for ele in stk_sh][0:10]
class Order(xtp_test_case):

    def test_order(self):
        # insert_all_traded()
        #insert_all_canceled()
        insert_all_random()

# 全成
def insert_all_traded():
    global count
    while count < order_count:
        for i in xrange(len(stk_info_sz)):
            all_traded_common(stk_info_sz, i, 2)

        for i in xrange(len(stk_info_sh)):
            all_traded_common(stk_info_sh, i, 1)

def all_traded_common(stk_list, index, market):
    global count
    market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'] if market == 1 else \
        Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']

    if count == order_count:
        return
    count += 1
    wt_reqs = {
        'business_type': Api.const.XTP_BUSINESS_TYPE[
            'XTP_BUSINESS_TYPE_CASH'],
        'order_client_id': 2,
        'market': market,
        'ticker': stk_list[index][0],
        'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
        'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
        'price': stk_list[index][1] / 10000.0,
        'quantity': 200
    }
    Api.trade.InsertOrder(wt_reqs)

# 撤单
def insert_all_canceled():
    count = 0
    while count < order_count:
        for i in xrange(len(stk_info_sz)):
            print 'sz------'
            print stk_info_sz, i
            all_canceled_common(stk_info_sz, i, 2)

        for i in xrange(len(stk_info_sh)):
            print 'sh------'
            all_canceled_common(stk_info_sh, i, 1)
        count += 1

    for xtpid in xtpids:
        print xtpid
        Api.trade.CancelOrder(xtpid)

def all_canceled_common(stk_list, index, market):    
    global  xtpids
    market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'] if market == 1 else \
        Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']

    wt_reqs = {
        'business_type': Api.const.XTP_BUSINESS_TYPE[
            'XTP_BUSINESS_TYPE_CASH'],
        'order_client_id': 1,
        'market': market,
        'ticker': stk_list[index][0],
        'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
        'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
        'price': stk_list[index][1] / 10000.0,
        'quantity': 200
    }
    xtpid = Api.trade.InsertOrder(wt_reqs)    
    xtpids.append(xtpid)

# 各种成交类型轮旬下单
def insert_all_random():
    trade_typ_sz = [1, 2, 2, 3, 5] # 1-订单确认 2-全成 3-部成 5-废单    
    trade_typ_sh = [1, 2, 2, 3, 4] # 1-订单确认 2-全成 3-部成 4-废单    

    while count < order_count:
        for i in xrange(len(stk_info_sz)):
            all_random_common(stk_info_sz, i, 2, trade_typ_sz)

        for i in xrange(len(stk_info_sh)):
            all_random_common(stk_info_sh, i, 1, trade_typ_sh)

def all_random_common(stk_list, index, market, trade_type):
    global count
    market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'] if market == 1 else \
        Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']

    if count == order_count:
        return
    count += 1
    wt_reqs = {
        'business_type': Api.const.XTP_BUSINESS_TYPE[
            'XTP_BUSINESS_TYPE_CASH'],
        'order_client_id': trade_type[index % len(trade_type)],
        'market': market,
        'ticker': stk_list[index][0],
        'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
        'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
        'price': stk_list[index][1] / 10000.0,
        'quantity': 200
    }
    Api.trade.InsertOrder(wt_reqs)            
    # time.sleep(0.01)


if __name__ == '__main__':
    unittest.main()
