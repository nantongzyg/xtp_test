#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from mainService import *
from log import *

class YW_XGSG_SZSG_012(xtp_test_case):

    def test_YW_XGSG_SZSG_012(self):
        title='深圳新股申购--多次申购'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '未成交',
            'errorID': 0,
            'errorMSG': '',
            '是否生成报单': '是',
            '是否是撤废': '否',
            '是否是新股申购': '是',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type': Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_IPOS'],
            'order_client_id': 2,
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
            'ticker': '300641',
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'quantity': 10000
        }

        # 第一次下单
        title = '深圳新股申购--多次申购-第一次下单'
        logger.warning(title)

        ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # 0

        # 第二次下单
        title = '深圳新股申购--多次申购-第二次下单'
        logger.warning(title)

        case_goal['期望状态'] = '废单'
        case_goal['errorID'] = 11100000
        case_goal['errorMSG'] = '20039'
        wt_reqs['quantity'] = 3000

        ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True)  # 0

        # 第三次下单
        title = '深圳新股申购--多次申购-第三次下单'
        logger.warning(title)

        case_goal['期望状态'] = '废单'
        case_goal['errorID'] = 11100000
        case_goal['errorMSG'] = '20039'
        wt_reqs['quantity'] = 2000

        ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True)  # 0

if __name__ == '__main__':
    unittest.main()
        
