#!/usr/bin/python
# -*- encoding: utf-8 -*-

# 导入单元测试模块
from testcase import *



# 单元测试01
############################################################################
class TestCase01(XTPTestCase):

    # --------------------------------------------------
    def testSubscriptSync(self):
        """测试用例00 - 测试同步订阅行情"""
        req = {
            'exchange_id': 1,
            'ticker': '600300'
        }
        # 调用行情api的同步订阅命令
        ret = Api.quote.SubscribeSync(req)
        print '订阅行情(同步) : ', ret['ticker']['ticker']

    # --------------------------------------------------
    def testSubscript(self):
        """测试用例1 - 测试订阅行情"""

        # 定义一些计数器和变量
        var = Attribute({
            'wait': 2,
            'count': 0,
            'count_num': 1,
            'exchange': 1,
            'ticker': '600350'
        })

        # ----------------------------------------------
        def on_sub_market_data(data, error, last):
            """订阅回调"""

            # 对数据进行一些判断处理

            if data['ticker'] != var['ticker']:
                pass

            if error['error_id'] != 0:
                print "出现了错误: error_id=", error['error_id']

            if last:
                var.wait -= 1

        # -----------------------------------------------
        def on_market_data(data):
            """行情数据回调"""

            if data['bid1'] > data['last_price']*1.1:
                print "出现了错误: bid1超过涨停价"

            # 在全局变量里记录行情数据的总推送次数
            var.count += 1

            # 推送的行情次数达到指定次数后就不再测了
            if var.count >= var.count_num:
                var.wait -= 1

        # 设置订阅回调函数
        Api.quote.setSubMarketDataHandle(on_sub_market_data)
        # 设置行情数据回调函数
        Api.quote.setMarketDataHandle(on_market_data)

        req = {
            'exchange_id': var.exchange,
            'ticker': var.ticker
        }
        # 调用行情api的订阅命令
        ret = Api.quote.SubscribeMarketData(req)
        # 测试用例: ret 必须等于0
        self.assertEqual(ret, 0)

        # 等待所有数据处理完成
        while var.wait:
            sleep(0.1)

        # 测试用例: count 必须大于等于1
        self.assertGreaterEqual(var.count, 1)

    # -----------------------------------------------
    def testUnSubscript(self):
        """测试用例2 - 测试取消订阅行情"""

        var = Attribute({
            'exchange': enumDict["XTP_EXCHANGE_SH"],
            'ticker': '600350'
        })

        req = {
            'exchange_id': var.exchange,
            'ticker': var.ticker
        }
        ret = Api.quote.UnSubscribeMarketData(req)
        # 测试用例: ret 必须等于0
        self.assertEqual(ret, 0)

    # --------------------------------------------------
    def testInsertOrder(self):
        """测试用例3 - 测试订单"""

        var = Attribute({
            'wait': 1,
            'count': 0,
            'count_num': 1,
            'total_asset': 0,
            'ticker': '600350',
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']
        })

        # -----------------------------------------------
        def asset_event_01(data, error, request_id, is_last):
            """测试用例3的查询资金响应回调"""
            if request_id:
                pass

            if is_last:
                pass

            if error['error_id'] == 0:
                var.total_asset = data['buying_power']

            var.wait = False

        # 开始查询初始资金
        var.wait = True

        # 设置查询资金响应回调函数
        Api.trade.setQueryAssetHandle(asset_event_01)
        Api.trade.QueryAsset()

        # 等待所有数据处理完成
        while var.wait:
            sleep(0.1)

        # 查看总资金
        print '总资金(异步) : ', var.total_asset

        # -----------------------------------------------
        def order_event(order, error):
            """订测试用例3的委托响应回调"""
            print "订单响应: ", order, error

            var.wait -= 1

        # 开始委托
        var.wait = 1

        # 设置订单响应回调函数
        Api.trade.setOrderEventHandle(order_event)

        req = {
            'ticker': var['ticker'],
            'market': var['market'],
            'quantity': 200,
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_FORWARD_BEST'],
            'price_type': 1
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY']
        }
        xtp_order_id = Api.trade.InsertOrder(req)
        print '订单ID =', xtp_order_id

        # 订单ID必须大于0
        self.assertGreater(xtp_order_id, 0)

        req = {
            'ticker': var['ticker'],
            'begin_time': '',
            'end_time': ''
        }
        ret = Api.trade.QueryOrdersSync(req)
        print '订单查询(同步) : ', ret

        # # 等待所有数据处理完成
        # while var.wait:
        #     sleep(0.1)


############################################################################
if __name__ == '__main__':
    unittest.main()

while 1:
    sleep(0.1)
