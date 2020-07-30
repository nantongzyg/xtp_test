#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import random
import sys
import time
from multiprocessing import Pool

from quoteOneService import *

sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *


class SUB_MARKET_DATA(xtp_test_case):
    def test_SUB_MARKET_DATA(self):
        print('Parent process %s.' % os.getpid())
        p = Pool(1)
        for i in range(1):
            p.apply_async(sub_market, args=(i,))
        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        print('All subprocesses done.')

def sub_market(name):
    client_id = 70
    Api = XTPQuoteApi(client_id)
    Api.Login()
    stk_info = {
        'ticker': '600066',  # 全部行情
        'exchange_id': 1  # 沪A
    }
    subTickByTick(Api, stk_info)
    Api.Logout()

if __name__=='__main__':
    unittest.main()
