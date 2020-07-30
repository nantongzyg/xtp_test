#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *

class HQ_18_048(xtp_test_case):

    def subOrderBook(self, Api, stk_info, case_name, rs_expect):
        print Api.GetApiVersion()
        def on_order_book(data, error, last):
            self.print_msg(case_name, rs_expect, error)

        Api.setSubOrderBookHandle(on_order_book)
        Api.SubscribeOrderBook(stk_info)
        time.sleep(1)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('{0}测试正确！'.format(case_name))
        else:
            logger.error('{0}测试错误!'.format(case_name))
        self.assertEqual(error, rs_expect)

    def test_HQ_18_048(self):
        pyname = 'HQ_18_048'
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '', 'exchange_id': 1}
        self.subOrderBook(Api, stk_info, pyname,
                                    {'error_id': 11200003, 'error_msg': 'unknown security'}) # 1
        Api.Logout()

if __name__=='__main__':
    unittest.main()
