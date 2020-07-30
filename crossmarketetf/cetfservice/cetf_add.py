#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfmysql.query_creation_redem_unit import *
from mysql.getUpOrDownPrice import *
from crossmarketetf.cetfservice.cetf_utils import split_etf_quantity


def cetf_add(Api, market, etf_code, unit):
    """
    二级市场买入ETF
    :param Api:
    :param market: 格式：Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']
    :param etf_code: ETF二级市场代码
    :param unit: 买入ETF的份数
    :return: None
    """
    # 查询ETF最小申赎单位
    creation_redemption_unit = query_creation_redem_unit(etf_code)
    # 总的委托数量
    quantity = int(unit * creation_redemption_unit)
    # 若etf买卖数量大于最大值，则做拆分
    quantity_list = split_etf_quantity(quantity)

    limitup_lx = getUpPrice(etf_code)

    for etf_quantity in quantity_list:
        wt_reqs = {
            'market': market,
            'order_client_id': 2,
            'ticker': etf_code,  # 返回的股票代码有空格
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
            'price':limitup_lx,
            'quantity': etf_quantity,
            'position_effect':     
                Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT']
        }
        Api.trade.InsertOrder(wt_reqs)
     
