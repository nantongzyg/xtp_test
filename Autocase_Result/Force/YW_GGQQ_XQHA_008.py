#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/option/service")
from mainService import *
from QueryStkPriceQty import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *

reload(sys)
sys.setdefaultencoding('utf-8')

class YW_GGQQ_XQHA_008(xtp_test_case):

    def test_YW_GGQQ_XQHA_008(self):
        title = '认购行权-订单确认'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '未成交',
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
  
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_OPTION'],
            # 'order_client_id':1,
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
            'ticker': '10001030',
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'position_effect':Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_FORCECLOSE'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'price': 0.0312,
            'quantity': 10
        }
        print Api.trade.InsertOrder(wt_reqs)
if __name__ == '__main__':
    unittest.main()
        