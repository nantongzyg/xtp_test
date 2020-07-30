#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os
sys.path.append("/home/yhl2/workspace/xtp_test/Autocase_Result/Risk/service")
from order import f
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from QueryStkPriceQty import *
from log import *
from utils import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
from SqlData_Transfer import SqlData_Transfer
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import oms_restart


class FK_FKYW_QQMM_003(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.delete_cur_risk()
        sql_transfer.insert_cur_risk('FK_FKYW_GPWT_623')
        oms_restart()
        Api.trade.Logout()
        time.sleep(2)
        Api.trade.Login()

    def test_FK_FKYW_QQMM_003(self):
        title = '默认rule25,rule0=1'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '未成交',
            'errorID':0,
            'errorMSG': '',
            '是否生成报单':'是',
            '是否是撤废':'否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        # stkparm = QueryStkPriceQty('999999','2','0','2','0','B',case_goal['期望状态'],Api)
        # # 如果下单参数获取失败，则用例失败
        # if stkparm['返回结果'] == False:
        #     rs = {
        #         '用例测试结果':stkparm['返回结果'],
        #         '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
        #     }
        #     self.assertEqual(rs['用例测试结果'], True)
        #
        # else:
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_OPTION'],
            'order_client_id': 4,
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
            'ticker': '11002290',
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_OPEN'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'price': 0.1,
            'quantity': 2
        }
        count = 1
        max_count = 101
        filename = 'FK_FKYW_QQMM_003_order'
        insert_orders_sleep(count, max_count, Api, case_goal, wt_reqs, filename)
        time.sleep(3)

        max_count = 1
        wt_reqs['order_client_id'] = 1
        insert_orders_sleep(count, max_count, Api, case_goal, wt_reqs, filename)
        time.sleep(3)

        file_reorder(filename)

        # 校验订单是否正确触发风控
        rule25_check(filename)

if __name__ == '__main__':
    unittest.main()

