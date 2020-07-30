#!/usr/bin/python
# -*- encoding: utf-8 -*-
import datetime
import logging
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
import quote_save

class QuoteTest(xtp_test_case):
    def subMarketData(self, Api, stk_info, rs_expect):
        print Api.GetApiVersion()
        def on_market_data(data, error, last):
            print error

        Api.setSubMarketDataHandle(on_market_data)
        Api.SubscribeMarketData(stk_info)
        time.sleep(1)

    def subOrderBook(Api, stk_info):
        print Api.GetApiVersion()
        def on_order_book(data, error, last):
            print data

        def on_order_book_data(data):
            print data
            #quote_save.save_ob(data)

        Api.setSubOrderBookHandle(on_order_book)
        Api.setOrderBookHandle(on_order_book_data)
        Api.SubscribeOrderBook(stk_info)
        sleep(5)
        print '-----UnSubscribeOrderBook-----'
        Api.UnSubscribeOrderBook(stk_info)

    def subTickByTick(Api, stk_info):
        print Api.GetApiVersion()

        def on_all_tick_by_tick(data, error, is_last):
            print data

        def on_tick_by_tick(data):
            print data
            #quote_save.save_tick_by_tick(data)

        Api.setSubTickByTickHandle(on_all_tick_by_tick)
        Api.setTickByTickHandle(on_tick_by_tick)
        while 1:
            Api.SubscribeTickByTick(stk_info)
            sleep(10)
            print '-----UnSubscribeTickByTick------'
            Api.UnSubscribeTickByTick(stk_info)
            sleep(3)

    def queryAllTickers(Api, req, client_id):
        def on_queryalltickers(data, error, last):
            print data


        Api.setQueryAllTickersHandle(on_queryalltickers)
        Api.QueryAllTickers(req)
        while 1:
            time.sleep(10)

    def queryAllTickersPriceInfo(Api):
        def on_querytickerspriceinfo(data, error, last):
            print 11111111111
            print data

        Api.setQueryAllTickersPriceInfoHandle(on_querytickerspriceinfo)
        Api.QueryAllTickersPriceInfo()
        while 1:
            time.sleep(1)

    def queryTickersPriceInfo(Api, req):
        def on_querytickerspriceinfo(data, error, last):
            print data

        print 'QueryTickersPriceInfo calling'
        Api.setQueryTickersPriceInfoHandle(on_querytickerspriceinfo)
        print 'QueryTickersPriceInfo middle'
        Api.QueryTickersPriceInfo(req)
        print 'QueryTickersPriceInfo end'
        while 1:
            time.sleep(1)




