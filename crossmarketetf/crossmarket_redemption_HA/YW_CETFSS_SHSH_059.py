#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer
from utils.env_restart import clear_data_and_restart_all
from service.mainService import *

class YW_CETFSS_SHSH_059(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('YW_CETFSS_SHSH_059')
        sql_transfer.update_cur_fee_rate(1, 'YW_CETFSS_SHSH_059')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_YW_CETFSS_SHSH_059(self):
        # -----------ETF赎回-------------
        title = ('上海ETF赎回--全部成交（数量：最大单位&费用>min，上海：99000000；上海：根据etfbaseinfo中的redemption_limit字段）')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
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
        unit_info = {
            'ticker': '530650',  # etf代码
            'etf_unit': 99.0   # etf赎回单位数
        }

        # -----------查询ETF赎回前成分股持仓-------------
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf赎回数量
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
                Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,
                                pyname = 'YW_CETFSS_SHSH_059')
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

if __name__ == '__main__':
    unittest.main()
