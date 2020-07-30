#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfmysql.query_cetf_components_code import query_cetf_components_info
from cetf_utils import get_valid_amount,split_etf_quantity


def cetf_basket_add_real(Api, market, unit_info):
    """
    根据etf代码买入一篮子股票，只买非必须现金替代部分
    :param Api:
    :param market: etf市场，1是上海，2是深圳
    :param unit_info:
    :return:
    """
    # 将每支成分股信息(dict)加入到列表data_list中
    data_list = []
    component_rs = query_cetf_components_info(unit_info['ticker'],market)
    for rs in component_rs:
        data = {}
        data['quantity'] = rs[2]
        data['component_ticker'] = rs[0]
        data['replace_type'] = rs[1]
        if rs[8] == 1:
            market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']
        else:
            market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']
        data['component_market'] = market
        data_list.append(data)

    for data in data_list:
        wt_reqs = {
            'market': data['component_market'],
            'order_client_id': 2,
            'ticker': data['component_ticker'],  # 返回的股票代码有空格
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
            'position_effect': 
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }

        #按比例购买成份股
        if data['replace_type'] == 0:
            if 'forbidden_unit' in unit_info:
                wt_quantity = int(data['quantity'] * unit_info['forbidden_unit'])
                wt_reqs['quantity'] = get_valid_amount(wt_quantity)
            if wt_reqs['quantity'] != 0:
                Api.trade.InsertOrder(wt_reqs)
        elif data['replace_type'] == 1:
            if 'optional_unit' in unit_info:
                if unit_info['optional_unit'] >= 100:
                    wt_reqs['quantity'] = unit_info['optional_unit']
                    if wt_reqs['quantity'] != 0:
                        Api.trade.InsertOrder(wt_reqs)
                else:
                    wt_quantity = int(data['quantity'] *
                                             unit_info['optional_unit'])
                    wt_quantity = get_valid_amount(wt_quantity)
                    wt_quantity_list = split_etf_quantity(wt_quantity)
                    for number in wt_quantity_list:
                        wt_reqs['quantity'] = number
                        if wt_reqs['quantity'] != 0:
                            Api.trade.InsertOrder(wt_reqs)


# def getside(Api,bsflag):
#     if bsflag == 'B':
#         return Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY']
#     elif bsflag == 'S':
#         return Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']
