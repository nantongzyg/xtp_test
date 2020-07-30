#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/Autocase_Result/Risk/service")
from utils import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF")
from import_common import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import SqlData_Transfer
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from ETF_Basket_Add_Real import etf_basket_add_real
from ETF_GetComponentShare import etf_get_all_component_stk
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import clear_data_and_restart_sz


class FK_FKYW_ETFSS_312(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.delete_cur_risk()
        sql_transfer.insert_cur_risk('FK_FKYW_GPWT_621')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        time.sleep(5)
        login_session = Api.trade.Login()
        print 1111111111111111
        print login_session
        time.sleep(2)

    def test_FK_FKYW_ETFSS_312(self):
        # -----------ETF申购-------------
        title = '默认rule14,rule0=1'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
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
            'ticker': '179910',  # etf代码
            'etf_unit': 1,  # etf申购单位数
        }

        # -----------ETF申购-------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryEtfQty(unit_info['ticker'], '2', '14', '2', '0',
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
                    Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker':
                    stkparm['证券代码'],
                'side':
                    Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'quantity':
                    int(unit_info['etf_unit'] * stkparm['最小申赎单位']) + 1,
            }
            count = 1
            max_count = 9000
            filename1 = 'FK_FKYW_ETFSS_312_order1'
            filename2 = 'FK_FKYW_ETFSS_312_order2'
            insert_orders(count, max_count, Api, case_goal, wt_reqs, filename1)

            max_count = 1000
            wt_reqs['quantity'] = int(unit_info['etf_unit'] * stkparm['最小申赎单位'])
            insert_orders(count, max_count, Api, case_goal, wt_reqs, filename1)

            time.sleep(58)
            max_count = 200
            insert_orders_sleep(count, max_count, Api, case_goal, wt_reqs,
                                filename2)
            time.sleep(3)
            file_reorder(filename1)
            file_reorder(filename2)

            # 校验订单是否正确触发风控
            rule14_check_etf(filename1, filename2)


if __name__ == '__main__':
    unittest.main()

