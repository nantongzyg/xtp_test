#!/usr/bin/python
# -*- encoding: utf-8 -*-
from ETF_mainService_2 import *
from ETF_EnvironmentInit import *
from etf_basket_add import *
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryCreationRedemUnitDB import *


class insertOrder(xtp_test_case):

    def test_insertOrder(self):
        #市场
        market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']
        #etf代码
        ticker = '159906'
        #etf申赎单位数
        quantity = 1
        #买卖方向
        etf_side = Api.const.XTP_SIDE_TYPE['XTP_SIDE_ETF_CREATION']
        #价格条件
        price_type = Api.const.XTP_PRICE_TYPE['XTP_PRICE_ETF_CREATION']
        #成分股买卖方向，B-买，S-卖
        stk_side = 'B'

        req = {
            'ticker': '159906',
        }

        stkasset0 = Api.trade.QueryPositionSync(req)
        print stkasset0

        creation_redemption_unit = QueryCreationRedemUnitDB(ticker)
        etf_basket_add(Api,market,stk_side,ticker,quantity)

        sleep(2)

        case_goal = {
            'case_ID': 'ATC-107-04',
            '期望状态': '全成',
            'errorID': 0,
            'errorMSG': '',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }

        wt_reqs = {
            'market': market,
            'ticker': ticker,
            'side': etf_side,
            'price_type': price_type,
            'quantity': quantity*creation_redemption_unit
        }
        rs = etf_serviceTest(Api, wt_reqs)
        logger.warning('用例case_ID=' + case_goal['case_ID'] + '执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True)

        while 1:
            time.sleep(1)

        #rs=etf_mainService(Api, case_goal, wt_reqs)


if __name__ == '__main__':
    unittest.main()
