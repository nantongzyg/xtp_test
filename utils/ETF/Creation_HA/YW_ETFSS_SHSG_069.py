#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/ETF")
from import_common import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from ETF_Basket_Add_Real import etf_basket_add_real
from ETF_GetComponentShare import etf_get_all_component_stk


class YW_ETFSS_SHSG_069(xtp_test_case):

    def test_YW_ETFSS_SHSG_069(self):
        # -----------ETF申购-------------
        title = '上海ETF申购--错误的证券代码'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            'case_ID': 'ATC-202-069',
            '期望状态': '废单',
            'errorID': 11000010,
            'errorMSG': 'Failed to get ticker quotes,'
                        'ticker does not exist or can not be traded!',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title + ', case_ID=' + case_goal['case_ID'])
        unit_info = {
            'ticker': '259900',  # etf代码
        }

        # -----------ETF申购-------------
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ETF'],
            'market':
                Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'quantity':
                1000000,
        }
        EtfParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        CaseParmInsertMysql(case_goal, wt_reqs)
        rs = etfServiceTest(Api, case_goal, wt_reqs)
        etf_creation_log(case_goal, rs)


if __name__ == '__main__':
    unittest.main()

