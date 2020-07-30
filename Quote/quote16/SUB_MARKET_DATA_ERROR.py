#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
from ApiContext import ApiManage

class SUB_MARKET_DATA(xtp_test_case):

    def subMarketData(self, Api, stk_info, case_name, rs_expect):
        # print Api.GetApiVersion()
        def on_market_data(data, error, last):
            print error
            self.print_msg(case_name, rs_expect, error)

        Api.setSubMarketDataHandle(on_market_data)
        Api.SubscribeMarketData(stk_info)
        print 'SubscribeMarketData'
        time.sleep(2)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('%s测试正确！' % case_name)
        else:
            logger.error('%s测试错误!' % case_name)
        self.assertEqual(error, rs_expect)

    def test_hq_16_006(self):
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '', 'exchange_id': 2}
        self.subMarketData(Api, stk_info, 'hq_16_006',
                                    {'error_id': 11200003, 'error_msg': 'unknown security'})
        #Api.Logout()

    def test_hq_16_007(self):
        client_id = 7
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': 399001, 'exchange_id': 0}
        self.subMarketData(Api, stk_info, 'hq_16_007',
                                    {'error_id': 11200002, 'error_msg': 'unknown exchange'})
        #Api.Logout()

    def test_hq_16_008(self):
        client_id = 8
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': 400008, 'exchange_id': 0}
        self.subMarketData(Api, stk_info, 'hq_16_008',
                                    {'error_id': 11200002, 'error_msg': 'unknown exchange'})
        #Api.Logout()

if __name__=='__main__':
    unittest.main()
