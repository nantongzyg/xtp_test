#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceSplitMerge")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import oms_restart

class YW_FJJJ_SZCFHB_007(xtp_test_case):
    # YW_FJJJ_SZCFHB_007
    def test_YW_FJJJ_SZCFHB_007(self):
        title='深圳分级基金拆分合并—拆分：错误的证券代码'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '废单',
            'errorID': 11000308,
            'errorMSG': 'Business type not match with security type.',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_STRUCTURED_FUND_SPLIT_MERGE'],
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
            'ticker': '150009',
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_SPLIT'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'quantity': 1000
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # 2

if __name__ == '__main__':
    unittest.main()
        