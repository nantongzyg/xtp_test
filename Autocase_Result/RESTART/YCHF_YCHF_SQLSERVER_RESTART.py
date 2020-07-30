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
sys.path.append(r"/home/yhl/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *

class YCHF_RZRQYCHF_OMS_RESTART(xtp_test_case):
    def test_query_info(self):
        logger.warning("SH Sqlserver restart: ")
        print("1-查询资金 持仓")
        wt_reqs_before={}
        #查询用户日间委托订单不包括oms拒单
        #query_orders(Api,order_info, wt_reqs_before)
        sleep(1)
        # 查询当前用户的资金和持仓
	query_capital(Api, order_info, wt_reqs_before)
        print("2-SH sqlserver重启:")
        sqlserver_stop()
        sqlserver_start()
        sleep(2)
	

        print("3-查询资金 持仓:")
        wt_reqs_after = {}
        #查询用户日间委托订单不包括oms拒单
        #query_orders(Api,restart_info, wt_reqs_after)
        # 重启后查询当前用户的资金和持仓
        query_capital(Api, restart_info, wt_reqs_after)
        
        # 重启环境前后，各用户订单信息校验
        result = check_result(order_info, restart_info)
        logger.warning('用例测试结果为' + str(result['用例测试结果']))
        self.assertEqual(result['用例测试结果'], True)

        print("4-SH sqlserver停止时下单:")
        sqlserver_stop()
        sleep(1)
        
        case_goal1 = {
            '期望状态': '废单',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            'errorID': '11112002',
            'errorMSG': 'Execute Sql string failed!',
        }
        case_goal2 = {
            '期望状态': '成功',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0
        }
        stkcode = '518800'
        market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']
        price_type = Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL']
        
        ret_insert = insert_Orders(case_goal1, case_goal2, stkcode, market, price_type)
        
        
        print("5-SZBP恢复正常:")
        sqlserver_start()
        sleep(2)
        ## 重启下match
        sh_noonclosed()
        sh_noonstart()
        sleep(3)
        
        if ret_insert == False:
            logger.warning('用例测试结果为: ret_insert: ' + str(ret_insert))
            self.assertEqual(False, True)
        else:    
            logger.warning('用例测试结果为' + str(result['用例测试结果']))
            self.assertEqual(result['用例测试结果'], True)

if __name__ == '__main__':
    unittest.main()

