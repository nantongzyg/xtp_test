#!/usr/bin/python
# -*- coding: UTF-8 -*-

from testcase import *

class Test1(XTPTestCase):

    def testMycase1(self):
        self.assertGreater(1, 0)


    def testMycase1(self):
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