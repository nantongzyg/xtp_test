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
from crossmarketetf.cetfservice.cetf_basket_add import cetf_basket_add

class YW_CETFSS_SHSG_038(xtp_test_case):

    def test_YW_CETFSS_SHSG_038(self):
        # -----------ETF申购-------------
        title = ('上海ETF申购--现金替代比例边界值验证（最大现金比例+0.00001）')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '废单',
            'errorID': 11010203,
            'errorMSG': queryOrderErrorMsg(11010203),
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '550520',  # etf代码
            'component_unit_buy': 100.0,  # 成分股买入单位数
            'etf_unit': 1.0,  # etf申购单位数
            'etf_unit_sell': 1.0,  # etf卖出单位数
            'component_unit_sell': 0.5  # 成分股卖出单位数
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
                quantity
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '废单'
        case_goal['errorID'] = 11010121
        case_goal['errorMSG'] = queryOrderErrorMsg(11010121)
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '废单'
        case_goal['errorID'] = 11010121
        case_goal['errorMSG'] = queryOrderErrorMsg(11010121)
        # 查询etf成分股代码和数量
        etf_components = query_cetf_component_share(unit_info['ticker'])
        rs3 = {}
        for stk_code in etf_components:
            # 申购用例1-43会有上海和深圳的成分股各一支，深圳成分股为'008000'，只卖上海的
            if stk_code != '008000':
                components_share = etf_components[stk_code]
                components_total = (int(unit_info['component_unit_sell'])
                    if unit_info['component_unit_sell'] >= 100
                    else int(components_share * unit_info['component_unit_sell']))
                # 如果买入成分股包含半份，买入时数量取整了，卖出成分股是也要取整
                if str(unit_info['component_unit_buy'])[-1] == '5':
                    quantity = get_valid_amount(components_total)
                else:
                    quantity = components_total
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
