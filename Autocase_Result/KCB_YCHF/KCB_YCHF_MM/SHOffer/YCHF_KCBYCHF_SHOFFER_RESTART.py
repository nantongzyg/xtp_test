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


class YCHF_KCBYCHF_SHOFFER_RESTART(xtp_test_case):

    def insert_one_order(self):
        case_goal = {
            '期望状态': '全成',
            'errorID': 0,
            'errorMSG': '',
            '是否生成报单': '是',
            '是否是撤废': '否',
            # '是否是新股申购': '否',
        }
        title = '停止时下单:'

        logger.warning(title)
        stkparm = QueryStkPriceQty('688000', '1', '4', '2', '0', 'B', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '报单测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            print(stkparm['错误原因'])
            #self.assertEqual(rs['报单测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                'order_client_id':2,
                'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'price': stkparm['随机中间价'],
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
        
        print("2-重启SH 报盘:")
        # 上海offer重启
        xogwsh_restart()
        
        
        print("3-查询资金 持仓")
        ticker = ""
        # 重启后查询当前用户的资金和持仓
        query_capital_stock(Api, restart_info, ticker)
        
        # 重启环境前后，各用户订单信息校验
        result = check_result(order_info, restart_info)
        
        print("4-关闭时下单:")
        #SH offer 关闭:
        close_ogwsh()
        # 关闭时, 下单:
        ret_insert = self.insert_one_order()
        xogwsh_restart()
        
        if ret_insert == False:
            logger.warning('用例测试结果为' + str(result['用例测试结果']))
            self.assertEqual(result['用例测试结果'], True)
        else:
            logger.warning('用例测试结果为' + str(ret_insert))
            self.assertEqual(ret_insert, False)

if __name__ == '__main__':
    unittest.main()

