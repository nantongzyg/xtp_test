#!/usr/bin/python
# -*- encoding: utf-8 -*-

from testcase import *
from requests import api


class TestCase02(XTPTestCase):
    #
    # --------------------------------------------------
    def testQueryAssetSync(self):
        """测试用例 - 测试"""

        # 调用行情api的同步订阅命令
        ret = Api.trade.QueryAssetSync()

        print '总资金 : ', ret

    # --------------------------------------------------
    def testQueryOrdersSync(self):
        """测试用例 - 测试"""

        req = {
            'ticker': '600350'
        }
        # 调用行情api的同步订阅命令
        ret = Api.trade.QueryOrdersSync(req)
        print '委托: ', ret

    # --------------------------------------------------
    def testQueryTradesSync(self):
        """测试用例 - 测试"""

        req = {
            'ticker': '600350'
        }
        # 调用行情api的同步订阅命令
        ret = Api.trade.QueryTradesSync(req)
        print '成交 : ', ret


    # --------------------------------------------------
    def testQueryTradesByXTPIDSync(self):
        """测试用例 - 测试"""

        xtp_id = 112154682453041
        # 调用行情api的同步订阅命令
        ret = Api.trade.QueryTradesByXTPIDSync(xtp_id)
        print '成交XTPID : ', ret

        sleep(2)


    # --------------------------------------------------
    def testQueryPosition(self):
        """测试用例 - 测试"""

        def pos_event(data, error, request_id, is_last):
            print "持仓回调:", data

        Api.trade.setQueryPositionHandle(pos_event)

        req = {
            'ticker': ''
        }
        # 调用交易api的查询持仓命令
        Api.trade.QueryPosition(req)


if __name__ == '__main__':
    unittest.main()
