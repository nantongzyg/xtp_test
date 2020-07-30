#!/usr/bin/python
# -*- coding: UTF-8 -*-

from api.attribute import Attribute
from quote.daily import dailyData
from xtp.api.lib_20170306.xtpapi_20170303_1 import XTPConst


class Atc30:
    # --------------------------------------------------
    def __init__(self):
        raise NotImplementedError()

    quote = dailyData
    const = XTPConst()

    atc_301_02 = Attribute({
        'buy': {

        },
        'sell': [
            # 市场,  股票代码,  价,  量,  价格类型
            ['SZ', '159933', quote['SZ']['159933']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']],
            ['SZ', '159933', quote['SZ']['159933']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_BEST_OR_CANCEL']],
            ['SZ', '159933', quote['SZ']['159933']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL']],
            ['SZ', '159933', quote['SZ']['159933']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_ALL_OR_CANCEL']],
            ['SZ', '159933', quote['SZ']['159933']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_FORWARD_BEST']],
            ['SZ', '159933', quote['SZ']['159933']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_REVERSE_BEST_LIMIT']]
        ]
    })

    atc_302_01 = Attribute({ 
        'buy': [
            # 市场,  股票代码,  价,  量,  价格类型
            ['SH', '510300', quote['SH']['510300']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']],
            ['SH', '510300', quote['SH']['510300']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_BEST_OR_CANCEL']],
            ['SH', '510300', quote['SH']['510300']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL']],
            ['SH', '510300', quote['SH']['510300']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_ALL_OR_CANCEL']],
            ['SH', '510300', quote['SH']['510300']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_FORWARD_BEST']],
            ['SH', '510300', quote['SH']['510300']['last'], 100, const.XTP_PRICE_TYPE['XTP_PRICE_REVERSE_BEST_LIMIT']]
        ],
        'sell': {

        }
    })


if __name__ == '__main__':
    data = Atc30.atc_301_02
    print data
