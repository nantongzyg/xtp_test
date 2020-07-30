#!/usr/bin/python
# -*- coding: UTF-8 -*-

from api.attribute import Attribute
import random

class DemoConfig():

    case01 = Attribute({
        'ticker_sh': ['600020', '600030', '600120', '600089']
    })

    case02 = Attribute({
        'price': [10.89, 120.2]
    })

if __name__ == '__main__':

    DemoConfig.case01.ticker_sh.append('600100')

    ticker = random.choice(DemoConfig.case01.ticker_sh)
    print ticker