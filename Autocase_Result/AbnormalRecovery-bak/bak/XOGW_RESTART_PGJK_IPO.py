#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
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

class XOGW_RESTART_PGJK_IPO(unittest.TestCase):

    def test_XOGW_RESTART_PGJK_IPO(self):

        title = '异常恢复：重启报盘-配股缴款、新股申购'
        logger.warning(title)

        for user in ALL_USER:
            # 当前用户登录
            tradeApi.trade.Login(user)

            wt_reqs = {
                'business_type': tradeApi.const.XTP_BUSINESS_TYPE[
                    'XTP_BUSINESS_TYPE_ALLOTMENT'],
                'order_client_id': 1,
                'market': tradeApi.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker': '080001',
                'side': tradeApi.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                'price_type': tradeApi.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'price': 0,
                'quantity': 1000
            }

            # 配股缴款下单,深圳配股缴款仅有未成交和已撤两种状态
            service_insertorder(tradeApi, wt_reqs, user)
            service_insertorder(tradeApi, wt_reqs, user)
            service_cancleorder(tradeApi, wt_reqs, user)

            # 配股缴款下单,上海配股缴款仅有未成交和全成两种状态，无法撤单
            wt_reqs['ticker'] = '700001'
            wt_reqs['market'] = tradeApi.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']
            for client_id in range(1,3):
                wt_reqs['order_client_id'] = client_id
                service_insertorder(tradeApi, wt_reqs, user)

            # 新股申购下单，新股申购仅有未成交状态
            wt_reqs['business_type'] = tradeApi.const.XTP_BUSINESS_TYPE[
                'XTP_BUSINESS_TYPE_IPOS']
            wt_reqs['order_client_id'] = 1

            wt_reqs['market'] = tradeApi.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']
            wt_reqs['ticker'] = '002846'
            service_insertorder(tradeApi, wt_reqs, user)
            wt_reqs['market'] = tradeApi.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']
            wt_reqs['ticker'] = '732818'
            service_insertorder(tradeApi, wt_reqs, user)

            # 查询当前用户的资金和持仓
            query_capital_stock(tradeApi,order_info ,user,wt_reqs['ticker'])
            # 当前用户登出
            tradeApi.trade.Logout()

        # 重启环境
        xogwsh_restart()
        xogwsz_restart()
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

