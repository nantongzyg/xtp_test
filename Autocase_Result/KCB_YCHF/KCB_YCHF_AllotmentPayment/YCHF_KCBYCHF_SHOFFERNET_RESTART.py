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


class YCHF_KCBYCHF_SHOFFERNET_RESTART(xtp_test_case):

    def insert_one_order(self):
        case_goal = {
            '期望状态': '全成',
            'errorID': 0,
            'errorMSG': "",
            '是否生成报单': '是',
            '是否是撤废': '否',
            '是否是新股申购': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            
            
        }
        case_goal.pop("是否是新股申购")
        #logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        ticker = '785001'
        # '1', '0', '2', '0', 'B'
        # 如果下单参数获取失败，则用例失败

        wt_reqs = {
            'business_type': Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT'],
            'order_client_id':2,
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
            'ticker': ticker,
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_LIMIT'],
            # 'price': 1,
            'quantity': 300,
            'position_effect':Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }

        rs = serviceTest(Api, case_goal, wt_reqs)
        
        sleep(0.1)
        return rs['报单测试结果']
    
    
    def test_query_info(self):
        print("1-查询资金 持仓:")
        ticker=""
        # 查询当前用户的资金和持仓
        query_capital_stock(Api, order_info, ticker)
        
        print("2-SH 报盘断网后联网:")
        # 断网并联网
        sh_offer_broken_net_start()
        
        
        print("3-查询资金 持仓")
        ticker = ""
        # 重启后查询当前用户的资金和持仓
        query_capital_stock(Api, restart_info, ticker)
        
        # 重启环境前后，各用户订单信息校验
        result = check_result(order_info, restart_info)
        
        print("4-SH 报盘断网时下单:")
        #SH offer 断网:
        sh_offer_broken_net()
        # 断网时, 下单:
        ret_insert = self.insert_one_order()
        sh_offer_start_net()
        
        if ret_insert == False:
            logger.warning('用例测试结果为' + str(result['用例测试结果']))
            self.assertEqual(result['用例测试结果'], True)
        else:
            logger.warning('用例测试结果为' + str(ret_insert))
            self.assertEqual(ret_insert, False)

if __name__ == '__main__':
    unittest.main()

