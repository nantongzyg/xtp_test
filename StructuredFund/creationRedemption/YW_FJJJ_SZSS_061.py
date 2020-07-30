#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceCreationRedemption")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *

class YW_FJJJ_SZSS_061(xtp_test_case):

    py_name = 'YW_FJJJ_SZSS_061'

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.update_cur_fee_rate(2, self.py_name)
        sz_restart()
        Api.trade.Logout()
        Api.trade.Login()

    def test_YW_FJJJ_SZSS_061(self):
        title='母基金申赎—赎回：费用=0.0006'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '未成交',
            'errorID': 0,
            'errorMSG': '',
            '是否生成报单': '是',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStructuredFundInfo('160127','2','26','2','0','0',case_goal['期望状态'],Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_STRUCTURED_FUND_PURCHASE_REDEMPTION'],
                'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION'],
                'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'quantity': 10
            }
            ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs, self.py_name)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # 3

if __name__ == '__main__':
    unittest.main()
        