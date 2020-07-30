#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test//xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test//service")
from ServiceConfig import *
from ARmainservice import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test//mysql")
from CaseParmInsertMysql import *
sys.path.append("/home/yhl2/workspace/xtp_test//utils")
from QueryOrderErrorMsg import queryOrderErrorMsg
from env_restart import *

class YCHF_PGYCHF_OMS_SHOffer_002(xtp_test_case):
    def setUp(self):
        #clear_sse_data_and_restart_oms()
        #Api.trade.Logout()
        #Api.trade.Login()
        pass
        
    # YCHF_PGYCHF_OMS_SHOffer_002
    def test_YCHF_PGYCHF_OMS_SHOffer_002(self):
        title = '先重启上海报盘再重启OMS（沪A-订单确认）'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动

        case_goal = {
            '期望状态': '未成交',
            'errorID': 0,
            'errorMSG': queryOrderErrorMsg(0),
            '是否生成报单': '是',
            '是否是撤废': '否',
            '是否是新股申购': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            
            
        }
        case_goal.pop("是否是新股申购")
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        ticker = '785001'
        # '1', '0', '2', '0', 'B'
        # 如果下单参数获取失败，则用例失败

        wt_reqs = {
            'business_type': Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT'],
            'order_client_id':1,
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
            'ticker': ticker,
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_LIMIT'],
            # 'price': 1,
            'quantity': 300,
            'position_effect':Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }

        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['报单测试结果']) + ','
                       + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['报单测试结果'], True) # 215

if __name__ == '__main__':
    unittest.main()
        