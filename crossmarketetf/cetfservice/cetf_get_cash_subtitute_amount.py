#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from decimal import *
sys.path.append("/home/yhl2/workspace/xtp_test")
from crossmarketetf.cetfmysql.query_preclose_price import *
from crossmarketetf.cetfmysql.query_premium_ratio import query_premium_ratio
from crossmarketetf.cetfmysql.query_premium_ratio import query_discount_ratio
# from xtp.api.xtpapi import Api


def cetf_get_cash_subtitute_amount(Api, wt_reqs, etf_code1, component_unit):
    """
    计算总的现金替代金额：允许现金替代金额＝替代证券数量×该证券参考价格×（1＋现金替代溢价比例）
    :param component_unit:
    :return:
    """
    stkcode = {
        'ticker': '',
    }
    market = wt_reqs['market']
    stk_asset_total = 0
    side = wt_reqs['side']
    # 查询所有可现金替代成分股的溢价比例
    substitute_flag_optional = query_premium_ratio(etf_code1)
    if int(side) == 8:
        print 'side******',side
        substitute_flag_optional = query_discount_ratio(etf_code1)
    # 查询所有持仓
    stkasset = Api.trade.QueryPositionSync(stkcode)
    for substitute in substitute_flag_optional:
        # 查询单支成分股昨收价
        preclose_price = query_preclose_price(substitute[0])
        # 深圳市场成分股价格计算，四舍五入保留两位小数
        ratio = float(Decimal(
            Decimal(str((1 + substitute[1]) * preclose_price)).quantize(
                Decimal('.01'), rounding=ROUND_HALF_UP)))
        # 如果已有该成分股持仓
        if substitute[0] in stkasset['data']:
            # 上海市场计算可以现金替代所需金额 = 昨收价*（1+溢价比例） * 数量
            # 昨收价*（1+溢价比例）可能为3位小数，不四舍五入成两位
            if market == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                # 申购所需成分股数量>=可用持仓,计算缺失股数所需的金额
                if substitute[2] * component_unit >= stkasset['data'][
                                        substitute[0]]['position']['total_qty']:
                    stk_asset_total = (
                        stk_asset_total + float(preclose_price) *
                        (substitute[2] * component_unit - stkasset['data'][
                            substitute[0]]['position']['total_qty']) *
                        (1 + float(substitute[1]))
                                       )
            # 深圳市场计算可以现金替代所需金额 = 溢价 * 数量
            # 与上海市场不同， 昨收价*（1+溢价比例）四舍五入成两位小数
            else:
                if substitute[2] * component_unit >= stkasset['data'][
                    substitute[0]]['position']['total_qty']:
                    stk_asset_total = (stk_asset_total + ratio *
                                       (substitute[2]*component_unit -
                                        stkasset['data'][substitute[0]][
                                            'position']['total_qty']))
        # 没有该成分股持仓，直接计算
        else:
            # 上海市场计算
            if market == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                stk_asset_total = (stk_asset_total + float(preclose_price) *
                                substitute[2] * component_unit *
                               (1 + float(substitute[1])))
            # 深圳市场计算
            else:
                stk_asset_total = (stk_asset_total + substitute[2] *
                                   component_unit * ratio)

    return stk_asset_total

# if __name__ == '__main__':
#     print cetf_get_cash_subtitute_amount(Api,Api.const.XTP_MARKET_TYPE[
#         'XTP_MKT_SH_A'],'510301',2)







