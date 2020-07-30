#!/usr/bin/python
# -*- encoding: utf-8 -*-
import datetime
import logging
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
import quote_save


def subMarketData(Api, stk_info, client_id):
    print Api.GetApiVersion()
    # logger = log_set(client_id)
    # ------------------------------------------------------------------------------------------------------------------
    #　业务回调(成交回报／报单回报／报单查询／撤单废单)-------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # 报单查询业务回调
    def on_market_data(data, error, last):
        print data, error

    def on_depth_market_data(data):
        print data
        # quote_save.hq_index_one(data)
        # quote_save.snap_level_spot_one(data, client_id)
        #quote_save.hq_snap_spot(data)
    
    Api.setSubMarketDataHandle(on_market_data)
    Api.setDepthMarketDataHandle(on_depth_market_data)
    Api.SubscribeMarketData(stk_info)
    while 1:
        sleep(1)

def subOrderBook(Api, stk_info):
    print Api.GetApiVersion()
    def on_order_book(data, error, last):
        print data, error
    
    def on_order_book_data(data):
        print data
        #quote_save.save_ob(data)

    Api.setSubOrderBookHandle(on_order_book)
    Api.setOrderBookHandle(on_order_book_data)
    Api.SubscribeOrderBook(stk_info)
    while 1:
        sleep(1)

def subTickByTick(Api, stk_info):
    print Api.GetApiVersion()

    def on_all_tick_by_tick(data, error, is_last):
        print data, error
    
    def on_tick_by_tick(data):
        print data
        #quote_save.save_tick_by_tick(data) 

    Api.setSubTickByTickHandle(on_all_tick_by_tick)
    Api.setTickByTickHandle(on_tick_by_tick)
    Api.SubscribeTickByTick(stk_info)
    while 1:
        sleep(1)

def queryAllTickers(Api, req, client_id):
    def on_queryalltickers(data, error, last):
        print data, error

    Api.setQueryAllTickersHandle(on_queryalltickers)
    Api.QueryAllTickers(req)
    while 1:
        time.sleep(10)
  
def queryAllTickersPriceInfo(Api):
    def on_querytickerspriceinfo(data, error, last):
        print data, error, last

    print 33333333333
    Api.setQueryAllTickersPriceInfoHandle(on_querytickerspriceinfo)
    print 44444444444
    Api.QueryAllTickersPriceInfo()
    print 55555555555
    while 1:
        time.sleep(1)

def queryTickersPriceInfo(Api, tickers, count, exchange_id):
    def on_querytickerspriceinfo(data, error, last):
        print data, error, last

    Api.setQueryTickersPriceInfoHandle(on_querytickerspriceinfo)
    Api.QueryTickersPriceInfo(tickers, count, exchange_id)
    while 1:
        time.sleep(1)




