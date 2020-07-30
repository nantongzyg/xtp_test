#!/usr/bin/python
# -*- encoding: utf-8 -*-
import datetime
import logging
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
import quote_save


def subAllTest(Api,stk_info,client_id):
    print Api.GetApiVersion()
    # logger = log_set(client_id)
    # ------------------------------------------------------------------------------------------------------------------
    #　业务回调(成交回报／报单回报／报单查询／撤单废单)-------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # 报单查询业务回调
    def on_option_market_data(exchange_id, data):
        print exchange_id, data

    def on_depth_market_data(data):
        print data
        #quote_save.hq_index(data, client_id)
        #quote_save.snap_level_spot(data, client_id)
        #quote_save.hq_snap_spot(data, client_id)

    Api.setSubAllOptionMarketDataHandle(on_option_market_data)
    Api.setDepthMarketDataHandle(on_depth_market_data)
    Api.SubscribeAllOptionMarketData(stk_info)
    while 1:
        sleep(1)

def subAllOrderBook(Api, stk_info, client_id):
    print Api.GetApiVersion()
    def on_order_book(exchange_id, data):
        print data
    
    def on_order_book_data(data):
        print 'on_order_book_data'
        print data
        # quote_save.save_ob(data, client_id)

    Api.setSubAllOptionOrderBookHandle(on_order_book)
    Api.setOrderBookHandle(on_order_book_data)
    Api.SubscribeAllOptionOrderBook(stk_info)
    while 1:
        sleep(1)


def subAllTickByTick(Api, stk_info, client_id):
    print Api.GetApiVersion()

    def on_all_tick_by_tick(exchange_id, data):
        print data
    
    def on_tick_by_tick(data):
        print data
       # quote_save.save_tick_by_tick(data, client_id)

    Api.setSubAllTickByTickHandle(on_all_tick_by_tick)
    Api.setTickByTickHandle(on_tick_by_tick)
    Api.SubscribeAllOptionTickByTick(stk_info)
    print 'SubscribeAllOptionTickByTick'
    while 1:
        sleep(1)

def queryAllTickers(Api, req):
    def on_queryalltickers(data, error, last):
        print data

    Api.setQueryAllTickersHandle(on_queryalltickers)
    Api.QueryAllTickers(req)
    while 1:
        time.sleep(10)
  
def queryAllTickersPriceInfo(Api):
    def on_querytickerspriceinfo(data, error, last):
        print data, error

    Api.setQueryAllTickersPriceInfoHandle(on_querytickerspriceinfo)
    Api.QueryAllTickersPriceInfo()
    
    while 1:
        time.sleep(10)

def queryTickersPriceInfo(Api, req):
    def on_querytickerspriceinfo(data, error, last):
        print data, error

    Api.setQueryAllTickersPriceInfoHandle(on_querytickerspriceinfo)
    Api.QueryTickersPriceInfo()
    
    while 1:
        time.sleep(10)




