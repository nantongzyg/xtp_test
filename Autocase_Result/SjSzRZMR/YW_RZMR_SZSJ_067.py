#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from financing.service.mainService import ParmIni, serviceTest
from financing.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from financing.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class YW_RZMR_SZSJ_067(xtp_test_case):
    # YW_RZMR_SZSJ_067 YW_RZMR_SZSJ_067 YW_RZMR_SZSJ_067 YW_RZMR_SZSJ_067
    def test_YW_RZMR_SZSJ_067(self):
        title = '全部成交或撤销买--已成（费用<min）'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动

        case_goal = {
            '期望状态': '全成',
            'errorID': 0,
            'errorMSG': '',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            
            
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('003254', '2', '0', '2', '0', 'B', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_MARGIN'],
                'order_client_id':2,
                'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_MARGIN_TRADE'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT'],
                'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_ALL_OR_CANCEL'],
                'price': stkparm['涨停价'],
                'quantity': 100
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # 0

if __name__ == '__main__':
    unittest.main()
        