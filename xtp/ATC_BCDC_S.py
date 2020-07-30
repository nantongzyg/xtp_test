#!/usr/bin/python
# -*- coding: UTF-8 -*-

from api.XTPTestCase import *


 
class ATC_BCDC_S(XTPTestCase):
    def testATC_301_02(self):
        pos = Api.trade.QueryPositionsSync()
        dump(pos.data)

        asset = Api.trade.QueryAssetSync()
        dump(asset.data)
        pass

if __name__ == '__main__':
    unittest.main()