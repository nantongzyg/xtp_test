#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryEtfComponentsDB import *
from QueryEtfComponentsCodeDB import QueryEtfComponentsInfoDB
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from etf_utils import get_valid_amount
from ETF_GetComponentShare import etf_get_one_component_stk
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtpapi import Api

# 禁止现金替代成分股计数
forbidden_count = 0
# 允许现金替代成分股计数
optional_count = 0

#根据etf代码买入一篮子股票，只买非必须现金替代部分
def etf_basket_add_real(Api, market, bsflag, unit_info, case_goal):
    data_list = []
    component_rs = QueryEtfComponentsInfoDB(unit_info['ticker'],market)
    for rs in component_rs:
        data = {}
        data['quantity'] = rs[2]
        data['component_ticker'] = rs[0]
        if rs[1] == 0:
            data['replace_type'] = Api.const.ETF_REPLACE_TYPE['ERT_CASH_FORBIDDEN']
        elif rs[1] == 1:
            data['replace_type'] = Api.const.ETF_REPLACE_TYPE['ERT_CASH_OPTIONAL']
        else:
            data['replace_type'] = Api.const.ETF_REPLACE_TYPE['ERT_CASH_MUST']
        data['component_market'] = market
        data_list.append(data)

    for data in data_list:
        if data['quantity'] != 0:

            wt_reqs_side = getSide(Api, bsflag)
            wt_reqs = {
                'market': data['component_market'],
                'order_client_id': 2,
                'ticker': data['component_ticker'],  # 返回的股票代码有空格
                'side': wt_reqs_side,
                'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
                'position_effect': 
                    Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
            }
            #（T-1日+T日）总的成份股比1unit少100股
            # creational_qty = 0
            # if unit_info.has_key('T-1日+T日成份股'):
            #     req = {
            #         'ticker': ''
            #     }
            #     stkasset = Api.trade.QueryPositionSync(req)
            #     if stkasset['data'].has_key(wt_reqs['ticker']):
            #         creational_qty = stkasset['data'][wt_reqs['ticker']]['position']['creational_qty']
            #
            #     if unit_info['T-1日+T日成份股'] == 100:
            #         if data['quantity'] - creational_qty > 100 and creational_qty >= 0:
            #             wt_reqs['quantity'] = data['quantity'] - creational_qty - 100
            #             Api.trade.InsertOrder(wt_reqs)
            #         elif data['quantity'] == 200 and data['quantity'] - creational_qty >= 100:
            #             wt_reqs['quantity'] = 100
            #             Api.trade.InsertOrder(wt_reqs)
            #     elif unit_info['T-1日+T日成份股'] < 100:
            #         qty1 = int(data['quantity'] * unit_info['T-1日+T日成份股'] - creational_qty) * 1.0 / 100
            #         qty2 = int(data['quantity'] * unit_info['T-1日+T日成份股'] - creational_qty) / 100
            #         if qty1 - qty2 > 0:
            #             wt_reqs['quantity'] = int(data['quantity'] * unit_info['T-1日+T日成份股'] - creational_qty) + 50
            #         else:
            #             wt_reqs['quantity'] = int(data['quantity'] * unit_info['T-1日+T日成份股'] - creational_qty)
            #
            #         if creational_qty < unit_info['T-1日+T日成份股'] * data['quantity']:
            #             Api.trade.InsertOrder(wt_reqs)
            #
            # if unit_info.has_key('T日部分成份股'):
            #     if unit_info['T日部分成份股'] >= 100:
            #         wt_reqs['quantity'] = unit_info['T日部分成份股']
            #         Api.trade.InsertOrder(wt_reqs)

            #按比例购买成份股
            if data['replace_type'] == Api.const.ETF_REPLACE_TYPE['ERT_CASH_FORBIDDEN']:
                global count
                if 'forbidden_unit' in unit_info:
                    component_quantity = int(data['quantity'] * unit_info['forbidden_unit'])
                    wt_reqs['quantity'] = get_valid_amount(component_quantity)
                if wt_reqs['quantity'] != 0:
                    Api.trade.InsertOrder(wt_reqs)
            elif data['replace_type'] == \
                    Api.const.ETF_REPLACE_TYPE['ERT_CASH_OPTIONAL']:
                if 'optional_unit' in unit_info:
                    if unit_info['optional_unit'] >= 100:
                        wt_reqs['quantity'] = unit_info['optional_unit']
                    else:
                        component_quantity = int(data['quantity'] *
                                                 unit_info['optional_unit'])
                        wt_reqs['quantity'] = get_valid_amount(component_quantity)

                if wt_reqs['quantity'] != 0:
                    Api.trade.InsertOrder(wt_reqs)

def getSide(Api,bsflag):
    if bsflag == 'B':
        return Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY']
    elif bsflag == 'S':
        return Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']

def getPropertyQuqntity(unit_info, Api, wt_reqs, data, unit_type):
    global optional_count, forbidden_count
    component_stk_info = etf_get_one_component_stk(data['component_ticker'])
    purchase_redeemable_qty = 0
    if component_stk_info != {}:
        purchase_redeemable_qty = \
            component_stk_info[data['component_ticker']]['今日可申购赎回持仓']

    if (purchase_redeemable_qty == 0 or component_stk_info == {}):
        if data['replace_type'] == Api.const.ETF_REPLACE_TYPE['ERT_CASH_OPTIONAL']:
            optional_count += 1
        elif data['replace_type'] == Api.const.ETF_REPLACE_TYPE['ERT_CASH_FORBIDDEN']:
            forbidden_count += 1

    if unit_type in unit_info \
            and (optional_count == 1 or forbidden_count == 1) \
            and (purchase_redeemable_qty == 0 or
                    component_stk_info == {}):
        wt_reqs['quantity'] = wt_reqs['quantity'] + unit_info[unit_type]

    return wt_reqs['quantity']
