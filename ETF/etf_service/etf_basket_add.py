#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from etf_utils import get_valid_amount


#根据etf代码买入一篮子股票，只买非必须现金替代部分
def etf_basket_add(Api, market, etf_code, component_unit):
    #查询一篮子股票有哪些
    query = {
        'market': market,
        'ticker': etf_code,
    }

    def on_QueryETFBasket(data, error, request_id, is_last):
        #异步回调函数on_QueryETFBasket
        quantity = 0
        if data['quantity'] != 0:
            if component_unit >= 100:
                quantity = component_unit
            else:
                component_quantity = int(data['quantity'] * component_unit)
                quantity = get_valid_amount(component_quantity)
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                'order_client_id': 2,
                'market': data['component_market'],
                'ticker': data['component_ticker'].strip(),  # 返回的股票代码有空格
                'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
                'quantity': quantity,
                'position_effect':
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            Api.trade.InsertOrder(wt_reqs)

    Api.trade.setQueryETFBasketHandle(on_QueryETFBasket)
    #查询成分股持仓
    Api.trade.QueryETFTickerBasket(query)
    time.sleep(3)




