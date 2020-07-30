#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/ETF")
from import_common import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from ETF_Basket_Add_Real import etf_basket_add_real
from ETF_GetComponentShare import etf_get_all_component_stk
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg
from env_restart import clear_data_and_restart_sh
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import SqlData_Transfer
import time

class YW_ETFSS_SHSG_046(xtp_test_case):
         
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('YW_ETFSS_SHSG_044')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()
        time.sleep(2) 
  
    def test_YW_ETFSS_SHSG_046(self):
        # -----------ETF申购-------------
        title = '上海ETF申购真实ETF-资金充足，申购所需的成分股不足（可现金替代的比例>最大现金替代比例）'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            'case_ID': 'ATC-202-46',
            '期望状态': '废单',
            'errorID': 11010203,
            'errorMSG': queryOrderErrorMsg(11010203),
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title + ', case_ID=' + case_goal['case_ID'])
        unit_info = {
            'ticker': '570130',  # etf代码
            'optional_unit': 100,  # 买入允许现金替代成分股份数或者数量,大于等于100为买入数量
            'forbidden_unit': 1,  # 买入禁止现金替代成分股份数
            'etf_unit': 1,  # etf申购单位数
        }

        # -----------T日买入成分股-------------
        etf_basket_add_real(Api,
                            Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                            'B',
                            unit_info,
                            case_goal,
                            )
        time.sleep(3)

        # -----------ETF申购-------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryEtfQty(unit_info['ticker'], '1', '14', '2', '0',
                              'B', case_goal['期望状态'], Api)

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
                'market':
                    Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                'ticker':
                    stkparm['证券代码'],
                'side':
                    Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'quantity':
                    int(unit_info['etf_unit'] * stkparm['最小申赎单位']),
				'position_effect': 
				    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            EtfParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = etfServiceTest(Api, case_goal, wt_reqs)
            etf_creation_log(case_goal, rs)
        time.sleep(2)
if __name__ == '__main__':
    unittest.main()

