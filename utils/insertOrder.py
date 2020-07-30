#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from QueryStkPriceQty import *
import time

a = []
i = 0

def insertOrder(order_client_id):
    case_goal = {
        'case_ID': 'ATC-103-19',
        '期望状态': '全成',
        'errorID': 0,
        'errorMSG': '',
        '是否生成报单': '是',
        '是否是撤废': '否',
        'xtp_ID': 0,
        'cancel_xtpID': 0,
    }
    stkparm = QueryStkPriceQty('999999', '2', '0', '2', '0', 'B', case_goal['期望状态'], Api)
    wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_FORWARD_BEST'],
                'price': stkparm['涨停价'],
                'quantity': 200
                }
    wt_reqs['order_client_id'] = order_client_id
    Api.trade.InsertOrder(wt_reqs)

# 报单分页查询
def test_orderpage(self):
    
    def pagedate(data, req_count, order_sequence, query_reference, request_id, is_last):
        #print data,is_last
        global i
	for k in data.keys():
            if 'order_cancel_xtp_id' in k:
               i +=1
               a.append(i)

    Api.trade.setQueryOrderByPageHandle(pagedate)
    Api.trade.QueryOrdersByPage({'req_count':13,'reference':198})
    time.sleep(0.5)
    rs = a[-1]
    self.assertEqual(rs, 3) 

# 成交分页查询
def test_tradepage():
    def pagedate(data, req_count, trade_sequence, query_reference, request_id, is_last):
        print data,is_last

    Api.trade.setQueryTradeByPageHandle(pagedate)
    Api.trade.QueryTradesByPage({'req_count':10,'reference':0})
    time.sleep(0.5)
if __name__ == '__main__':
    ''' 
    for i in range(100):
        order_client_id = i+1
        #print order_client_id
        Api.trade.Login()
        insertOrder(order_client_id)
    ''' 
    #test_orderpage()
    test_tradepage()
