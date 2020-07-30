#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *
from mysql.getUpOrDownPrice import getUpPrice
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from UpdateCetfqx import *
sys.path.append("/home/yhl2/workspace/xtp_test/util")
from env_restart import *
from crossmarketetf.cetfservice.cetf_basket_add import cetf_basket_add

class YW_CETFSS_SHSG_003(xtp_test_case):

    def test_YW_CETFSS_SHSG_003(self):
        # -----------ETF申购-------------
        title = ('上海ETF申购--禁止现金替代：T-1日无成分股→T日买入成分股可以申购1unitETF→T日申购ETF')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
	updateFundRightHasP()
	clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()
        case_goal = {
            '期望状态': '废单',
            'errorID': 11000555,
            'errorMSG': queryOrderErrorMsg(11000555),
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '550160',  # etf代码
            'component_unit_buy': 1.0,  # 成分股买入单位数
            'etf_unit': 1.0,  # etf申购单位数
            'etf_unit_sell': 1.0,  # etf卖出单位数
            'component_unit_sell': 1.0  # 成分股卖出单位数
        }

        # -----------T日买入成分股-------------
        cetf_basket_add(Api,
                        Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                        unit_info['ticker'],
                        unit_info['component_unit_buy'])

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
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)



if __name__ == '__main__':
    unittest.main()
