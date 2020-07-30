#!/usr/bin/python
# -*- coding: UTF-8 -*-

from testcase import *


def on_order(data, error):
    print data
    # if 1==1:
    #     result['wait'] -= 1


def on_trade(data):
    # # print  data
    # req = {'ticker':''}
    # pos = Api.trade.QueryPositionSync(req)
    # rs = (pos.total_qty - pos_old.total_qty == 100) and (1)
    # rs = rs and (pos.total_qty - pos_old.total_qty == 100) and (1)
    # result['result'] = rs
    # if data['state'] == 'AC':
    #     result['wait'] -= 1
    pass

class Test2(XTPTestCase):

    def testTrade(self):
        result = {
            "wait": 2,
            "result": 0
        }

        var = {
            'ticker': '000002',
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
            'quantity': 100000,
            'price': 21.8,
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY']
        }

        req = {'ticker': ''}
        pos_old = Api.trade.QueryPositionSync(req)
        # print pos_old


        Api.trade.setOrderEventHandle(on_order)
        Api.trade.setTradeEventHandle(on_trade)

        xtp_id = Api.trade.InsertOrder(var)
        print xtp_id

        while result['wait']:
            sleep(1)

        self.assertEqual(result['result'], True)


    def testMycase1(self):
        data = Api.trade.QueryAssetSync()
        self.asset = data['asset']["buying_power"]
        self.assertGreater(-1, 0)


    def testMycase2(self):
        print Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'] == 1
        self.assertGreaterEqual(1, 0)

    def testQueryPos(self):
        req = {
            "ticker": ''
        }

        data = Api.trade.QueryPositionSync(req)
        print data['position'][0]['position']['ticker_name']
        self.assertGreaterEqual(1, 0)

if __name__ == '__main__':
    unittest.main()