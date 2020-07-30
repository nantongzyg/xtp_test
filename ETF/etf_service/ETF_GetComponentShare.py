#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import Api
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryEtfComponentsCodeDB import QueryEtfComponentsCodeDB
from QueryEtfinfoDB import QueryEtfCode1
from QueryMarketByStkcode import QueryMarketByStkcode

# 查询etf所有成分股的总持仓
def etf_get_all_component_stk(ticker):
    etf_code1 = QueryEtfCode1(ticker)
    component_code = QueryEtfComponentsCodeDB(etf_code1)
    stkcode = {
        'ticker': '',
    }
    stkasset = Api.trade.QueryPositionSync(stkcode)
    component_stk_info = {}
    for code in component_code:
        stk_info = {}
        if code in stkasset['data']:
            stk_position = stkasset['data'][code]['position']
            stk_code = stk_position['ticker']
            stk_info['证券代码'] = stk_position['ticker']
            stk_info['市场'] = stk_position['market']
            stk_info['总持仓'] = stk_position['total_qty']
            stk_info['可卖持仓'] = stk_position['sellable_qty']
            stk_info['昨日持仓'] = stk_position['yesterday_position']
            stk_info['今日可申购赎回持仓'] = stk_position['purchase_redeemable_qty']
            stk_info['持仓成本价'] = stk_position['avg_price']
            stk_info['浮动盈亏'] = stk_position['unrealized_pnl']
            component_stk_info[stk_code] = stk_info
        else:
            market_type = QueryMarketByStkcode(code)
            if market_type == 1:
                market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']
            elif market_type == 2:
                market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']
            stk_info['证券代码'] = code
            stk_info['市场'] = market
            stk_info['总持仓'] = 0
            stk_info['可卖持仓'] = 0
            stk_info['昨日持仓'] = 0
            stk_info['今日可申购赎回持仓'] = 0
            stk_info['持仓成本价'] = 0
            stk_info['浮动盈亏'] = 0
            component_stk_info[code] = stk_info

    return component_stk_info

# 查询etf某个成分股的总持仓
def etf_get_one_component_stk(ticker):
    stkcode = {
        'ticker': '',
    }
    stkasset = Api.trade.QueryPositionSync(stkcode)
    component_stk_info = {}
    stk_info = {}
    if ticker in stkasset['data']:
        stk_position = stkasset['data'][ticker]['position']
        stk_code = stk_position['ticker']
        stk_info['证券代码'] = stk_position['ticker']
        stk_info['市场'] = stk_position['market']
        stk_info['总持仓'] = stk_position['total_qty']
        stk_info['可卖持仓'] = stk_position['sellable_qty']
        stk_info['昨日持仓'] = stk_position['yesterday_position']
        stk_info['今日可申购赎回持仓'] = stk_position['purchase_redeemable_qty']
        stk_info['持仓成本价'] = stk_position['avg_price']
        stk_info['浮动盈亏'] = stk_position['unrealized_pnl']
        component_stk_info[stk_code] = stk_info
    else:
        market_type = QueryMarketByStkcode(ticker)
        if market_type == 1:
            market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']
        elif market_type == 2:
            market = Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']
        stk_info['证券代码'] = ticker
        stk_info['市场'] = market
        stk_info['总持仓'] = 0
        stk_info['可卖持仓'] = 0
        stk_info['昨日持仓'] = 0
        stk_info['今日可申购赎回持仓'] = 0
        stk_info['持仓成本价'] = 0
        stk_info['浮动盈亏'] = 0
        component_stk_info[ticker] = stk_info

    return component_stk_info

# if __name__ == '__main__':
#     etf_get_all_component_stk(Api, '510050')