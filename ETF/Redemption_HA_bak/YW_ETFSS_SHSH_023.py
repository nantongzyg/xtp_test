#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/ETF")
from import_common import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from ETF_GetComponentShare import etf_get_all_component_stk
from ETF_Add import etf_add
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class YW_ETFSS_SHSH_023(xtp_test_case):

    def test_YW_ETFSS_SHSH_023(self):
        # -----------ETF赎回-------------
        title = '上海ETF赎回--允许现金替代：T-1日ETF拥股量0.5unit→T日ETF拥股量0.5unit→T日赎回ETF'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            'case_ID': 'ATC-204-023',
            '期望状态': '全成',
            'errorID': 0,
            'errorMSG': '',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title + ', case_ID=' + case_goal['case_ID'])
        unit_info = {
            'ticker': '580360',  # etf代码
            'etf_unit': 1,  # etf赎回单位数
            'etf_unit_buy': 0.5,  # etf买入单位数
            'etf_unit_sell': 1,  # etf卖出单位数
            'component_unit_sell': 1  # 成分股卖出单位数
        }

        # -----------二级市场买入etf-----------
        etf_add(Api,
                Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                unit_info['ticker'],
                unit_info['etf_unit_buy'])
        time.sleep(1)

        # -----------ETF赎回-------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryEtfQty(unit_info['ticker'], '1', '14', '2', '0',
                              'B', case_goal['期望状态'], Api)

        # -----------查询ETF赎回前成分股持仓-------------
        component_stk_info = etf_get_all_component_stk(unit_info['ticker'])

        # 定义委托参数信息------------------------------------------
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '用例错误原因': '获取下单参数失败, ' + stkparm['错误原因'],
            }
            etf_query_log(case_goal, rs)
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ETF'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                'ticker':
                    stkparm['证券代码'],
                'side':
                    Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'quantity':
                    int(unit_info['etf_unit'] * stkparm['最小申赎单位']),
            }
            EtfParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = etfServiceTest(Api, case_goal, wt_reqs, component_stk_info)
            etf_creation_log(case_goal, rs)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '废单'
        case_goal['errorID'] = 11010121
        case_goal['errorMSG'] = queryOrderErrorMsg(11010121)
        quantity = int(unit_info['etf_unit_sell'] *
                       stkparm['最小申赎单位'])  # 二级市场卖出的etf数量
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(stkparm['证券代码'])
        rs = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                'market':
                    Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                'ticker':
                    stkparm['证券代码'],
                'side':
                    Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs['用例测试结果'] is False:
                etf_sell_log(case_goal, rs)
                self.assertEqual(rs['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '全成'
        case_goal['errorID'] = 0
        case_goal['errorMSG'] = ''
        etf_component_info = QueryEtfComponentsInfoDB(stkparm['证券代码'],wt_reqs['market'])
        rs = {}
        for stk_info in etf_component_info:
            stk_code = stk_info[0]
            components_share = QueryEtfComponentsDB(stkparm['证券代码'],
                                                    stk_code)
            components_total = int(components_share *
                                   unit_info['component_unit_sell'])
            quantity = get_valid_amount(components_total)
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
                    quantity,
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果'] is False:
                etf_components_sell_log(case_goal, rs)
                self.assertEqual(rs['用例测试结果'], True)
        etf_components_sell_log(case_goal, rs)
        self.assertEqual(rs['用例测试结果'], True)

if __name__ == '__main__':
    unittest.main()

