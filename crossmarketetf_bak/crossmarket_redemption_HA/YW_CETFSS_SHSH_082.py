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
from crossmarketetf.cetfservice.cetf_add import cetf_add

class YW_CETFSS_SHSH_082(xtp_test_case):

    def test_YW_CETFSS_SHSH_082(self):
        # -----------ETF赎回-------------
        title = ('上海：当日赎回的证券，当日可以卖出并检查持仓')
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
            'ticker': '530770',  # etf代码
            'etf_unit_buy': 1.0,  # etf买入单位数
            'etf_unit': 1.0 ,   # etf申赎单位数
            'component_unit_sell': 1.0 # 成分股卖出单位数
        }

        # -----------T日买入etf-------------
        cetf_add(Api,
                 Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                 unit_info['ticker'],
                 unit_info['etf_unit_buy'])
        time.sleep(1)

        # 查询ETF赎回前成分股持仓
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf申赎数量
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
                quantity
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '全成'
        case_goal['errorID'] = 0
        case_goal['errorMSG'] = ''
        # 查询etf成分股代码、数量、现金替代标志等
        etf_components = query_cetf_components_info(unit_info['ticker'],1)
        # 如果卖出单位大于100，表示卖出数量；小于100，表示卖出份数
        rs3 = {}
        for component_info in etf_components:
            substitute_flag = component_info[1]
            if substitute_flag in (0,1):
                stk_code = component_info[0]
                components_share = component_info[2]
                quantity = (int(unit_info['component_unit_sell'])
                    if unit_info['component_unit_sell'] >= 100 else
                    int(components_share * unit_info['component_unit_sell']))
                limitup_px = getUpPrice(stk_code)
                wt_reqs = {
                    'business_type':
                        Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity
                }
                ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
                rs3 = serviceTest(Api, case_goal, wt_reqs)
                if rs3['用例测试结果'] is False:
                    etf_components_sell_log(case_goal, rs3)
                    self.assertEqual(rs3['用例测试结果'], True)
        etf_components_sell_log(case_goal, rs3)
        self.assertEqual(rs3['用例测试结果'], True)


if __name__ == '__main__':
    unittest.main()
