#!/usr/bin/python
# -*- encoding: utf-8 -*-
import random
import sys
import time
from multiprocessing import Pool

from quoteServiceOpt import *

sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from config import *


class SUB_ALL_OPT_MARKET_DATA(xtp_test_case):
    def test_SUB_ALL_OPT_MARKET_DATA(self):
        pool_count = 1
        p = Pool(pool_count)
        for i in range(pool_count):
            p.apply_async(sub_market, args=(i,))
        p.close()
        p.join()

def sub_market(name):
    client_id_key = 'id' + str(name + 1)
    client_id = 63
    Api = XTPQuoteApi(client_id)
    Api.Login()
    stk_info = {
        #'ticker': '',  # 全部行情
        'exchange_id': 1,
    }
    subAllTest(Api, stk_info, 1)
    Api.Logout()

if __name__=='__main__':
    unittest.main()
