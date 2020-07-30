#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys,time
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from QueryStkPriceQty import *


class Test_tradepage(xtp_test_case):
    # 下单
    def test_insertOrder(order_client_id):
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
        for i in range(100):
            order_client_id = i+1
            Api.trade.Login()
            Api.trade.InsertOrder(wt_reqs)
        
   

if __name__ == '__main__':
    unittest.main()
