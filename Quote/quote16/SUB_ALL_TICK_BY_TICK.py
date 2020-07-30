#!/usr/bin/python
# -*- encoding: utf-8 -*-
from quoteService import *
from multiprocessing import Pool
import os, time, random
import sys
from random import randint
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from config import *


class SUB_ALL_TICK_BY_TICK(xtp_test_case):
    def test_SUB_ALL_TICK_BY_TICK(self):
        pool_count = 1
        p = Pool(pool_count)
        for i in range(pool_count):
            p.apply_async(sub_market, args=(i,))
        p.close()
        p.join()

def sub_market(name):
    client_id_key = 'id' + str(name + 1)
    client_id = CONST_QUOTE_CLIENT_ID[client_id_key]
    Api = XTPQuoteApi(client_id)
    Api.Login()
    subAllTickByTick(Api, 1)
    Api.Logout()

if __name__=='__main__':
    unittest.main()
