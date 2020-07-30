#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/ETF")
from import_common import *


class YW_ETFSS_SZSH_061(xtp_test_case):

    def test_YW_ETFSS_SZSH_061(self):
        # -----------ETF申购-------------
        title = '深圳ETF赎回--错误的买卖方向'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            'case_ID': 'ATC-204-060',
            '期望状态': '废单',
            'errorID': 11000114,
            'errorMSG': 'Parameter side invalid!',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title + ', case_ID=' + case_goal['case_ID'])
        unit_info = {
            'ticker': '179850',  # etf代码
            'etf_unit': 1,  # etf申购单位数
        }

        # -----------ETF申购-------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryEtfQty(unit_info['ticker'], '2', '14', '2', '0',
                              'B', case_goal['期望状态'], Api)

        # -----------ETF申购-------------
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ETF'],
            'market':
                Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'quantity':
                int(unit_info['etf_unit'] * stkparm['最小申赎单位']),
        }
        EtfParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        CaseParmInsertMysql(case_goal, wt_reqs)
        rs = etfServiceTest(Api, case_goal, wt_reqs)
        etf_creation_log(case_goal, rs)


if __name__ == '__main__':
    unittest.main()

