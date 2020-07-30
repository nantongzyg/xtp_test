#!/usr/bin/python
# -*- encoding: utf-8 -*-

'''
模板类型说明：
templet_case_str1：买卖case正常测试模板
templet_case_str2：买卖case模板,清深圳接口库，改数据库，重启环境
templet_case_str3：分级基金申购模板,正常情况
templet_case_str4：分级基金申购模板,清深圳接口库，改数据库，重启环境
templet_case_str5：分级基金申赎，修改oms申赎费用配置，重启深圳环境
templet_case_str6：分级基金申赎，错误的证券代码
templet_case_str7：分级基金申购模板,清上海接口库，改数据库，重启环境
templet_case_str8：买卖模板，错误的证券代码
templet_case_str9：分级基金拆分合并模板，正常情况
templet_case_str10：分级基金拆分合并模板，修改资金，重启oms
templet_case_str11：分级基金拆分合并模板，错误的代码
templet_case_str12：新股申购模板，正常情况
templet_case_str13：买卖case模板,清上海接口库，改数据库，重启环境
templet_case_str14：配股模板,正常情况
templet_case_str15：配股模板,清深圳接口库该资金重启环境
templet_case_str16：配股模板,清上海接口库该资金重启环境
templet_case_str17：买卖case模板,清深圳和上海接口库，重启环境
templet_case_str18：配股模板,清深圳和上海接口库,重启环境
templet_case_str19：新股申购模板,清深圳和上海接口库,重启环境
templet_case_str20：买卖业务，修改风控，重启oms
templet_case_str21：分级基金拆分合并模板，清深圳接口库，重启环境
templet_case_str22:期权买卖case正常测试模板
templet_case_str23:期权买卖,错误的证券代码
templet_case_str24:期权买卖,清上海接口库，改数据库，重启环境
templet_case_str25:期权买卖,清深圳和上海接口库，重启环境
templet_case_str26:行情基本信息
templet_case_str27:行情订单薄
templet_case_str28:行情逐笔订单
templet_case_str29:行情基本信息退订
templet_case_str30:行情订单薄退订
templet_case_str31:行情逐笔订单退订
templet_case_str37:货币基金买卖case正常测试模板
templet_case_str38:货币基金买卖模板，错误的证券代码
templet_case_str39:买卖case模板,清上海接口库，改数据库，重启环境
templet_case_str40:货币基金买卖case模板,清深圳和上海接口库，重启环境
templet_case_str41:担保品买卖case模板,清深圳和上海接口库，重启环境
templet_case_str42:担保品买卖模板，错误的证券代码
templet_case_str43:担保品买卖case正常测试模板
templet_case_str44:担保品买卖case模板,清上海接口库，改数据库，重启环境
templet_case_str45:融资买入case模板,清深圳和上海接口库，重启环境
templet_case_str46:融资买入模板，错误的证券代码
templet_case_str47:融资买入case正常测试模板
templet_case_str48:融资买入case模板,清上海接口库，改数据库，重启环境
templet_case_str49:融券卖出case模板,清深圳和上海接口库，重启环境
templet_case_str50:融券卖出模板，错误的证券代码
templet_case_str51:融券卖出case正常测试模板
templet_case_str52:融券卖出case模板,清上海接口库，改数据库，重启环境
templet_case_str53:融券卖出case模板,清深圳接口库，改数据库，重启环境
templet_case_str54:卖券还款case模板,清深圳和上海接口库，重启环境
templet_case_str55:卖券还款模板，错误的证券代码
templet_case_str56:卖券还款case正常测试模板
templet_case_str57:卖券还款case模板,清上海接口库，改数据库，重启环境
templet_case_str58:卖券还款case模板,清深圳接口库，改数据库，重启环境
templet_case_str59:卖券还款case模板,清上海接口库，改数据库，改合约负债，重启环境
templet_case_str60:卖券还款case模板,清深圳接口库，改数据库，改合约负债，重启环境
'''
# 买卖case正常测试模板
templet_case_str1='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from mainService import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动

        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''


# 买卖case模板,清深圳接口库，改数据库，重启环境
templet_case_str2='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from mainService import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg


class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 分级基金申购模板,正常情况(无重启环境)
templet_case_str3='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceCreationRedemption")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStructuredFundInfo('%s','%s','%s','%s','%s','%s',case_goal['期望状态'],Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'quantity': %d
            }
            ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 分级基金申购模板,清深圳接口库，改数据库，重启环境
templet_case_str4='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceCreationRedemption")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStructuredFundInfo('%s','%s','%s','%s','%s','%s',case_goal['期望状态'],Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'quantity': %d
            }
            ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 分级基金申赎，修改oms申赎费用配置，重启深圳环境
templet_case_str5='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceCreationRedemption")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    py_name = '%s'

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.update_cur_fee_rate(2, self.py_name)
        sz_restart()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStructuredFundInfo('%s','%s','%s','%s','%s','%s',case_goal['期望状态'],Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'quantity': %d
            }
            ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs, self.py_name)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 分级基金申赎，错误的证券代码
templet_case_str6='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceCreationRedemption")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'quantity': %d
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 分级基金申购模板,清上海接口库，改数据库，重启环境
templet_case_str7='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceCreationRedemption")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStructuredFundInfo('%s','%s','%s','%s','%s','%s',case_goal['期望状态'],Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'quantity': %d
            }
            ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买卖模板，错误的证券代码
templet_case_str8='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from mainService import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'price': %s,
            'quantity': %d
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 分级基金拆分合并模板，正常情况
templet_case_str9 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceSplitMerge")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStructuredFundInfo('%s','%s','%s','%s','%s','%s',case_goal['期望状态'],Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'quantity': %d
            }
            ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 分级基金拆分合并模板，修改资金，重启oms
templet_case_str10 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceSplitMerge")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import oms_restart
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        oms_restart()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStructuredFundInfo('%s','%s','%s','%s','%s','%s',case_goal['期望状态'],Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'quantity': %d
            }
            ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 分级基金拆分合并模板，错误的代码
templet_case_str11 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceSplitMerge")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import oms_restart
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'quantity': %d
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 新股申购模板
templet_case_str12 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from mainService import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            '是否是新股申购': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'quantity': %d
        }
        ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买卖case模板,清上海接口库，改数据库，重启环境
templet_case_str13='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from mainService import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 配股模板,正常情况
templet_case_str14 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from mainService import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'quantity': %d
        }
        ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 配股模板,清深圳接口库该资金重启环境
templet_case_str15 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from mainService import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'quantity': %d
        }
        ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 配股模板,清上海接口库该资金重启环境
templet_case_str16 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from mainService import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'quantity': %d
        }
        ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买卖case模板,清深圳和上海接口库，重启环境
templet_case_str17='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from mainService import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 配股模板,清深圳和上海接口库,重启环境
templet_case_str18 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from mainService import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'quantity': %d
        }
        ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 新股申购模板,清深圳和上海接口库,重启环境
templet_case_str19 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from mainService import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            '是否是新股申购': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'quantity': %d
        }
        ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买卖业务，修改风控，重启oms
templet_case_str20='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from mainService import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.delete_cur_risk()
        sql_transfer.insert_cur_risk('%s')
        oms_restart()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 分级基金申购模板,改资金，改费用配置，重启环境
templet_case_str21='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceCreationRedemption")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    py_name = '%s'

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset(self.py_name)
        sql_transfer.update_cur_fee_rate(2, self.py_name)
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStructuredFundInfo('%s','%s','%s','%s','%s','%s',case_goal['期望状态'],Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'quantity': %d
            }
            ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 分级基金拆分合并模板，清深圳接口库，重启环境
templet_case_str21 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/creationRedemption")
from mainService import *
from QueryStructuredFundInfo import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def setUp(self):
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStructuredFundInfo('%s','%s','%s','%s','%s','%s',case_goal['期望状态'],Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'quantity': %d
            }
            ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''


# 期权买卖case正常测试模板
templet_case_str22 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/option/service")
from OptMainService import *
from OptQueryStkPriceQty import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from CaseParmInsertMysql import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果':stkparm['返回结果'],
                '测试错误原因':'获取下单参数失败,'+stkparm['错误原因'],
            }
            logger.error('查询结果为False,错误原因: {0}'.format(
                        json.dumps(rs['测试错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True)

        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect':Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''


# 期权买卖，错误的证券代码
templet_case_str23 = '''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/option/service")
from OptMainService import *
from OptQueryStkPriceQty import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from CaseParmInsertMysql import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s

    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'position_effect':Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'price': %s,
            'quantity': %d
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        CaseParmInsertMysql(case_goal, wt_reqs)
        rs = serviceTest(Api, case_goal, wt_reqs)
        if rs['用例测试结果']:
            logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
        else:
            logger.warning('执行结果为{0},{1},{2}'.format(
                          str(rs['用例测试结果']), str(rs['用例错误源']),
                          json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''


# 期权买卖,清上海接口库，改数据库，重启环境
templet_case_str24='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/option/service")
from OptMainService import *
from OptQueryStkPriceQty import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
from CaseParmInsertMysql import *
sys.path.append("/home/yhl2/workspace/xtp_test/option/mysql")
from Opt_SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from QueryOrderErrorMsg import queryOrderErrorMsg
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *


reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = Opt_SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '%s',
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            logger.error('查询结果为False,错误原因: {0}'.format(
                        json.dumps(rs['测试错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect':Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''


# 买卖case模板,清深圳和上海接口库，重启环境
templet_case_str25='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from mainService import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

templet_case_str26='''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def subMarketData(self, Api, stk_info, case_name, rs_expect):
        print Api.GetApiVersion()
        def on_market_data(data, error, last):
            self.print_msg(case_name, rs_expect, error)

        Api.setSubMarketDataHandle(on_market_data)
        Api.SubscribeMarketData(stk_info)
        time.sleep(1)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('{0}测试正确！'.format(case_name))
        else:
            logger.error('{0}测试错误!'.format(case_name))
        self.assertEqual(error, rs_expect)

    def test_%s(self):
        pyname = '%s'
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '%s', 'exchange_id': %s}
        self.subMarketData(Api, stk_info, pyname,
                                    {'error_id': %s, 'error_msg': '%s'}) # %d
        Api.Logout()

if __name__=='__main__':
    unittest.main()
'''

templet_case_str27='''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def subOrderBook(self, Api, stk_info, case_name, rs_expect):
        print Api.GetApiVersion()
        def on_order_book(data, error, last):
            self.print_msg(case_name, rs_expect, error)

        Api.setSubOrderBookHandle(on_order_book)
        Api.SubscribeOrderBook(stk_info)
        time.sleep(1)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('{0}测试正确！'.format(case_name))
        else:
            logger.error('{0}测试错误!'.format(case_name))
        self.assertEqual(error, rs_expect)

    def test_%s(self):
        pyname = '%s'
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '%s', 'exchange_id': %s}
        self.subOrderBook(Api, stk_info, pyname,
                                    {'error_id': %s, 'error_msg': '%s'}) # %d
        Api.Logout()

if __name__=='__main__':
    unittest.main()
'''

templet_case_str28='''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def subTickByTick(self, Api, stk_info, case_name, rs_expect):
        print Api.GetApiVersion()
        def on_all_tick_by_tick(data, error, is_last):
            self.print_msg(case_name, rs_expect, error)

        Api.setSubTickByTickHandle(on_all_tick_by_tick)
        Api.SubscribeTickByTick(stk_info)
        time.sleep(1)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('{0}测试正确！'.format(case_name))
        else:
            logger.error('{0}测试错误!'.format(case_name))
        self.assertEqual(error, rs_expect)

    def test_%s(self):
        pyname = '%s'
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '%s', 'exchange_id': %s}
        self.subTickByTick(Api, stk_info, pyname,
                                    {'error_id': %s, 'error_msg': '%s'}) # %d
        Api.Logout()

if __name__=='__main__':
    unittest.main()
'''

templet_case_str29='''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def subMarketData(self, Api, stk_info, case_name, rs_expect):
        print Api.GetApiVersion()
        def on_market_data(data, error, last):
            pass

        def on_unsub_market_data(data, error, last):
            self.print_msg(case_name, rs_expect, error)

        Api.setSubMarketDataHandle(on_market_data)
        Api.setUnSubMarketDataHandle(on_unsub_market_data)
        Api.SubscribeMarketData(stk_info)
        Api.UnSubscribeMarketData(stk_info)
        time.sleep(1)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('{0}测试正确！'.format(case_name))
        else:
            logger.error('{0}测试错误!'.format(case_name))
        self.assertEqual(error, rs_expect)

    def test_%s(self):
        pyname = '%s'
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '%s', 'exchange_id': %s}
        self.subMarketData(Api, stk_info, pyname,
                                    {'error_id': %s, 'error_msg': '%s'}) # %d
        Api.Logout()

if __name__=='__main__':
    unittest.main()
'''

templet_case_str30='''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def subOrderBook(self, Api, stk_info, case_name, rs_expect):
        print Api.GetApiVersion()
        def on_order_book(data, error, last):
            self.print_msg(case_name, rs_expect, error)

        Api.setSubOrderBookHandle(on_order_book)
        Api.SubscribeOrderBook(stk_info)
        time.sleep(1)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('{0}测试正确！'.format(case_name))
        else:
            logger.error('{0}测试错误!'.format(case_name))
        self.assertEqual(error, rs_expect)

    def test_%s(self):
        pyname = '%s'
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '%s', 'exchange_id': %s}
        self.subOrderBook(Api, stk_info, pyname,
                                    {'error_id': %s, 'error_msg': '%s'}) # %d
        Api.Logout()

if __name__=='__main__':
    unittest.main()
'''

templet_case_str31='''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def subTickByTick(self, Api, stk_info, case_name, rs_expect):
        print Api.GetApiVersion()
        def on_all_tick_by_tick(data, error, is_last):
            pass

        def on_unsub_tick_by_tick(data, error, is_last):
            self.print_msg(case_name, rs_expect, error)

        Api.setSubTickByTickHandle(on_all_tick_by_tick)
        Api.setUnSubscribeTickByTickHandle(on_unsub_tick_by_tick)
        Api.SubscribeTickByTick(stk_info)
        Api.UnSubscribeTickByTick(stk_info)
        time.sleep(1)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('{0}测试正确！'.format(case_name))
        else:
            logger.error('{0}测试错误!'.format(case_name))
        self.assertEqual(error, rs_expect)

    def test_%s(self):
        pyname = '%s'
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '%s', 'exchange_id': %s}
        self.subTickByTick(Api, stk_info, pyname,
                                    {'error_id': %s, 'error_msg': '%s'}) # %d
        Api.Logout()

if __name__=='__main__':
    unittest.main()
'''

# 买卖case正常测试模板,多pbu
templet_case_str32='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from config import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from mainService import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg


config_trade = {
            'client_id': CONST_TRADE_CLIENT_ID,
            'save_file_path': CONST_TRADE_SAVE_FILE_PATH,
            'ip': CONST_TRADE_IP,
            'port': CONST_TRADE_PORT,
            'user': '%s',
            'password': CONST_TRADE_PASSWORD,
            'sock_type': CONST_TRADE_SOCK_TYPE,
            'auto_login': CONST_TRADE_AUTO_LOGIN,
            'key': CONST_TRADE_KEY
        }

class tradeApi(object):
    const = XTPConst()

    trade = XTPTradeApi(config_trade)

class %s(xtp_test_case):

    def setUp(self):
        tradeApi.trade.Login()

    # %s
    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], tradeApi)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': tradeApi.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': tradeApi.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': tradeApi.const.XTP_SIDE_TYPE['%s'],
                'price_type': tradeApi.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(tradeApi, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(tradeApi, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买卖模板，错误的证券代码，多pbu
templet_case_str33='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from config import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from mainService import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg


config_trade = {
            'client_id': CONST_TRADE_CLIENT_ID,
            'save_file_path': CONST_TRADE_SAVE_FILE_PATH,
            'ip': CONST_TRADE_IP,
            'port': CONST_TRADE_PORT,
            'user': '%s',
            'password': CONST_TRADE_PASSWORD,
            'sock_type': CONST_TRADE_SOCK_TYPE,
            'auto_login': CONST_TRADE_AUTO_LOGIN,
            'key': CONST_TRADE_KEY
        }

class tradeApi(object):
    const = XTPConst()

    trade = XTPTradeApi(config_trade)

class %s(xtp_test_case):

    def setUp(self):
        tradeApi.trade.Login()

    # %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':tradeApi.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': tradeApi.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': tradeApi.const.XTP_SIDE_TYPE['%s'],
            'price_type': tradeApi.const.XTP_PRICE_TYPE['%s'],
            'price': %s,
            'quantity': %d
        }
        ParmIni(tradeApi,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(tradeApi, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买卖case模板,清深圳接口库，改数据库，重启环境，多pbu
templet_case_str34='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from config import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from mainService import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
from SqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg


config_trade = {
            'client_id': CONST_TRADE_CLIENT_ID,
            'save_file_path': CONST_TRADE_SAVE_FILE_PATH,
            'ip': CONST_TRADE_IP,
            'port': CONST_TRADE_PORT,
            'user': '%s',
            'password': CONST_TRADE_PASSWORD,
            'sock_type': CONST_TRADE_SOCK_TYPE,
            'auto_login': CONST_TRADE_AUTO_LOGIN,
            'key': CONST_TRADE_KEY
        }

class tradeApi(object):
    const = XTPConst()

    trade = XTPTradeApi(config_trade)

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_sz()
        tradeApi.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], tradeApi)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': tradeApi.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': tradeApi.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': tradeApi.const.XTP_SIDE_TYPE['%s'],
                'price_type': tradeApi.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(tradeApi, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(tradeApi, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买卖case模板,清深圳和上海接口库，重启环境,多pbu
templet_case_str35='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from config import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from mainService import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg


config_trade = {
            'client_id': CONST_TRADE_CLIENT_ID,
            'save_file_path': CONST_TRADE_SAVE_FILE_PATH,
            'ip': CONST_TRADE_IP,
            'port': CONST_TRADE_PORT,
            'user': 'testshopt09tgt',
            'password': CONST_TRADE_PASSWORD,
            'sock_type': CONST_TRADE_SOCK_TYPE,
            'auto_login': CONST_TRADE_AUTO_LOGIN,
            'key': CONST_TRADE_KEY
        }

class tradeApi(object):
    const = XTPConst()

    trade = XTPTradeApi(config_trade)

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_all()
        tradeApi.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], tradeApi)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': tradeApi.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': tradeApi.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': tradeApi.const.XTP_SIDE_TYPE['%s'],
                'price_type': tradeApi.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(tradeApi, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(tradeApi, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

#
templet_case_str36='''#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def queryTickersPriceInfo(self, Api, stk_info, case_name, rs_expect):
        print Api.GetApiVersion()
        def on_querytickerspriceinfo(data, error, last):
            self.print_msg(case_name, rs_expect, error)

        Api.setQueryTickersPriceInfoHandle(on_querytickerspriceinfo)
        Api.QueryTickersPriceInfo(stk_info)
        time.sleep(3)

    def print_msg(self, case_name, rs_expect, error):
        if rs_expect == error:
            logger.warning('{0}测试正确！'.format(case_name))
        else:
            logger.error('{0}测试错误!'.format(case_name))
        self.assertEqual(error, rs_expect)

    def test_%s(self):
        pyname = '%s'
        client_id = 6
        Api = XTPQuoteApi(client_id)
        Api.Login()
        stk_info = {'ticker': '%s', 'exchange_id': %s}
        self.queryTickersPriceInfo(Api, stk_info, pyname, {'error_id': %s, 'error_msg': '%s'}) # %d
        Api.Logout()

if __name__=='__main__':
    unittest.main()
'''


# 货币基金买卖case正常测试模板
templet_case_str37='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundservice")
from mfmainService import *
from mfQueryStkPriceQty import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql")
from mfCaseParmInsertMysql import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动

        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 货币基金买卖模板，错误的证券代码
templet_case_str38='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundservice")
from mfmainService import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql")
from mfSqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'price': %s,
            'quantity': %d
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 货币基金买卖case模板,清上海接口库，改数据库，重启环境
templet_case_str39='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundservice")
from mfmainService import *
from mfQueryStkPriceQty import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql")
from mfCaseParmInsertMysql import *
from mfSqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg


class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 货币基金买卖case模板,清深圳和上海接口库，重启环境
templet_case_str40='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundservice")
from mfmainService import *
from mfQueryStkPriceQty import *
from mfSqlData_Transfer import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql")
from mfCaseParmInsertMysql import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_fund_asset('%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''        

# 担保品买卖case模板,清深圳和上海接口库，重启环境
templet_case_str41='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from collateral.service.mainService import ParmIni, serviceTest
from collateral.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from collateral.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_all
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.delete_credit_debts()
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 担保品买卖模板，错误的证券代码
templet_case_str42='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from collateral.service.mainService import ParmIni, serviceTest
from collateral.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from collateral.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'price': %s,
            'quantity': %d
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        logger.warning('执行结果为' + str(rs['用例测试结果']) + ',' + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''        

# 担保品买卖case正常测试模板
templet_case_str43='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from collateral.service.mainService import ParmIni, serviceTest
from collateral.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from collateral.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动

        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 担保品买卖case模板,清上海接口库，改数据库，重启环境
templet_case_str44='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from collateral.service.mainService import ParmIni, serviceTest
from collateral.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from collateral.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融资买入case模板,清深圳和上海接口库，重启环境
templet_case_str45='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from financing.service.mainService import ParmIni, serviceTest
from financing.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from financing.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_all
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.keep_stk_asset()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.transfer_credit_cash_fund_asset("%s")
        sql_transfer.transfer_credit_debts('%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融资买入模板，错误的证券代码
templet_case_str46='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from financing.service.mainService import ParmIni, serviceTest
from financing.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from financing.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s %s %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'price': %s,
            'quantity': %d
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        if rs['用例测试结果']:
            logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
        else:
            logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''        

# 融资买入case正常测试模板
templet_case_str47='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from financing.service.mainService import ParmIni, serviceTest
from financing.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from financing.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s %s %s
    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动

        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融资买入case模板,清上海接口库，改数据库，重启环境
templet_case_str48='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from financing.service.mainService import ParmIni, serviceTest
from financing.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from financing.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''
# 融券卖出case模板,清深圳和上海接口库，重启环境
templet_case_str49='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from shortselling.service.mainService import ParmIni, serviceTest
from shortselling.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from shortselling.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_all
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.transfer_credit_debts('%s')
        sql_transfer.keep_stk_asset()
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融券卖出模板，错误的证券代码
templet_case_str50='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from shortselling.service.mainService import ParmIni, serviceTest
from shortselling.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from shortselling.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'price': %s,
            'quantity': %d
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        if rs['用例测试结果']:
            logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
        else:
            logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''        

# 融券卖出case正常测试模板
templet_case_str51='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from shortselling.service.mainService import ParmIni, serviceTest
from shortselling.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from shortselling.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s
    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动

        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融券卖出case模板,清上海接口库，改数据库，重启环境
templet_case_str52='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from shortselling.service.mainService import ParmIni, serviceTest
from shortselling.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from shortselling.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融券卖出case模板,清深圳接口库，改数据库，重启环境
templet_case_str53='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from shortselling.service.mainService import ParmIni, serviceTest
from shortselling.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from shortselling.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 卖券还款case模板,清深圳和上海接口库，重启环境
templet_case_str54='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_all
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.keep_stk_asset()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.transfer_credit_debts('%s')
        sql_transfer.transfer_credit_cash_fund_asset("%s")
        sql_transfer.delete_debts_data()
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 卖券还款模板，错误的证券代码
templet_case_str55='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'price': %s,
            'quantity': %d
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        if rs['用例测试结果']:
            logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
        else:
            logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''        

# 卖券还款case正常测试模板
templet_case_str56='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s %s
    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动

        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 卖券还款case模板,清上海接口库，改数据库，重启环境
templet_case_str57='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.delete_debts_data()
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 卖券还款case模板,清深圳接口库，改数据库，重启环境
templet_case_str58='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.delete_debts_data()
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 卖券还款case模板,清上海接口库，改数据库，改合约负债，重启环境
templet_case_str59='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.transfer_credit_debts('%s')
        sql_transfer.delete_debts_data()
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 卖券还款case模板,清深圳接口库，改数据库，改合约负债，重启环境
templet_case_str60='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.transfer_credit_debts('%s')
        sql_transfer.delete_debts_data()
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 卖券还款case模板,清上海接口库，改数据库，改合约负债，改融资头寸，重启环境
templet_case_str61='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s 
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_debts('%s')
        sql_transfer.transfer_credit_cash_fund_asset('%s')
        sql_transfer.delete_debts_data()
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 卖券还款case模板,清深圳接口库，改数据库，改合约负债，重启环境
templet_case_str62='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s 
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_debts('%s')
        sql_transfer.transfer_credit_cash_fund_asset('%s')
        sql_transfer.delete_debts_data()
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 卖券还款case模板,清上海接口库，改合约负债，重启环境
templet_case_str63='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s 
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_debts('%s')
        sql_transfer.delete_debts_data()
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 卖券还款case模板,清深圳接口库，改合约负债，重启环境
templet_case_str64='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s 
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_debts('%s')
        sql_transfer.delete_debts_data()
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
             '''

# 卖券还款case模板,清上海接口库，重启环境
templet_case_str65='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.delete_debts_data()
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
             '''

# 卖券还款case模板,清深圳接口库, 重启环境
templet_case_str66='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from salevoucher.service.mainService import ParmIni, serviceTest
from salevoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from salevoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        clear_data_and_restart_sz()
        sql_transfer.delete_debts_data()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
             '''

# 买券还券case模板,清深圳和上海接口库，重启环境
templet_case_str67='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from buyvoucher.service.mainService import ParmIni, serviceTest
from buyvoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from buyvoucher.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_all
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.transfer_credit_debts('%s')
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买券还券模板，错误的证券代码
templet_case_str68='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from buyvoucher.service.mainService import ParmIni, serviceTest
from buyvoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from buyvoucher.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s
    def test_%s(self):
        title='%s'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['%s'],
            'order_client_id':%s,
            'market': Api.const.XTP_MARKET_TYPE['%s'],
            'ticker': '%s',
            'side': Api.const.XTP_SIDE_TYPE['%s'],
            'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
            'price_type': Api.const.XTP_PRICE_TYPE['%s'],
            'price': %s,
            'quantity': %d
        }
        ParmIni(Api,case_goal['期望状态'],wt_reqs['price_type'])
        rs = serviceTest(Api, case_goal, wt_reqs)
        if rs['用例测试结果']:
            logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
        else:
            logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
        self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''        

# 买券还券case正常测试模板
templet_case_str69='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from buyvoucher.service.mainService import ParmIni, serviceTest
from buyvoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from buyvoucher.service.CaseParmInsertMysql import *
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s
    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动

        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买券还券case模板,清上海接口库，改数据库，重启环境
templet_case_str70='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from buyvoucher.service.mainService import ParmIni, serviceTest
from buyvoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from buyvoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买券还券case模板,清深圳接口库，改数据库，重启环境
templet_case_str71='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from buyvoucher.service.mainService import ParmIni, serviceTest
from buyvoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from buyvoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买券还券case模板,清上海接口库，改合约负债，重启环境
templet_case_str72='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from buyvoucher.service.mainService import ParmIni, serviceTest
from buyvoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from buyvoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_debts('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 买券还券case模板,清深圳接口库，改合约负债，重启环境
templet_case_str73='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from buyvoucher.service.mainService import ParmIni, serviceTest
from buyvoucher.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from buyvoucher.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_debts('%s')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 担保品买卖case模板,清深圳接口库，改数据库，重启环境
templet_case_str74='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from collateral.service.mainService import ParmIni, serviceTest
from collateral.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from collateral.service.CaseParmInsertMysql import *
from utils.env_restart import SqlData_Transfer, clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):

    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融资买入case模板,改两融额度和融资头寸，清上海数据并重启环境
templet_case_str75='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from financing.service.mainService import ParmIni, serviceTest
from financing.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from financing.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.transfer_credit_cash_fund_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融资买入case模板,改两融额度和融资头寸，清深圳数据并重启环境
templet_case_str76='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from financing.service.mainService import ParmIni, serviceTest
from financing.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from financing.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.transfer_credit_cash_fund_asset('%s')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融资买入case模板,清深圳接口库，改持仓，改资金, 重启环境
templet_case_str77='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from financing.service.mainService import ParmIni, serviceTest
from financing.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from financing.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.delete_stk_asset()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.transfer_credit_cash_fund_asset('%s')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融资买入case模板,清上海接口库，改持仓，改资金, 重启环境
templet_case_str78='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from financing.service.mainService import ParmIni, serviceTest
from financing.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from financing.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.delete_stk_asset()
        sql_transfer.transfer_credit_asset('%s')
        sql_transfer.transfer_credit_cash_fund_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融券卖出case模板,清深圳接口库，改持仓，改资金，重启环境
templet_case_str79='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from shortselling.service.mainService import ParmIni, serviceTest
from shortselling.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from shortselling.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_sz
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.delete_stk_asset()
        sql_transfer.transfer_credit_asset('%s')
        clear_data_and_restart_sz()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''

# 融券卖出case模板,清深圳接口库，改持仓，改资金，重启环境
templet_case_str80='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import json
sys.path.append("/home/yhl2/workspace/xtp_test")
from xtp.api.xtp_test_case import xtp_test_case, Api, unittest
from service.ServiceConfig import *
from shortselling.service.mainService import ParmIni, serviceTest
from shortselling.service.QueryStkPriceQty import QueryStkPriceQty
from service.log import *
from shortselling.service.CaseParmInsertMysql import *
from utils.env_restart import clear_data_and_restart_sh
from mysql.QueryOrderErrorMsg import queryOrderErrorMsg
from mysql.SqlData_Transfer import SqlData_Transfer

reload(sys)
sys.setdefaultencoding('utf-8')

class %s(xtp_test_case):
    # %s
    def setUp(self):
        sql_transfer = SqlData_Transfer()
        sql_transfer.delete_stk_asset()
        sql_transfer.transfer_credit_asset('%s')
        clear_data_and_restart_sh()
        Api.trade.Logout()
        Api.trade.Login()

    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': %s,
            'errorID': %d,
            'errorMSG': %s,
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            if rs['用例测试结果']:
                logger.warning('执行结果为{0}'.format(str(rs['用例测试结果'])))
            else:
                logger.warning('执行结果为{0},{1},{2}'.format(
                              str(rs['用例测试结果']), str(rs['用例错误源']),
                              json.dumps(rs['用例错误原因'], encoding='UTF-8', ensure_ascii=False)))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''


templet_case_str81='''#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from xtpapi import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ARmainservice import *
from ServiceConfig import *
from mainService import *
from QueryStkPriceQty import *
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class %s(xtp_test_case):
    # %s
    def test_%s(self):
        title = '%s'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动

        case_goal = {
            '期望状态': '%s',
            '是否生成报单': '%s',
            '是否是撤废': '%s',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            %s
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('%s', '%s', '%s', '%s', '%s', '%s', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['%s'],
                'order_client_id':%s,
                'market': Api.const.XTP_MARKET_TYPE['%s'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['%s'],
                'price_type': Api.const.XTP_PRICE_TYPE['%s'],
                'price': %s,
                'quantity': %d
            }
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # %d

if __name__ == '__main__':
    unittest.main()
        '''
