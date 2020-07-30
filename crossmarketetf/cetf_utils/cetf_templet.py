#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
模板类型说明：
templet_cetf_str1：跨市场ETF申购模板,单支成分股，T日不买入成分股，重启环境
templet_cetf_str2：跨市场ETF申购模板,单支成分股，T日不买入成分股
templet_cetf_str3：跨市场ETF申购模板,单支成分股，T日买入成分股
templet_cetf_str4：跨市场ETF申购模板,模拟真实etf，T日买入成分股，申购
templet_cetf_str5：跨市场ETF申购模板，模拟真实etf，T日买入成分股，重启环境，申购
templet_cetf_str6：跨市场ETF申购模板，模拟真实etf，修改费率,重启环境
templet_cetf_str7：跨市场ETF申购模板，模拟真实etf，直接申购
templet_cetf_str8：跨市场ETF申购模板，用例 110/111，买入成分股，申购，卖出ETF
templet_cetf_str9：跨市场ETF申购模板，用例 112，买入成分股，申购，卖出ETF
templet_cetf_str10：
templet_cetf_str11：跨市场ETF赎回模板,单支成分股，重启环境，赎回/卖出etf/卖成分股
templet_cetf_str12：跨市场ETF赎回模板,单支成分股，赎回/卖出etf/卖成分股
templet_cetf_str13：跨市场ETF赎回模板,单支成分股，T日买入etf，赎回/卖出etf/卖成分股
templet_cetf_str14：跨市场ETF赎回模板，模拟真实etf，赎回/卖出etf/卖成分股
templet_cetf_str15：跨市场ETF赎回模板，模拟真实etf，重启环境，赎回/卖出etf/卖成分股
templet_cetf_str16：跨市场ETF赎回模板，模拟真实etf，修改费率,重启环境，赎回
templet_cetf_str17：跨市场ETF赎回模板，模拟真实etf，赎回
templet_cetf_str18：跨市场ETF赎回模板，模拟真实etf，赎回/申购/卖赎回的成分股
templet_cetf_str19：跨市场ETF赎回模板，模拟真实etf，申购/赎回/卖申购的etf
templet_cetf_str20：跨市场ETF赎回模板，模拟真实etf，购买etf/赎回/申购/卖赎回的成分股
templet_cetf_str21：跨市场ETF赎回模板，模拟真实etf，赎回/卖赎回的成分股
templet_cetf_str22：跨市场ETF赎回模板，模拟真实etf，T日买入etf，赎回
templet_cetf_str23：跨市场ETF赎回模板，模拟真实etf，T日买入etf，赎回,卖出etf

"""

# 跨市场ETF申购模板,单支成分股，T日不买入成分股，重启环境
templet_cetf_str1 = '''#!/usr/bin/python
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
from mysql.getUpOrDownPrice import getUpPrice

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        # -----------ETF申购-------------
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s,  # etf申购单位数
            'etf_unit_sell': %s,  # etf卖出单位数
            'component_unit_sell': %s  # 成分股卖出单位数
        }

        # -----------查询ETF申购前成分股持仓-------------
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf申购数量
        quantity = int(unit_info['etf_unit'] * unit_number)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 查询etf成分股代码和数量
        etf_components = query_cetf_component_share(unit_info['ticker'])
        rs3 = {}
        for stk_code in etf_components:
            # 申购用例1-43会有上海和深圳的成分股各一支，深圳成分股为'008000'，只卖上海的
            if stk_code != '008000':
                components_share = etf_components[stk_code]
                quantity = (int(unit_info['component_unit_sell'])
                    if unit_info['component_unit_sell'] >= 100
                    else int(components_share * unit_info['component_unit_sell']))
                limitup_px = getUpPrice(stk_code)
                wt_reqs = {
                    'business_type':
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''

# 跨市场ETF申购模板，单支成分股，T日不买入成分股
templet_cetf_str2 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *
from mysql.getUpOrDownPrice import getUpPrice

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF申购-------------
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s,  # etf申购单位数
            'etf_unit_sell': %s,  # etf卖出单位数
            'component_unit_sell': %s # 成分股卖出单位数
        }

        # -----------查询ETF申购前成分股持仓-------------
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf申购数量
        quantity = int(unit_info['etf_unit'] * unit_number)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 查询etf成分股代码和数量
        etf_components = query_cetf_component_share(unit_info['ticker'])
        # 如果卖出单位大于100，表示卖出数量；小于100，表示卖出份数
        rs3 = {}
        for stk_code in etf_components:
            # 申购用例1-43会有上海和深圳的成分股各一支，深圳成分股为'008000'，只卖上海的
            if stk_code != '008000':
                components_share = etf_components[stk_code]
                quantity = (int(unit_info['component_unit_sell'])
                    if unit_info['component_unit_sell'] >= 100
                    else int(components_share * unit_info['component_unit_sell']))
                limitup_px = getUpPrice(stk_code)
                wt_reqs = {
                    'business_type':
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''

# 跨市场ETF申购模板，单支成分股，T日买入成分股
templet_cetf_str3 = '''#!/usr/bin/python
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

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF申购-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'component_unit_buy': %s,  # 成分股买入单位数
            'etf_unit': %s,  # etf申购单位数
            'etf_unit_sell': %s,  # etf卖出单位数
            'component_unit_sell': %s  # 成分股卖出单位数
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
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
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''

# 跨市场ETF申购模板，模拟真实etf，T日买入成分股，申购
templet_cetf_str4 = '''#!/usr/bin/python
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

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF申购-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'optional_unit': %s,  # 买入允许现金替代成分股份数
            'forbidden_unit': %s,  # 买入禁止现金替代成分股份数
            'etf_unit': %s   # etf申购单位数
        }

        # -----------T日买入成分股-------------
        cetf_basket_add_real(Api,
                        %s,
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
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
'''


# 跨市场ETF申购模板，模拟真实etf，T日买入成分股，重启环境，申购
templet_cetf_str5 = '''#!/usr/bin/python
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
from crossmarketetf.cetfservice.cetf_basket_add_real import cetf_basket_add_real


class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        # -----------ETF申购-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'optional_unit': %s,  # 买入允许现金替代成分股份数
            'forbidden_unit': %s,  # 买入禁止现金替代成分股份数
            'etf_unit': %s   # etf申购单位数
        }

        # -----------T日买入成分股-------------
        cetf_basket_add_real(Api,
                        %s,
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
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
'''


# 跨市场ETF申购模板，模拟真实etf，修改费率，重启环境
templet_cetf_str6 = '''#!/usr/bin/python
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

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.update_cur_fee_rate(1, '%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        # -----------ETF申购-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s   # etf申购单位数
        }

        # -----------查询ETF申购前成分股持仓-------------
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf申购数量
        quantity = int(unit_info['etf_unit'] * unit_number)

        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,
                                pyname = '%s')
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

if __name__ == '__main__':
    unittest.main()
'''

# 跨市场ETF申购模板，模拟真实etf，直接申购
templet_cetf_str7 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF申购-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s   # etf申购单位数
        }

        # -----------查询ETF申购前成分股持仓-------------
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf申购数量
        quantity = int(unit_info['etf_unit'] * unit_number)

        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
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
'''

# 跨市场ETF申购模板，用例 110，买入成分股，申购，卖出ETF
templet_cetf_str8 = '''#!/usr/bin/python
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

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF申购-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'component_unit_buy': %s,  # 成分股买入单位数
            'etf_unit': %s,  # etf申购单位数
            'etf_unit_sell': %s,  # etf卖出单位数
            'component_unit_sell': %s  # 成分股卖出单位数
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)


if __name__ == '__main__':
    unittest.main()
'''

# 跨市场ETF申购模板，用例 112，买入成分股，申购，卖出ETF
# ETF卖出优先使用当天申购的ETF，其次使用昨日持仓的ETF
templet_cetf_str9 = '''#!/usr/bin/python
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

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF申购-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'component_unit_buy': %s,  # 成分股买入单位数
            'etf_unit': %s,  # etf申购单位数
            'etf_unit_sell': %s,  # etf卖出单位数
            'component_unit_sell': %s  # 成分股卖出单位数
        }

        # -----------T日买入成分股-------------
        cetf_basket_add(Api,
                        Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                        unit_info['ticker'],
                        unit_info['component_unit_buy'])

        # -----------申购前查询etf昨仓-------------
        stkcode = {'ticker': unit_info['ticker']}
        stkasset_start = Api.trade.QueryPositionSync(stkcode)
        stkasset_start =(stkasset_start['data'][unit_info['ticker']]['position']
         ['purchase_redeemable_qty'])

        # -----------查询ETF申购前成分股持仓-------------
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf申购数量
        quantity = int(unit_info['etf_unit'] * unit_number)

        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
           	'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)

        #申购并且卖出etf，查询etf昨仓
        stkasset_end = Api.trade.QueryPositionSync(stkcode)
        stkasset_end = (stkasset_end['data'][unit_info['ticker']]['position']
         ['purchase_redeemable_qty'])

        self.assertEqual(stkasset_start,stkasset_end)

if __name__ == '__main__':
    unittest.main()
'''


# 跨市场ETF赎回模板,单支成分股，T日不买入etf，重启环境
templet_cetf_str11 = '''#!/usr/bin/python
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
from mysql.getUpOrDownPrice import getUpPrice

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        # -----------ETF赎回-------------
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s,  # etf赎回单位数
            'etf_unit_sell': %s,  # etf卖出单位数
            'component_unit_sell': %s  # 成分股卖出单位数
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 查询etf成分股代码和数量
        etf_components = query_cetf_component_share(unit_info['ticker'])
        rs3 = {}
        for stk_code in etf_components:
            # 赎回用例1-25会有上海和深圳的成分股各一支，深圳成分股为'008000'，只卖上海的
            if stk_code != '008000':
                components_share = etf_components[stk_code]
                quantity = (int(unit_info['component_unit_sell'])
                    if unit_info['component_unit_sell'] >= 100
                    else int(components_share * unit_info['component_unit_sell']))

                limitup_px = getUpPrice(stk_code)
                wt_reqs = {
                    'business_type':
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''

# 跨市场ETF赎回模板，单支成分股，T日不买入etf
templet_cetf_str12 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *
from mysql.getUpOrDownPrice import getUpPrice

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF赎回-------------
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s,  # etf赎回单位数
            'etf_unit_sell': %s,  # etf卖出单位数
            'component_unit_sell': %s # 成分股卖出单位数
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 查询etf成分股代码和数量
        etf_components = query_cetf_component_share(unit_info['ticker'])
        # 如果卖出单位大于100，表示卖出数量；小于100，表示卖出份数
        rs3 = {}
        for stk_code in etf_components:
            # 赎回用例1-25会有上海和深圳的成分股各一支，深圳成分股为'008000'，只卖上海的
            if stk_code != '008000':
                components_share = etf_components[stk_code]
                quantity = (int(unit_info['component_unit_sell'])
                    if unit_info['component_unit_sell'] >= 100
                    else int(components_share * unit_info['component_unit_sell']))
                limitup_px = getUpPrice(stk_code)
                wt_reqs = {
                    'business_type':
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''

# 跨市场ETF赎回模板，单支成分股，T日买入etf
templet_cetf_str13 = '''#!/usr/bin/python
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

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF赎回-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit_buy': %s,  # etf买入单位数
            'etf_unit': %s,  # etf赎回单位数
            'etf_unit_sell': %s,  # etf卖出单位数
            'component_unit_sell': %s  # 成分股卖出单位数
        }

        # -----------T日买入etf-------------
        cetf_add(Api,
                 Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                 unit_info['ticker'],
                 unit_info['etf_unit_buy'])

        # -----------查询ETF赎回前成分股持仓-------------
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf赎回数量
        quantity = int(unit_info['etf_unit'] * unit_number)

        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 查询etf成分股代码和数量
        etf_components = query_cetf_component_share(unit_info['ticker'])
        rs3 = {}
        for stk_code in etf_components:
            # 赎回用例1-25会有上海和深圳的成分股各一支，深圳成分股为'008000'，只卖上海的
            if stk_code != '008000':
                components_share = etf_components[stk_code]
                quantity = (int(unit_info['component_unit_sell'])
                    if unit_info['component_unit_sell'] >= 100
                    else int(components_share * unit_info['component_unit_sell']))
                limitup_px = getUpPrice(stk_code)
                wt_reqs = {
                    'business_type':
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''

# 跨市场ETF赎回模板，模拟真实etf，T日不买入etf
templet_cetf_str14 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from crossmarketetf.cetfmysql.query_cetf_components_code import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *
from mysql.getUpOrDownPrice import getUpPrice

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF赎回-------------
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s,  # etf赎回单位数
            'etf_unit_sell': %s,  # etf卖出单位数
            'component_unit_sell': %s # 成分股卖出单位数
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
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
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''


# 跨市场ETF赎回模板，模拟真实etf，T日不买入etf,重启环境
templet_cetf_str15 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from crossmarketetf.cetfmysql.query_cetf_components_code import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer
from utils.env_restart import clear_data_and_restart_all
from service.mainService import *
from mysql.getUpOrDownPrice import getUpPrice

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        # -----------ETF赎回-------------
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s,  # etf赎回单位数
            'etf_unit_sell': %s,  # etf卖出单位数
            'component_unit_sell': %s # 成分股卖出单位数
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
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
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''

# 跨市场ETF赎回模板，模拟真实etf，修改费率，重启环境
templet_cetf_str16 = '''#!/usr/bin/python
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

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        sql_transfer.update_cur_fee_rate(1, '%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        # -----------ETF赎回-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s   # etf赎回单位数
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,
                                pyname = '%s')
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

if __name__ == '__main__':
    unittest.main()
'''


# 跨市场ETF赎回模板，模拟真实etf，仅赎回
templet_cetf_str17 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF赎回-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s   # etf赎回单位数
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

if __name__ == '__main__':
    unittest.main()
'''

# 跨市场ETF赎回模板，模拟真实etf，赎回/申购/卖赎回的成分股
templet_cetf_str18 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *
from mysql.getUpOrDownPrice import getUpPrice

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF赎回-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s ,   # etf申赎单位数
            'component_unit_sell': %s # 成分股卖出单位数
        }

        # 查询ETF赎回前成分股持仓
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf申赎数量
        quantity = int(unit_info['etf_unit'] * unit_number)

        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # -----------ETF申购-------------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 查询ETF申购前成分股持仓
        component_stk_info2 =cetf_get_all_component_stk(Api,unit_info['ticker'])
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs2 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info2)
        etf_creation_log(case_goal, rs2)
        self.assertEqual(rs2['用例测试结果'], True)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
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
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''


# 跨市场ETF赎回模板，模拟真实etf，申购/赎回/卖申购的etf
templet_cetf_str19 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *
from mysql.getUpOrDownPrice import getUpPrice

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF申购-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit': %s ,   # etf申赎单位数
            'etf_unit_sell': %s,  # etf卖出单位数
        }

        # 查询ETF申购前成分股持仓
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf申赎数量
        quantity = int(unit_info['etf_unit'] * unit_number)

        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # -----------ETF赎回-------------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 查询ETF赎回前成分股持仓
        component_stk_info2 =cetf_get_all_component_stk(Api,unit_info['ticker'])
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs2 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info2)
        etf_creation_log(case_goal, rs2)
        self.assertEqual(rs2['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs3 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs3 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs3['用例测试结果'] is False:
                etf_sell_log(case_goal, rs3)
                self.assertEqual(rs3['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs3)


if __name__ == '__main__':
    unittest.main()
'''


# 跨市场ETF赎回模板，模拟真实etf，购买etf/赎回/申购/卖赎回的成分股
templet_cetf_str20 = '''#!/usr/bin/python
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

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF赎回-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit_buy': %s,  # etf买入单位数
            'etf_unit': %s ,   # etf申赎单位数
            'component_unit_sell': %s # 成分股卖出单位数
        }

        # -----------T日买入etf-------------
        cetf_add(Api,
                 Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                 unit_info['ticker'],
                 unit_info['etf_unit_buy'])

        # 查询ETF赎回前成分股持仓
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf申赎数量
        quantity = int(unit_info['etf_unit'] * unit_number)

        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # -----------ETF申购-------------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 查询ETF申购前成分股持仓
        component_stk_info2 =cetf_get_all_component_stk(Api,unit_info['ticker'])
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs2 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info2)
        etf_creation_log(case_goal, rs2)
        self.assertEqual(rs2['用例测试结果'], True)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
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
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''


# 跨市场ETF赎回模板，模拟真实etf，赎回/卖赎回的成分股
templet_cetf_str21 = '''#!/usr/bin/python
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

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF赎回-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit_buy': %s,  # etf买入单位数
            'etf_unit': %s ,   # etf申赎单位数
            'component_unit_sell': %s # 成分股卖出单位数
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
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # ------------二级市场卖出成份股-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
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
                        Api.const.XTP_BUSINESS_TYPE['%s'],
                    'order_client_id':
                        2,
                    'market':
                        Api.const.XTP_MARKET_TYPE['%s'],
                    'ticker':
                        stk_code,
                    'side':
                        Api.const.XTP_SIDE_TYPE['%s'],
                    'price_type':
                        Api.const.XTP_PRICE_TYPE['%s'],
                    'price':
                        limitup_px,
                    'quantity':
                        quantity,
                    'position_effect':
                        Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
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
'''


# 跨市场ETF赎回模板，模拟真实etf，T日买入etf，赎回
templet_cetf_str22 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *
from crossmarketetf.cetfservice.cetf_add import cetf_add

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF赎回-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit_buy': %s,  # etf买入单位数
            'etf_unit': %s   # etf赎回单位数
        }

        # -----------T日买入etf-------------
        cetf_add(Api,
                 Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                 unit_info['ticker'],
                 unit_info['etf_unit_buy'])
        time.sleep(1)

        # -----------查询ETF赎回前成分股持仓-------------
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf赎回数量
        quantity = int(unit_info['etf_unit'] * unit_number)

        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

if __name__ == '__main__':
    unittest.main()
'''


# 跨市场ETF赎回模板，模拟真实etf，T日买入etf，赎回,卖出etf
templet_cetf_str23 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfservice.cetf_main_service import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfservice.cetf_utils import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from service.mainService import *
from crossmarketetf.cetfservice.cetf_add import cetf_add

class %s(xtp_test_case):

    def test_%s(self):
        # -----------ETF赎回-------------
        title = ('%s')
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、全成、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %s,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        unit_info = {
            'ticker': '%s',  # etf代码
            'etf_unit_buy': %s,  # etf买入单位数
            'etf_unit': %s,   # etf赎回单位数
            'etf_unit_sell': %s,  # etf卖出单位数
        }

        # -----------T日买入etf-------------
        cetf_add(Api,
                 Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                 unit_info['ticker'],
                 unit_info['etf_unit_buy'])
        time.sleep(1)

        # -----------查询ETF赎回前成分股持仓-------------
        component_stk_info = cetf_get_all_component_stk(Api,unit_info['ticker'])

        # 查询etf最小申赎数量
        unit_number = query_creation_redem_unit(unit_info['ticker'])
        # etf赎回数量
        quantity = int(unit_info['etf_unit'] * unit_number)

        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':
                Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':
                2,
            'market':
                Api.const.XTP_MARKET_TYPE['%s'],
            'ticker':
                unit_info['ticker'],
            'side':
                Api.const.XTP_SIDE_TYPE['%s'],
            'price_type':
                Api.const.XTP_PRICE_TYPE['%s'],
            'quantity':
                quantity,
            'position_effect':
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        g_func.cetf_parm_init(case_goal['期望状态'])
        rs1 = cetf_service_test(Api, case_goal, wt_reqs,component_stk_info,)
        etf_creation_log(case_goal, rs1)
        self.assertEqual(rs1['用例测试结果'], True)

        # --------二级市场，卖出etf-----------
        case_goal['期望状态'] = '%s'
        case_goal['errorID'] = %s
        case_goal['errorMSG'] = %s
        # 二级市场卖出的etf数量
        quantity = int(unit_info['etf_unit_sell'] * unit_number)
        quantity_list = split_etf_quantity(quantity)
        # 查询涨停价
        limitup_px = getUpPrice(unit_info['ticker'])
        rs2 = {}
        for etf_quantity in quantity_list:
            wt_reqs_etf = {
                'business_type':
                    Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':
                    2,
                'market':
                    Api.const.XTP_MARKET_TYPE['%s'],
                'ticker':
                    unit_info['ticker'],
                'side':
                    Api.const.XTP_SIDE_TYPE['%s'],
                'price_type':
                    Api.const.XTP_PRICE_TYPE['%s'],
                'price':
                    limitup_px,
                'quantity':
                    etf_quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            rs2 = serviceTest(Api, case_goal, wt_reqs_etf)
            if rs2['用例测试结果'] is False:
                etf_sell_log(case_goal, rs2)
                self.assertEqual(rs2['用例测试结果'], True)
                return
        etf_sell_log(case_goal, rs2)
if __name__ == '__main__':
    unittest.main()
'''

