#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/service")
import ServiceConfig
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql/mysql")
from mfgetUpOrDownPrice import *

#验证报单推送或报单查询或成交回报的价格是否正确
#根据service配置和市场来确定是否校验data['price'],返回值：data['price']的校验结果
def checkDataPrice(Api,wt_reqs,price):
    flag=False
    #获取涨停价／跌停价
    up_price=getUpPrice(wt_reqs['ticker'])
    down_price=getDownPrice(wt_reqs['ticker'])
    #获取配置：沪Ａ市场的价格是否需要校验，（备注：上海mock下撮合价是１块）
    isCheck_HA_hbprice = ServiceConfig.IS_CHECK_HA_HB_PRICE
    # 如果配置为不做校验上海的回报价格且委托市场为上海
    if isCheck_HA_hbprice == False and wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
        flag = True
    #如果市场不为沪A或深A
    # elif wt_reqs['market'] not in(Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']):


    else:
        # 如果是限价
        if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
            # 如果是买,price应小于等于委托价格
            if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'] and wt_reqs['business_type'] != Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
                if wt_reqs['price'] >= price:
                    flag = True
                else:
                    logger.error('price应小于等于委托价格，price和委托价格分别是' + str(price) + ',' + str(wt_reqs['price']))
                    flag = False
            # 如果是卖,price应大于等于委托价格
            elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL'] and wt_reqs['business_type'] != Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
                if wt_reqs['price'] <= price:
                    flag = True
                else:
                    logger.error('price应大于等于委托价格，price和委托价格分别是' + str(price) + ',' + str(wt_reqs['price']))
                    flag = False
            else:
                if down_price<=price<=up_price:
                    flag = True
                else:
                    logger.error('price应介于张跌停之间，price和涨跌停价分别为'+str(price)+','+str(down_price)+','+str(up_price))
                    flag = False

        # 如果是市价，price应大于等于跌停小于等于涨停
        elif wt_reqs['price_type'] != Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
            if price >= down_price and price <= up_price:
                flag = True
            else:
                logger.error(
                    'price应大于等于跌停小于等于涨停，price和张跌停价格分别是' + str(price) + ',' + str(up_price) + ',' + str(down_price))
                flag = False

    return flag






