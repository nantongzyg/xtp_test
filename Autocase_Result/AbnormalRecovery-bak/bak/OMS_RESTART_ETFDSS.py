#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from service.QueryStkPriceQty import *
from Autocase_Result.AbnormalRecovery.ARservice.ARmainservice import *
from utils.env_restart import *
from service.ServiceConfig import *
from xtp.api.xtp_test_case import *
from xtp.api.config import ALL_USER

# 执行用例前，将所有数据清除
clear_data_and_restart_all()

class tradeApi(object):
    const = XTPConst()
    trade = XTPTradeApi(ALL_USER[0])

class OMS_RESTART_ETFSS(unittest.TestCase):

    def test_OMS_RESTART_ETFSS(self):

        title = '异常恢复：重启OMS-ETF申赎(单市场+跨市场)'
        logger.warning(title)

        for user in ALL_USER:
            # 当前用户登录
            tradeApi.trade.Login(user)

            wt_reqs = {
                'business_type': tradeApi.const.XTP_BUSINESS_TYPE[
                    'XTP_BUSINESS_TYPE_ETF'],
                'order_client_id': 2,
                'market': tradeApi.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                'ticker': '570250',
                'side': tradeApi.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE'],
                'price_type': tradeApi.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'quantity': 1000000
            }
            # ---------------------单市场申赎----------------------------------
            # 上海申购
            service_insertorder(tradeApi, wt_reqs, user)
            # 上海赎回
            wt_reqs['ticker'] = '580460'
            wt_reqs['side'] = tradeApi.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION']
            service_insertorder(tradeApi, wt_reqs, user)
            # 深圳赎回
            wt_reqs['market'] = tradeApi.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']
            wt_reqs['ticker'] = '179890'
            service_insertorder(tradeApi, wt_reqs, user)
            # 深圳申购
            wt_reqs['ticker'] = '169151'
            wt_reqs['side'] = tradeApi.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE']
            service_insertorder(tradeApi, wt_reqs, user)
            # ---------------------跨市场申赎-----------------------------------
            # 上海申购
            wt_reqs['market'] = tradeApi.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']
            wt_reqs['ticker'] = '540150'
            service_insertorder(tradeApi, wt_reqs, user)
            # 上海赎回
            wt_reqs['side'] = tradeApi.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION']
            wt_reqs['ticker'] = '530790'
            service_insertorder(tradeApi, wt_reqs, user)
            time.sleep(3)

            # 查询当前用户的资金和持仓
            query_capital_stock(tradeApi,order_info ,user,wt_reqs['ticker'])
            # 当前用户登出
            tradeApi.trade.Logout()

        # 重启环境
        oms_restart()
        time.sleep(3)

        for user in ALL_USER:
            # 重启后用户登录，接收OMS推送的订单信息
            service_restart(tradeApi,user)
            # 查询当前用户的资金和持仓
            query_capital_stock(tradeApi,restart_info ,user,wt_reqs['ticker'])

        # 重启环境前后，各用户订单信息校验
        result = check_result(order_info, restart_info)
        self.assertEqual(result['结果'], True)


if __name__ == '__main__':
    unittest.main()

