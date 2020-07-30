#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/ETF")
from import_common import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg
from env_restart import clear_data_and_restart_all
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import SqlData_Transfer


class YW_ETFSS_SZSG_001(xtp_test_case):
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('YW_ETFSS_SZSG_001')
        clear_data_and_restart_all()
        time.sleep(2)
        Api.trade.Logout()
        Api.trade.Login()

    def test_YW_ETFSS_SZSG_001(self):
        # -----------ETF申购-------------
        title = '深圳ETF申购--禁止现金替代：T-1日无成分股→T日申购ETF'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            'case_ID': 'ATC-202-01',
            '期望状态': '废单',
            'errorID': 11010121,
            'errorMSG': queryOrderErrorMsg(11010121),
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title + ', case_ID=' + case_goal['case_ID'])
        unit_info = {
            'ticker': '169133',  # etf代码
            'etf_unit': 1,  # etf申购单位数
            'component_unit_sell': 1  # 成分股卖出单位数
        }

        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryEtfQty(unit_info['ticker'], '2', '14', '2', '0',
                              'B', case_goal['期望状态'], Api)
        # 定义委托参数信息------------------------------------------
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '用例错误原因': '获取下单参数失败, '+stkparm['错误原因'],
            }
            etf_query_log(case_goal, rs)
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': 
                    Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ETF'],
                'market':
                    Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker':
                    stkparm['证券代码'],
                'side':
                    Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'quantity':
                    unit_info['etf_unit']*stkparm['最小申赎单位']
            }
            EtfParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = etfServiceTest(Api, case_goal, wt_reqs)
            etf_creation_log(case_goal, rs)

        # --------二级市场，卖出etf-----------
        case_goal['errorID'] = 11010121
        case_goal['errorMSG'] = queryOrderErrorMsg(11010121)
        quantity = unit_info['etf_unit'] * stkparm['最小申赎单位']  # 二级市场卖出的etf数量
        quantity_list = split_etf_quantity(quantity)
        limitup_px = getUpPrice(stkparm['证券代码'])  # 查询涨停价
        rs = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                'market':
                    Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker':
                    stkparm['证券代码'],
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
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs['用例测试结果'] is False:
                etf_sell_log(case_goal, rs)
                self.assertEqual(rs['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs)

        # ------------二级市场卖出成份股-----------
        etf_component_info = QueryEtfComponentsInfoDB(stkparm['证券代码'],wt_reqs['market'])
        rs = {}
        for stk_info in etf_component_info:
            stk_code = stk_info[0]
            components_share = QueryEtfComponentsDB(stkparm['证券代码'], stk_code)
            limitup_px = getUpPrice(stk_code)
            wt_reqs = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                'market':
                    Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker':
                    stk_code,
                'side':
                    Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
                'price':
                    limitup_px,
                'quantity':
                    components_share * unit_info['component_unit_sell']
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
