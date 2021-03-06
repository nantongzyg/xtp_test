#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from Autocase_Result.AbnormalRecovery.ARservice.ARmainservice import *
from option.service.OptQueryStkPriceQty import QueryStkPriceQty
from utils.env_restart import *
from service.ServiceConfig import *
from xtp.api.xtp_test_case import *
from xtp.api.config import ALL_USER_OPTION


# 执行用例前，将所有数据清除
clear_data_and_restart_all()

class tradeApi(object):
    const = XTPConst()
    trade = XTPTradeApi(ALL_USER_OPTION[0])

class OMS_RESTART_OPTION(unittest.TestCase):

    def test_OMS_RESTART_OPTION(self):

        title = '异常恢复：重启OMS-期权'
        logger.warning(title)

        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、期望状态、Api
        stkparm = QueryStkPriceQty('10001030', '1', '*', '1', '0', 'P', '全成', tradeApi)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        for user in ALL_USER_OPTION:
            # 当前用户登录
            tradeApi.trade.Login(user)

            wt_reqs = {
                'business_type': tradeApi.const.XTP_BUSINESS_TYPE[
                    'XTP_BUSINESS_TYPE_OPTION'],
                'order_client_id': 2,
                'market': tradeApi.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                'ticker': '10001030',
                'side': tradeApi.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE[
                    'XTP_POSITION_EFFECT_OPEN'],
                'price_type': tradeApi.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'price':stkparm['随机中间价'],
                'quantity': 2
            }

            service_insertorder(tradeApi, wt_reqs, user)
            service_insertorder(tradeApi, wt_reqs, user)
            wt_reqs['order_client_id']=3
            service_cancleorder(tradeApi, wt_reqs, user)
            service_cancleorder(tradeApi, wt_reqs, user)
            # insert_order_option(tradeApi, wt_reqs, user)
            time.sleep(3)

            # 查询当前用户的资金和持仓
            query_capital_stock(tradeApi,order_info ,user,wt_reqs['ticker'])
            # 当前用户登出
            tradeApi.trade.Logout()

        # 重启环境
        xogwsh_restart()
        xogwsz_restart()
        time.sleep(3)

        for user in ALL_USER_OPTION:
            # 重启后用户登录，接收OMS推送的订单信息
            service_restart(tradeApi,user)
            # 查询当前用户的资金和持仓
            query_capital_stock(tradeApi,restart_info ,user,wt_reqs['ticker'])

        # 重启环境前后，各用户订单信息校验
        result = check_result(order_info, restart_info)
        self.assertEqual(result['结果'], True)


if __name__ == '__main__':
    unittest.main()

