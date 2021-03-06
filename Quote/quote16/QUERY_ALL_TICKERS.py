#!/usr/bin/python
# -*- encoding: utf-8 -*-
from quoteOneService import *
from multiprocessing import Pool
import os, time, random
import sys
import time
from random import randint
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from config import *


class QUERY_ALL_TICKERS(xtp_test_case):

    def test_QUERY_ALL_TICKERS(self):
        p = Pool(1)
        for i in range(1):
            p.apply_async(query_all_tickers, args=(i,))
        p.close()
        p.join()

def query_all_tickers(name):
    client_id_key = 'id' + str(name +1)
    client_id = CONST_QUOTE_CLIENT_ID.get(client_id_key)
    Api = XTPQuoteApi(client_id)
    print Api.GetApiVersion()
    time.sleep(3)
    Api.Login()
    queryAllTickers(Api, {'exchange_id': 2}, 1)
    Api.Logout()

if __name__=='__main__':
    unittest.main()
