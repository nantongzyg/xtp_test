#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/Risk')
sys.path.append("/home/yhl2/workspace/xtp_test/Autocase_Result/Risk/service")
from utils import *
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
import CaseServiceRisk

path = '/home/yhl2/workspace/xtp_test/utils'

def runcase_Risk_GPMM():
    import gpmm_risk as a
    a.runCases(path, '风控.xlsx', u'风控-普通委托（股票）')

def runcase_Risk_ETFMM():
    import etfmm_risk as a
    a.runCases(path, '风控.xlsx', u'风控-普通委托（ETF）')

def runcase_Risk_ZJJMM():
    import zjjmm_risk as a
    a.runCases(path, '风控.xlsx', u'风控-分级基金（子基金）买卖')

def runcase_Risk_ReverseRepo():
    import nhg_risk as a
    a.runCases(path, '风控.xlsx', u'风控-逆回购')

def runcase_Risk_IPO():
    import xgsg_risk as a
    a.runCases(path, '风控.xlsx', u'风控-新股申购')

def runcase_Risk_AllotmentPayment():
    import pg_risk as a
    a.runCases(path, '风控.xlsx', u'风控-配股')

def runcase_Risk_ETFSS():
    import etfss_risk as a
    a.runCases(path, '风控.xlsx', u'风控-ETF申赎')

def runcase_Risk_FJJJSS():
    import fjjjss_risk as a
    a.runCases(path, '风控.xlsx', u'风控-分级基金（母基金）申赎')

def runcase_Risk():
    runcase_Risk_GPMM()
    runcase_Risk_ETFMM()
    runcase_Risk_ZJJMM()
    runcase_Risk_ReverseRepo()
    runcase_Risk_IPO()
    runcase_Risk_AllotmentPayment()
    runcase_Risk_ETFSS()
    #runcase_Risk_FJJJSS()

if __name__ == '__main__':
    runcase_Risk()
