#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import os
import time
sys.path.append('/home/yhl2/workspace/xtp_test/option/mysql')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/Risk')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/GPMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ETFMM_D')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ETFMM_K')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/FJZJJMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/IPO')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ReverseRepo')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/AllotmentPayment')
import runcase_common
import runcase_ipo
import runcase_allPayment
import gpmm_risk

#将测试数据导入到mc-test当日库
def Transferdata():
    import SqlData_Transfer
    sqldata = SqlData_Transfer.SqlData_Transfer()
    sqldata.delete_exch_sec()
    sqldata.insert_exch_sec()

    sqldata.delete_stk_asset()
    sqldata.insert_stk_asset()

    sqldata.delete_issue_params()
    sqldata.insert_issue_params()

    sqldata.delete_rights_issue_params()
    sqldata.insert_rights_issue_params()

    # sqldata.delete_etf_baseinfo()
    # sqldata.insert_etf_baseinfo()

    # sqldata.delete_etf_components()
    # sqldata.insert_etf_components()

def runcase_SZ():

    casepath = '/home/yhl2/workspace/xtp_test/Autocase_Result/'
    case1 = runcase_common.getCases(casepath + 'GPMM')
    # case2 = runcase_common.getCases(casepath + 'ETFMM_D')
    # case3 = runcase_common.getCases(casepath + 'ETFMM_K')
    # case4 = runcase_common.getCases(casepath + 'FJZJJMM')
    # case5 = runcase_common.getCases(casepath + 'ReverseRepo')
    # case6 = runcase_common.getCases(casepath + 'IPO')
    # case7 = runcase_common.getCases(casepath + 'AllotmentPayment')
    path = '/home/yhl2/workspace/xtp_test/utils'
    runcase_common.runCases(case1, path,  u'普通业务自动化用例.xlsx',u'深圳限价')
    # runcase_common.runCases(case1, path, u'普通业务自动化用例.xlsx', u'深圳市价')
    # runcase_common.runCases(case2, path, u'ETF买卖单市场.xlsx', u'深圳限价')
    # runcase_common.runCases(case2, path, u'ETF买卖单市场.xlsx', u'深圳市价')
    # runcase_common.runCases(case3, path, u'ETF买卖跨市场.xlsx', u'深圳限价')
    # runcase_common.runCases(case3, path, u'ETF买卖跨市场.xlsx', u'深圳市价')
    # runcase_common.runCases(case4, path, u'分级子基金买卖.xlsx', u'深圳限价')
    # runcase_common.runCases(case4, path, u'分级子基金买卖.xlsx', u'深圳市价')
    # runcase_common.runCases(case5, path, u'普通业务自动化用例.xlsx', u'逆回购_深圳')
    # runcase_ipo.runCases(case6, path, u'普通业务自动化用例.xlsx', u'新股申购_深圳')
    # runcase_allPayment.runCases(case7, path, u'普通业务自动化用例.xlsx', u'配股缴款_深圳')

def runcase_SH():
    # case1 = runcase_common.getCases(casepath + 'GPMM')
    # case2 = runcase_common.getCases(casepath + 'ETFMM_D')
    # case3 = runcase_common.getCases(casepath + 'ETFMM_K')
    # case4 = runcase_common.getCases(casepath + 'FJZJJMM')
    # case5 = runcase_common.getCases(casepath + 'ReverseRepo')
    # case6 = runcase_common.getCases(casepath + 'IPO')
    # case7 = runcase_common.getCases(casepath + 'AllotmentPayment')
    path = '/home/yhl2/workspace/xtp_test/utils'
    # runcase_common.runCases(case1, path,  u'普通业务自动化用例.xlsx',u'上海限价')
    # runcase_common.runCases(case1, path, u'普通业务自动化用例.xlsx', u'上海市价')
    # runcase_common.runCases(case5, path, u'普通业务自动化用例.xlsx', u'逆回购_上海')
    # runcase_ipo.runCases(case6, path, u'普通业务自动化用例.xlsx', u'新股申购_上海')
    # runcase_allPayment.runCases(case7, path, u'普通业务自动化用例.xlsx', u'配股缴款_上海')
    # runcase_common.runCases(case2, path, u'ETF买卖单市场.xlsx', u'上海限价')
    # runcase_common.runCases(case2, path, u'ETF买卖单市场.xlsx', u'上海市价')
    # runcase_common.runCases(case3, path, u'ETF买卖跨市场.xlsx', u'上海限价')
    # runcase_common.runCases(case3, path, u'ETF买卖跨市场.xlsx', u'上海市价')
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'权利方限价_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'权利方市价_沪市')
    runcase_common.runCasesOption(path,  u'个股期权自动化用例.xlsx', u'义务方限价（认购合约）_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'义务方市价（认购合约）_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'义务方限价（认沽合约）_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'义务方市价（认沽合约）_沪市')

if __name__ == '__main__':
    # Transferdata()
    # time.sleep(5)
    runcase_SZ()
    # runcase_SH()


