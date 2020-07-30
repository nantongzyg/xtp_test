#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *
from crossmarketetf.cetfservice.cetf_basket_add_real import cetf_basket_add_real

class YW_CETFSS_SHSG_094_1(xtp_test_case):

    def test_YW_CETFSS_SHSG_094_1(self):
        # -----------ETF申购-------------
        title = ('上海ETF申购--交易时间对状态为“未成交/全成/废单”进行撤单_全成')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '全成',
            'errorID': 11000343,
            'errorMSG': queryOrderErrorMsg(11000343),
            '是否生成报单': '是',
            '是否是撤废': '是',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '540180',
            #'ticker': '512070',  # etf代码
            'optional_unit': 1.0,  # 买入允许现金替代成分股份数
            'forbidden_unit': 1.0,  # 买入禁止现金替代成分股份数
            'etf_unit': 1.0   # etf申购单位数
        }

        # -----------T日买入成分股-------------
        cetf_basket_add_real(Api,
                        1.0,
                        unit_info,
                        )
        time.sleep(10)

        # -----------查询ETF申购前成分股持仓-------------
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf申购数量
        quantity = int(unit_info['etf_unit'] * unit_number)

        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ETF'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'quantity':
                quantity
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

if __name__ == '__main__':
    unittest.main()
