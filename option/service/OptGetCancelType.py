#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
from getTime import *
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *

#-----------------------------------------------------------------------------------------------------------------------
# 定义函数：获取撤单类型（交易所主动撤(False)或自己手动发起撤单(True)）
#-----------------------------------------------------------------------------------------------------------------------
def getCancelType(Api,price_type,expectStatus):
    isCancel = True
    xtp_price_type = Api.const.XTP_PRICE_TYPE
    #当价格条件为：全成全撤，即成剩撤，五档转撤(期望状态：非内部撤单)时，对手方最优（期望状态：已撤）不需要手动发起撤XTP_PRICE_ALL_OR_CANCEL
    if price_type in(xtp_price_type['XTP_PRICE_BEST_OR_CANCEL'], xtp_price_type['XTP_PRICE_ALL_OR_CANCEL'],
                     xtp_price_type['XTP_PRICE_BEST5_OR_CANCEL']) and expectStatus!='内部撤单':
        isCancel = False
    else:
        isCancel = True

    return isCancel

