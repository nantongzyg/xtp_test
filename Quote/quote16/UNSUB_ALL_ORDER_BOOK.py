#!/usr/bin/python
# -*- encoding: utf-8 -*-
from quoteServiceUnsub import *
from multiprocessing import Pool
import os, time, random
import sys
from random import randint
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from config import *


class UNSUB_ALL_ORDER_BOOK(xtp_test_case):
    def test_UNSUB_ALL_ORDER_BOOK(self):
        pool_count = 1
        p = Pool(pool_count)
        for i in range(pool_count):
            p.apply_async(sub_market, args=(i,))
        p.close()
        p.join()

def sub_market(name):
    start = time.time()
    client_id_key = 'id' + str(name +1)
    client_id = 54
    Api = XTPQuoteApi(client_id)
    flag = Api.Login()
    stk_info = {
        # 'ticker': 'shxtp*',
        # 'exchange_id': 2  # 1-沪A 2-深A
    }
    unSubAllOrderBook(Api, 1)
    Api.Logout()

    time.sleep(random.random() * 3)
    end = time.time()

if __name__=='__main__':
    unittest.main()
