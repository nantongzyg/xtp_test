#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from service.QueryStkPriceQty import *
sys.path.append('/home/yhl2/workspace/xtp_test/service')
from ARmainservice import *
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
from env_restart import *
from service.ServiceConfig import *
sys.path.append('/home/yhl2/workspace/xtp_test/xtp/api')
from xtp_test_case import *


class YCHF_RZRQYCHF_OMS_RESTART(xtp_test_case):

    def test_query_info(self):
        print("1-查询资金 持仓:")
        ticker=""
        # 查询当前用户的资金和持仓
        query_capital_stock(Api, order_info, ticker)
        
        print("2-重启SH报盘, 重启oms:")
        # 上海offer重启
        xogwsh_restart()
        oms_restart()
        print Api.trade.Logout()
        print Api.trade.Login()
        
        
        print("3-查询资金 持仓:")
        ticker = ""
        # 重启后查询当前用户的资金和持仓
        query_capital_stock(Api, restart_info, ticker)
        
        # 重启环境前后，各用户订单信息校验
        result = check_result(order_info, restart_info)
        

        
        logger.warning('用例测试结果为' + str(result['用例测试结果']))
        self.assertEqual(result['用例测试结果'], True)

if __name__ == '__main__':
    unittest.main()

