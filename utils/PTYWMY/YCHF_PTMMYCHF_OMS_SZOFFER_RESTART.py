#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl/workspace/xtp_test")
from service.QueryStkPriceQty import *
sys.path.append('/home/yhl/workspace/xtp_test/service')
from ARmainservice import *
sys.path.append('/home/yhl/workspace/xtp_test/utils')
from env_restart import *
from service.ServiceConfig import *
sys.path.append('/home/yhl/workspace/xtp_test/xtp/api')
from xtp_test_case import *


class YCHF_PTMMYCHF_OMS_SZOFFER_RESTART(xtp_test_case):
    def test_query_info_before(self):
        wt_reqs_before={}
        # 查询当前用户的资金和持仓
        query_capital(Api, order_info, wt_reqs_before)  
    def test_query_info_restart(self):
        xogwsz_close()
        oms_stop()
        xogwsz_restart()
        oms_restart()
        b=Api.trade.Logout()
        a=Api.trade.Login()
    def test_query_info_squery(self):
        sleep(2)
        wt_reqs_after = {}
        # 重启后查询当前用户的资金和持仓
        query_capital(Api, restart_info, wt_reqs_after)
        # 重启环境前后，各用户订单信息校验
        result = check_result(order_info, restart_info)
        logger.warning('用例测试结果为' + str(result['用例测试结果']))
        self.assertEqual(result['用例测试结果'], True)


if __name__ == '__main__':
    unittest.main()

