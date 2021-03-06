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
from env_restart import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import SqlData_Transfer

class YW_ETFSS_SHSH_046_2(xtp_test_case):

    py_name = 'YW_ETFSS_SHSH_046_2'

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.update_cur_fee_rate(1, self.py_name)
        sh_all_restart()
        Api.trade.Logout()
        Api.trade.Login()

    def test_YW_ETFSS_SHSH_046_2(self):
        # -----------ETF赎回-------------
        title = '上海ETF赎回--交易时间对状态为“全成”进行撤单'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            'case_ID': 'ATC-204-046',
            '期望状态': '全成',
            'errorID': 11000343,
            'errorMSG': queryOrderErrorMsg(11000343),
            '是否生成报单': '是',
            '是否是撤废': '是',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title + ', case_ID=' + case_goal['case_ID'])
        unit_info = {
            'ticker': '580440',  # etf代码
            'etf_unit': 1,  # etf赎回单位数
        }

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
                    Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
                'quantity':
                    int(unit_info['etf_unit'] * stkparm['最小申赎单位']),
				'position_effect':
					Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            EtfParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = etfServiceTest(Api, case_goal, wt_reqs, component_stk_info, self.py_name)
            etf_creation_log(case_goal, rs)


if __name__ == '__main__':
    unittest.main()

