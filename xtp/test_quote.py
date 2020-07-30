#!/usr/bin/python
# -*- encoding: utf-8 -*-

# 导入单元测试模块
import sys
import time
from api.xtp_test_case import *

print Api.quote.GetApiVersion()

def sub_all_market_data_cb(data):
    print 'sub_all_market_data_cb'
    print data

def print_depth_market_data(data):
    print 'print_depth_market_data'
    print data

# 单元测试01
############################################################################
class my_test(xtp_test_case):

    def test_limit_quote(self):
        print 'test_limit_quote'
        print Api.quote.Login()
        Api.quote.setSubAllMarketDataHandle(sub_all_market_data_cb)
        Api.quote.setDepthMarketDataHandle(print_depth_market_data)
        Api.quote.SubscribeAllMarketData()
        time.sleep(10) 

if __name__ == '__main__':
    unittest.main()
