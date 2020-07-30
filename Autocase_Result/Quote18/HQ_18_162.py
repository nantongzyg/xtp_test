#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *

class HQ_18_162(xtp_test_case):

    def subTickByTick(self, Api, stk_info, case_name, rs_expect):
        print Api.GetApiVersion()
        def on_all_tick_by_tick(data, error, is_last):
            pass

        def on_unsub_tick_by_tick(data, error, is_last):
            self.print_msg(case_name, rs_expect, error)

        Api.setSubTickByTickHandle(on_all_tick_by_tick)
        Api.setUnSubscribeTickByTickHandle(on_unsub_tick_by_tick)
        Api.SubscribeTickByTick(stk_info)
        Api.UnSubscribeTickByTick(stk_info)
        time.sleep(1)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('{0}测试正确！'.format(case_name))
        else:
            logger.error('{0}测试错误!'.format(case_name))
        self.assertEqual(error, rs_expect)

    def test_HQ_18_162(self):
        pyname = 'HQ_18_162'
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '399001', 'exchange_id': 0}
        self.subTickByTick(Api, stk_info, pyname,
                                    {'error_id': 11200002, 'error_msg': 'unknown exchange'}) # 5
        Api.Logout()

if __name__=='__main__':
    unittest.main()
