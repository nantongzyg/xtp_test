#!/usr/bin/python
# -*- encoding: utf-8 -*-
import random
import sys
import time
from multiprocessing import Pool

from quoteServiceUnsubOpt import *

sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from config import *


class UNSUB_ALL_MARKET_DATA(xtp_test_case):
    def test_UNSUB_ALL_TICK_BY_TICK(self):
        pool_count = 1
        p = Pool(pool_count)
        for i in range(pool_count):
            p.apply_async(sub_market, args=(i,))
        p.close()
        p.join()

def sub_market(name):
    client_id = 52
    Api = XTPQuoteApi(client_id)
    Api.Login()
    stk_info = {
        # 'ticker': 'shopt*',
        'exchange_id': {}  # 沪A
    }
    unSubAllMarketData(Api, stk_info)
    Api.Logout()

if __name__=='__main__':
    unittest.main()
