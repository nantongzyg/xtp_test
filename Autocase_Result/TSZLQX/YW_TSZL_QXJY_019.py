#!/usr/bin/python
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
from  UpdateTszlqx import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from QueryOrderErrorMsg import queryOrderErrorMsg

class YW_TSZL_QXJY_019(xtp_test_case):
    # YW_TSZL_QXJY_019
    def test_YW_TSZL_QXJY_019(self):
        title = 'OMS初始化—可选权限—Secuinfo表，深A证券账号无卖入退市整理期股票权限'
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        updateSecuRightHasNoMSz()
        updateSecuRightHasMSh()
        clear_data_and_restart_all()
        Api.trade.Logout()
        Api.trade.Login()

        case_goal = {
            '期望状态': '废单',
            'errorID': 11000563,
            'errorMSG': queryOrderErrorMsg(11000563),
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            
            
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        stkparm = QueryStkPriceQty('060001', '2', '0', '10', '0', 'S', case_goal['期望状态'], Api)
        # 如果下单参数获取失败，则用例失败
        if stkparm['返回结果'] is False:
            rs = {
                '用例测试结果': stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + stkparm['错误原因'],
            }
            self.assertEqual(rs['用例测试结果'], True)
        else:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                'order_client_id':2,
                'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker': stkparm['证券代码'],
                'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                'price': stkparm['涨停价'],
                'quantity': 200,
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            ParmIni(Api, case_goal['期望状态'], wt_reqs['price_type'])
            CaseParmInsertMysql(case_goal, wt_reqs)
            rs = serviceTest(Api, case_goal, wt_reqs)
            logger.warning('执行结果为' + str(rs['用例测试结果']) + ','
                           + str(rs['用例错误源']) + ',' + str(rs['用例错误原因']))
            self.assertEqual(rs['用例测试结果'], True) # 415 

if __name__ == '__main__':
    unittest.main()
        