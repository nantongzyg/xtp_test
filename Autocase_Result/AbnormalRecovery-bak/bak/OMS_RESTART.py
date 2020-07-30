#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from service.QueryStkPriceQty import *
from Autocase_Result.AbnormalRecovery.ARservice.ARmainservice import *
from utils.env_restart import *
from service.ServiceConfig import *
from xtp.api.xtp_test_case import *


# 执行用例前，将所有数据清除
clear_data_and_restart_all()


class TradeApi(object):
    const = XTPConst()
    trade = XTPTradeApi()


class OMS_RESTART(unittest.TestCase):

    def test_query_info_before(self):
        wt_reqs_before={}
        # 查询当前用户的资金和持仓
        query_capital_stock(TradeApi, order_info, wt_reqs_before)
        # 查询信用账户信息
        query_credit_account(TradeApi, order_info)
        # 查询负债合约
        query_debt_contract(TradeApi, order_info)
        # 查询可融券头寸信息
        query_marginable_positions(TradeApi, order_info, wt_reqs_before)
        # 当前用户登出
        TradeApi.trade.Logout()

    def test_env_restart(self):
        # 重启环境
        oms_restart()
        time.sleep(3)

    def test_query_info_after(self):
        wt_reqs_after = {}
        # 重启后查询当前用户的资金和持仓
        query_capital_stock(TradeApi, restart_info, wt_reqs_after)
        # 重启后查询信用账户信息
        query_credit_account(TradeApi, restart_info)
        # 重启后查询负债合约
        query_debt_contract(TradeApi, restart_info)
        # 查询可融券头寸信息
        query_marginable_positions(TradeApi, order_info, wt_reqs_after)
        # 重启环境前后，各用户订单信息校验
        result = check_result(order_info, restart_info)
        self.assertEqual(result['结果'], True)


if __name__ == '__main__':
    unittest.main()

