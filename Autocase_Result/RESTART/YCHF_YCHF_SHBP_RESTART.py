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
        logger.warning("SH BP restart: ")
        print("1-查询资金 持仓:")
        wt_reqs_before={}
        sleep(1)
        #查询用户日间委托订单不包括oms拒单
        #query_orders(Api,order_info, wt_reqs_before)
        # 查询当前用户的资金和持仓
	query_capital(Api, order_info, wt_reqs_before)
        print("2-SHBP重启:")
        sh_restart()
        c=Api.trade.Logout()
        print c
        sleep(2)
        a=Api.trade.Login()
        print a
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


        print("4-SHBP停止时下单:")
        close_ogw()
        sleep(1)

        case_goal1 = {
            '期望状态': '废单',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            'errorID': '11000330',
            'errorMSG': 'Forward message failed!',
        }
        case_goal2 = {
            '期望状态': '成功',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0
        }
        stkcodes = '110031'
        market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']
        price_type = Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL']
        ## kzzmm只能限价:
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('110031', '1', '8', '2', '8', 'B', case_goal1['期望状态'], Api)
        ret_insert = insert_Orders(case_goal1, case_goal2, stkcodes, market, price_type)

        print("5-SHBP恢复正常:")
        sh_restart()
        sleep(2)

        if ret_insert == False:
            logger.warning('用例测试结果为: ret_insert: ' + str(ret_insert))
            self.assertEqual(False, True)
        else:
            logger.warning('用例测试结果为' + str(result['用例测试结果']))
            self.assertEqual(result['用例测试结果'], True)


if __name__ == '__main__':
    unittest.main()

