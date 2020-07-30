#!/usr/bin/python
# -*- encoding: utf-8 -*-
import datetime
import logging
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
import quote_save

count = 0
def unSubAllMarketData(Api, client_id):
    print Api.GetApiVersion()
    # logger = log_set(client_id)
    # ------------------------------------------------------------------------------------------------------------------
    #　业务回调(成交回报／报单回报／报单查询／撤单废单)-------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # 报单查询业务回调
    def on_market_data(data):
        print data

    def on_depth_market_data(data):
        print data['data_time']
        # pass
        #quote_save.hq_index(data, client_id)

    Api.setSubAllMarketDataHandle(on_market_data)
    Api.setDepthMarketDataHandle(on_depth_market_data)
    sleep(1)
    while 1:
        Api.SubscribeAllMarketData()
        sleep(5)
        Api.UnSubscribeAllMarketData()
        print '-------------------------------UnSubscribeAllMarketData---------------------------'
        sleep(15)


def subAllSnapLevelSpotTest(Api,stk_info,client_id):
    print Api.GetApiVersion()
    # logger = log_set(client_id)
    # ------------------------------------------------------------------------------------------------------------------
    #　业务回调(成交回报／报单回报／报单查询／撤单废单)-------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # 报单查询业务回调
    def on_market_data(data):
        print data

    def on_depth_market_data(data):
        quote_save.snap_level_spot(data, client_id)
    
    Api.setSubAllMarketDataHandle(on_market_data) 
    Api.setDepthMarketDataHandle(on_depth_market_data)
    Api.SubscribeAllMarketData()
    print 1111111111111111
    while 1:
        sleep(1)

def subAllHqSnapSpotTest(Api,stk_info,client_id):
    print Api.GetApiVersion()
    # logger = log_set(client_id)
    # ------------------------------------------------------------------------------------------------------------------
    #　业务回调(成交回报／报单回报／报单查询／撤单废单)-------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # 报单查询业务回调
    def on_market_data(data):
        print data

    def on_depth_market_data(data):
        quote_save.hq_snap_spot(data, client_id)
    
    Api.setSubAllMarketDataHandle(on_market_data) 
    Api.setDepthMarketDataHandle(on_depth_market_data)
    Api.SubscribeAllMarketData()
    while 1:
        sleep(1)

def unSubAllOrderBook(Api, client_id):
    print Api.GetApiVersion()
    def on_order_book(data):
        print data
    
    def on_order_book_data(data):
        print data['data_time']
        #quote_save.save_ob(data, client_id)

    Api.setSubAllOrderBookHandle(on_order_book)
    Api.setOrderBookHandle(on_order_book_data)
    Api.SubscribeAllOrderBook()
    sleep(5)
    print '-----UnSubscribeAllOrderBook-----'
    Api.UnSubscribeAllOrderBook()
    while 1:
        sleep(1)

def unSubAllTickByTick(Api, client_id):
    print Api.GetApiVersion()

    def on_all_tick_by_tick(data):
        print data
    
    def on_tick_by_tick(data):
        global count
        count += 1
        if count % 1000 == 0:
            print data['data_time']
       #quote_save.save_tick_by_tick(data, client_id) 

    Api.setSubAllTickByTickHandle(on_all_tick_by_tick)
    Api.setTickByTickHandle(on_tick_by_tick)
    print '++++++++++++++++++++++++++++++++++++++++++++'
    while 1:
        Api.SubscribeAllTickByTick()
        sleep(3)
        print '-------------------------------UnSubscribeAllTickByTick---------------------------'
        Api.UnSubscribeAllTickByTick()
        sleep(10)


def queryAllTickers(Api, req):
    def on_queryalltickers(data, error, last):
        print data

    Api.setQueryAllTickersHandle(on_queryalltickers)
    Api.QueryAllTickers(req)
    while 1:
        time.sleep(10)
  
def queryAllTickersPriceInfo(Api):
    def on_querytickerspriceinfo(data, error, last):
        print data

    Api.setQueryAllTickersPriceInfoHandle(on_querytickerspriceinfo)
    Api.QueryAllTickersPriceInfo()
    
    while 1:
        time.sleep(10)

def queryTickersPriceInfo(Api, tickers, count, exchange_id):
    def on_querytickerspriceinfo(data, error, last):
        print data

    Api.setQueryAllTickersPriceInfoHandle(on_querytickerspriceinfo)
    Api.QueryTickersPriceInfo(tickers, count, exchange_id)
    sleep(3)
    print 'QueryTickersPriceInfo calling'
    #while 1:
        #time.sleep(10)




