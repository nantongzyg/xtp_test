#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append('/home/yhl2/workspace/xtp_test/mysql')
import SqlData_Transfer
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/GPMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ETFMM_D')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/HJETFMM_D')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ZQETFMM_D')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ETFMM_K')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/FJZJJMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/IPO')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ReverseRepo')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/AllotmentPayment')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/XjShHBJJMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/SjShHBJJMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/KZZMM')
import runcase_common
import runcase_ipo
import runcase_allPayment



#将测试数据导入到mc-test当日库
def Transferdata():

    sqldata = SqlData_Transfer.SqlData_Transfer()
    sqldata.delete_exch_sec()
    sqldata.insert_exch_sec()
    # # #
    sqldata.delete_fund_creation()
    sqldata.insert_fund_creation()
    #
    sqldata.delete_structured_fund_params()
    sqldata.insert_structured_fund_params()

    sqldata.delete_stk_asset()
    sqldata.insert_stk_asset()

    sqldata.delete_etf_baseinfo()
    sqldata.insert_etf_baseinfo()

    sqldata.delete_etf_components()
    sqldata.insert_etf_components()

    sqldata.delete_issue_params()
    sqldata.insert_issue_params()

    sqldata.delete_rights_issue_params()
    sqldata.insert_rights_issue_params()


path = '/home/yhl2/workspace/xtp_test/utils'

def runcase_SZ_GPMM():
    runcase_common.runCases(path,  u'普通业务自动化用例.xlsx',u'深圳限价')
    #runcase_common.runCases(path, u'普通业务自动化用例.xlsx', u'深圳市价')

def runcase_SZ_ETFMMD():
    runcase_common.runCases(path, u'ETF买卖.xlsx', u'深圳限价单市场')
    runcase_common.runCases(path, u'ETF买卖.xlsx', u'深圳市价单市场')

def runcase_HJ_ETFMMD():
    #runcase_common.runCases(path, u'hjetf_d.xlsx', u'上海限价')
    #runcase_common.runCases(path, u'hjetf_d.xlsx', u'上海市价')
    runcase_common.runCases(path, u'hjetf_d.xlsx', u'深圳限价')
    #runcase_common.runCases(path, u'hjetf_d.xlsx', u'深圳市价')

def runcase_ZQ_ETFMMD():
    runcase_common.runCases(path, u'zqetf_d.xlsx', u'上海限价')
    runcase_common.runCases(path, u'zqetf_d.xlsx', u'上海市价')
    runcase_common.runCases(path, u'zqetf_d.xlsx', u'深圳限价')
    runcase_common.runCases(path, u'zqetf_d.xlsx', u'深圳市价')

def runcase_SZ_ETFMMK():
    runcase_common.runCases(path, u'ETF买卖.xlsx', u'深圳限价跨市场')
    runcase_common.runCases(path, u'ETF买卖.xlsx', u'深圳市价跨市场')

def runcase_SZ_FJZJJMM():
    runcase_common.runCases(path, u'普通业务自动化用例.xlsx', u'分级子基金深圳限价')
    runcase_common.runCases(path, u'普通业务自动化用例.xlsx', u'分级子基金深圳市价')

def runcase_SZ_ReverseRepo():
    runcase_common.runCases(path, u'普通业务自动化用例.xlsx', u'逆回购_深圳')

def runcase_SZ_IPO():
    runcase_ipo.runCases(path, u'普通业务自动化用例.xlsx', u'新股申购_深圳')

def runcase_SZ_AllotmentPayment():
    runcase_allPayment.runCases(path, u'普通业务自动化用例.xlsx', u'配股缴款_深圳')

def runcase_SZ_KZZMM():
    runcase_common.runCases(path, u'kzz.xlsx', u'深圳限价')

def runcase_SH_GPMM():
    runcase_common.runCases(path,  u'普通业务自动化用例.xlsx',u'上海限价')
    runcase_common.runCases(path, u'普通业务自动化用例.xlsx', u'上海市价')


def runcase_SH_ETFMMD():
    runcase_common.runCases(path, u'ETF买卖.xlsx', u'上海限价单市场')
    runcase_common.runCases(path, u'ETF买卖.xlsx', u'上海市价单市场')


def runcase_SH_ETFMMK():
    runcase_common.runCases(path, u'ETF买卖.xlsx', u'上海限价跨市场')
    runcase_common.runCases(path, u'ETF买卖.xlsx', u'上海市价跨市场')

def runcase_SH_ReverseRepo():
    runcase_common.runCases(path, u'普通业务自动化用例.xlsx', u'逆回购_上海')


def runcase_SH_IPO():
    runcase_ipo.runCases(path, u'普通业务自动化用例.xlsx', u'新股申购_上海')


def runcase_SH_AllotmentPayment():
    runcase_allPayment.runCases(path, u'普通业务自动化用例.xlsx', u'配股缴款_上海')

def runcase_SH_HBJJ():
    runcase_common.runCases(path, u'普通业务自动化用例.xlsx', u'交易型货币基金买卖上海限价')
    runcase_common.runCases(path, u'普通业务自动化用例.xlsx', u'交易型货币基金买卖上海市价')

def runcase_SH_KZZMM():
    runcase_common.runCases(path, 'kzz.xlsx', u'上海限价')

def runcase_xianhuo_ychf_my():
    runcase_common.runCases(path, u'etfmmychfmy.xlsx', u'OMS')
    runcase_common.runCases(path, u'etfsgychfmy.xlsx', u'OMS')
    runcase_common.runCases(path, u'etfshychfmy.xlsx', u'OMS')
    runcase_common.runCases(path, u'fjzjjmmychfmy.xlsx', u'OMS')
    runcase_common.runCases(path, u'gpmmychfmy.xlsx', u'OMS')
    runcase_common.runCases(path, u'nhgychfmy.xlsx', u'OMS')
    runcase_common.runCases(path, u'pgychfmy.xlsx', u'OMS')
    runcase_common.runCases(path, u'xgsgychfmy.xlsx', u'OMS')

def runcase_commoncase():
    runcase_xianhuo_ychf_my()

if __name__ == '__main__':
    Transferdata()
    time.sleep(3)
    runcase_commoncase()
