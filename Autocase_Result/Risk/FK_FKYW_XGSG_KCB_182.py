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
from env_restart import clear_data_and_restart_sz


class FK_FKYW_XGSG_182(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.delete_cur_risk()
        sql_transfer.insert_cur_risk('FK_FKYW_GPWT_622')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        time.sleep(2)
        Api.trade.Login()

    def test_FK_FKYW_XGSG_182(self):
        title = '默认rule14,rule0=0'
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
        wt_reqs = {
            'business_type': Api.const.XTP_BUSINESS_TYPE[
                'XTP_BUSINESS_TYPE_IPOS'],
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
            'ticker': '787000',
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'quantity': 510,
            'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']

        }
        count = 1
        max_count = 10000
        filename = 'FK_FKYW_XGSG_182_order'
        insert_orders(count, max_count, Api, case_goal, wt_reqs, filename)

        time.sleep(58)
        max_count = 200
        wt_reqs['quantity'] = 500
        insert_orders_sleep(count, max_count, Api, case_goal, wt_reqs,
                            filename)
        time.sleep(3)

        file_reorder(filename)

        # 校验订单是否正确触发风控
        rule14_check_ipo2(filename)

if __name__ == '__main__':
    unittest.main()

