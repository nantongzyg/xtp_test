#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from service.QueryStkPriceQty import *
from Autocase_Result.AbnormalRecovery.ARservice.ARmainservice import *
from utils.env_restart import *
from xtp.api.xtp_test_case import *
from xtp.api.xtpapi import *

# 执行用例前，将所有数据清除
clear_data_and_restart_all()


class OMS_DBPMR_SZ(unittest.TestCase):
    const = XTPConst()
    trade = XTPTradeApi()
    trade.Login()

    def test_OMS_RESTART_DBPMR_SZ(self):
        title = '异常恢复：重启OMS-担保品买入-深圳'
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('000002', '2', '0', '2', '0', 'B', '全成',
                                   OMS_DBPMR_SZ)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] == False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type': OMS_DBPMR_SZ.const.XTP_BUSINESS_TYPE[
                    'XTP_BUSINESS_TYPE_MARGIN'],
                'order_client_id': 1,
                'market': OMS_DBPMR_SZ.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker': stkparm['证券代码'],
                'side': OMS_DBPMR_SZ.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                'price_type': OMS_DBPMR_SZ.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'price': stkparm['随机中间价'],
                'quantity': 200
            }
            # 批量下单，确认订单状态正确否则返回错误日志
            insert_order(OMS_DBPMR_SZ, wt_reqs)



if __name__ == '__main__':
    unittest.main()

