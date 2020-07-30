#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from service.QueryStkPriceQty import *
from Autocase_Result.AbnormalRecovery.ARservice.ARmainservice import *
from utils.env_restart import *
from service.ServiceConfig import *
from xtp.api.xtp_test_case import *
from Autocase_Result.AbnormalRecovery.config import ALL_USER

# 执行用例前，将所有数据清除
#clear_data_and_restart_all()

'''
class tradeApi(object):
    const = XTPConst()
    trade = XTPTradeApi()
'''
class OMS_RESTART_GPMM_SZ(unittest.TestCase):

    def test_OMS_RESTART_GPMM_SZ(self):
        title = '异常恢复：重启OMS-股票买卖-深圳'
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        '''
        stkparm = QueryStkPriceQty('000001', '2', '0', '2', '0', 'B', '全成',
                                   tradeApi)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] == False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            for user in ALL_USER:
                # 当前用户登录
                tradeApi.trade.Login(user)
            
                wt_reqs = {
                    'business_type': tradeApi.const.XTP_BUSINESS_TYPE[
                        'XTP_BUSINESS_TYPE_CASH'],
                    'order_client_id': 2,
                    'market': tradeApi.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                    'ticker': stkparm['证券代码'],
                    'side': tradeApi.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                    'price_type': tradeApi.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                    'price': stkparm['随机中间价'],
                    'quantity': 1000
                }
                # 批量下单
                insert_order(tradeApi, wt_reqs, user)
        '''
    '''               
	# 查询当前用户的资金和持仓
        for user in ALL_USER:
			query_capital_stock(Api,order_info ,user,'000100')
	# 当前用户登出
	#tradeApi.trade.Logout()
         
    	# 重启环境
    	# oms_restart()
    	# time.sleep(10)
	'''		
	# 重启后用户登录，接收OMS推送的订单信息
    	for user in ALL_USER:
	    #service_restart(tradeApi,user)
	# 查询当前用户的资金和持仓
            query_capital_stock(Api,restart_info ,user, '000100',2)
   	# 重启环境前后，各用户订单信息校验
    	check_result(order_info, restart_info)
    	#self.assertEqual(result['结果'], True)

if __name__ == '__main__':
    unittest.main()

