#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *

class HQ_18_094(xtp_test_case):

    def subMarketData(self, Api, stk_info, case_name, rs_expect):
        print Api.GetApiVersion()
        def on_market_data(data, error, last):
            pass

        def on_unsub_market_data(data, error, last):
            self.print_msg(case_name, rs_expect, error)

        Api.setSubMarketDataHandle(on_market_data)
        Api.setUnSubMarketDataHandle(on_unsub_market_data)
        Api.SubscribeMarketData(stk_info)
        Api.UnSubscribeMarketData(stk_info)
        time.sleep(1)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('{0}测试正确！'.format(case_name))
        else:
            logger.error('{0}测试错误!'.format(case_name))
        self.assertEqual(error, rs_expect)

    def test_HQ_18_094(self):
        pyname = 'HQ_18_094'
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '400008', 'exchange_id': 2}
        self.subMarketData(Api, stk_info, pyname,
                                    {'error_id': 11200003, 'error_msg': 'unknown security'}) # 3
        Api.Logout()

if __name__=='__main__':
    unittest.main()
