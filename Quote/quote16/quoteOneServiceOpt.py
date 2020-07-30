#!/usr/bin/python
# -*- encoding: utf-8 -*-
import datetime
import logging
import sys
import time
from log_quote import *
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
import quote_save


def subMarketData(Api,stk_info,client_id):
    print Api.GetApiVersion()
    # logger = log_set(client_id)
    # ------------------------------------------------------------------------------------------------------------------
    #　业务回调(成交回报／报单回报／报单查询／撤单废单)-------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # 报单查询业务回调
    def on_market_data(data, error, last):
        print data, error

    def on_depth_market_data(data):
        print 'on_depth_market_data'
        print data
        # quote_save.hq_index_one(data)
        quote_save.snap_level_spot_one(data, client_id)
        #quote_save.hq_snap_spot(data)
    
    Api.setSubMarketDataHandle(on_market_data)
    Api.setDepthMarketDataHandle(on_depth_market_data)
    Api.SubscribeMarketData(stk_info)
    sleep(15)
    print '-----UnSubscribeMarketData-----'
    Api.UnSubscribeMarketData(stk_info)

def subOrderBook(Api, stk_info):
    print Api.GetApiVersion()
    def on_order_book(data):
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

    def on_all_tick_by_tick(data):
        print data
    
    def on_tick_by_tick(data):
        print data
        #quote_save.save_tick_by_tick(data) 

    Api.setSubTickByTickHandle(on_all_tick_by_tick)
    Api.setTickByTickHandle(on_tick_by_tick)
    Api.SubscribeTickByTick(stk_info)
    sleep(8)
    print '-----UnSubscribeTickByTick------'
    Api.UnSubscribeTickByTick(stk_info)

def queryAllOpt(Api, req):
    def on_queryallopt(data, error, last):
        print data

    print 'setQueryAllOptHandle'
    time.sleep(5)
    Api.setQueryAllTickersHandle(on_queryallopt)
    print 'QueryAllOpt'
    time.sleep(5)
    Api.QueryAllTickers(req)
    while 1:
        time.sleep(10)
  
def queryAllTickersPriceInfo(Api):
    def on_querytickerspriceinfo(data, error, last):
        print data

    print 'queryAllTickersPriceInfo calling'
    Api.setQueryAllTickersPriceInfoHandle(on_querytickerspriceinfo)
    Api.QueryAllTickersPriceInfo()
    print 'queryAllTickersPriceInfo end'
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




