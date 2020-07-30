#!/usr/bin/python
# -*- encoding: utf-8 -*-

# 导入单元测试模块
from api.xtp_test_case import *

# import sys
# sys.path.append('/var/xtp/xtp.python/api')
print Api.trade.GetApiVersion()

def on_order(data, error):
    print 'on_order func'
    print data
    print error

def on_trade(data):
    print 'on_trade func'
    print data

def on_query_order(data, error, request_id, is_last):
    print 'on_query_order func'
    print data
    print error
    print request_id
    print is_last

def on_query_trade(data, error, request_id, is_last):
    print 'on query trade func'
    print data
    print error
    print request_id
    print is_last

Api.trade.setOrderEventHandle(on_order)
Api.trade.setTradeEventHandle(on_trade)
Api.trade.setQueryOrderHandle(on_query_order)
Api.trade.setQueryTradeHandle(on_query_trade)

# 单元测试01
############################################################################
class my_test(xtp_test_case):

    def test_limit_SZa(self):
        print '深圳Ａ股股票限价买入全成测试'

        #下单参数
        wt_reqs = {
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
            'ticker': '000002',
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'price': 35,
            'quantity': 100,
        }

        #下单
        xtp_id = Api.trade.InsertOrder(wt_reqs)
        print xtp_id

        #报单查询
        # rs_queue_order = Api.trade.QueryOrderByXTPID(xtp_id, 0)

        # print rs_QueryOrderSync

        t_idx = 0
        while True:
            t_idx += 1
            print '[%d]' % t_idx
            sleep(1)


if __name__ == '__main__':
    unittest.main()
