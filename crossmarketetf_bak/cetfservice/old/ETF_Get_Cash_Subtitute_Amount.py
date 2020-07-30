#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from decimal import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from etf_utils import get_valid_amount
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryPreclosePriceDB import QueryPreclosePriceDB
from QueryPremiumRatioDB import QueryPremiumRatioDB


#计算总的现金替代金额：允许现金替代金额＝替代证券数量×该证券参考价格×（1＋现金替代溢价比例）
def etf_get_cash_subtitute_amount(Api, market, etf_code1, component_unit):
    stkcode = {
        'ticker': '',
    }

    stk_asset_total = 0
    substitute_flag_optional = QueryPremiumRatioDB(etf_code1)
    for substitute in substitute_flag_optional:
        stkasset = Api.trade.QueryPositionSync(stkcode)
        preclose_price = QueryPreclosePriceDB(substitute[0])
        # (1 + 溢价比例) * 昨收价，四舍五入保留两位小数
        ratio = float(Decimal(
            Decimal(str((1 + substitute[1]) * preclose_price)).quantize(
                Decimal('.01'), rounding=ROUND_HALF_UP)))
        if substitute[0] in stkasset['data']:
            # 申购所需成分股数量>=可用持仓,计算缺失股数所需的金额
            if market == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                if substitute[2] >= stkasset['data'][substitute[0]]['position']['total_qty']:
                    stk_asset_total = stk_asset_total + float(preclose_price) * \
                                            (substitute[2] - stkasset['data']
                                            [substitute[0]]['position']['total_qty']) * \
                                            (1 + float(substitute[1]))
            else:
                if substitute[2] >= stkasset['data'][substitute[0]]['position']['total_qty']:

                    stk_asset_total = stk_asset_total + ratio * \
                                            (substitute[2] - stkasset['data']
                                            [substitute[0]]['position']['total_qty'])
        else:
            if market == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                stk_asset_total = (stk_asset_total + float(preclose_price) *
                                substitute[2] * (1 + float(substitute[1])))
            else:
                stk_asset_total = (stk_asset_total + substitute[2] * ratio)

    return stk_asset_total








