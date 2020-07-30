#!/usr/bin/python
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

class YW_GGQQ_YWFSJHA_GU_124(xtp_test_case):
    # YW_GGQQ_YWFSJHA_GU_124

    def test_YW_GGQQ_YWFSJHA_GU_124(self):
        title='卖开（义务方开仓）：市价剩余撤销-不存在的证券代码'
        #定义当前测试用例的期待值
        #期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        #xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': '废单',
            'errorID': 11000010,
            'errorMSG': queryOrderErrorMsg(11000010),
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        logger.warning(title)
        # 定义委托参数信息------------------------------------------
        wt_reqs = {
            'business_type':Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_OPTION'],
            'order_client_id':1,
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
            'ticker': '10009999',
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL'],
            'position_effect':Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_OPEN'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST_OR_CANCEL'],
            'price': 1.0000,
            'quantity': 2
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
        self.assertEqual(rs['用例测试结果'], True) # 2

if __name__ == '__main__':
    unittest.main()
        