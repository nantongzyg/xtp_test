#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import os
import time
sys.path.append('/home/yhl2/workspace/xtp_test/mysql')
import SqlData_Transfer
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/RESTART')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/GPMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/KZZMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ETFMM_D')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ETFMM_K')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/FJZJJMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/IPO')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ReverseRepo')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/AllotmentPayment')
sys.path.append('/home/yhl2/workspace/xtp_test/run')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/KCB_YCHF/KCB_YCHF_MM/OMS')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/KCB_YCHF/KCB_YCHF_IPO')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/KCB_YCHF/KCB_YCHF_AllotmentPayment')

import runcase_common
import runcase_ipo
import runcase_allPayment



#将测试数据导入到mc-test当日库
def Transferdata():

    sqldata = sqldata = SqlData_Transfer.SqlData_Transfer()
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
    runcase_common.runCases(path,  u'普通业务自动化用例冒烟测试.xlsx',u'深圳限价')
    runcase_common.runCases(path, u'普通业务自动化用例冒烟测试.xlsx', u'深圳市价')

def runcase_SZ_ETFMMD():
    runcase_common.runCases(path, u'ETF买卖冒烟测试.xlsx', u'深圳限价单市场')
    runcase_common.runCases(path, u'ETF买卖冒烟测试.xlsx', u'深圳市价单市场')

def runcase_SZ_ETFMMK():
    runcase_common.runCases(path, u'ETF买卖冒烟测试.xlsx', u'深圳限价跨市场')
    runcase_common.runCases(path, u'ETF买卖冒烟测试.xlsx', u'深圳市价跨市场')

def runcase_SZ_FJZJJMM():
    #runcase_common.runCases(path, u'普通业务自动化用例冒烟测试.xlsx', u'分级子基金深圳限价')
    runcase_common.runCases(path, u'普通业务自动化用例冒烟测试.xlsx', u'分级子基金深圳市价')

def runcase_SZ_ReverseRepo():
    runcase_common.runCases(path, u'普通业务自动化用例冒烟测试.xlsx', u'逆回购_深圳')

def runcase_SZ_IPO():
    runcase_ipo.runCases(path, u'普通业务自动化用例冒烟测试.xlsx', u'新股申购_深圳')

def runcase_SZ_AllotmentPayment():
    runcase_allPayment.runCases(path, u'普通业务自动化用例冒烟测试.xlsx', u'配股缴款_深圳')

def runcase_SH_GPMM():
    runcase_common.runCases(path,  u'普通业务自动化用例冒烟测试.xlsx',u'上海限价')
    runcase_common.runCases(path, u'普通业务自动化用例冒烟测试.xlsx', u'上海市价')

def runcase_SH_ETFMMD():
    runcase_common.runCases(path, u'ETF买卖冒烟测试.xlsx', u'上海限价单市场')
    runcase_common.runCases(path, u'ETF买卖冒烟测试.xlsx', u'上海市价单市场')


def runcase_SH_ETFMMK():
    runcase_common.runCases(path, u'ETF买卖冒烟测试.xlsx', u'上海限价跨市场')
    runcase_common.runCases(path, u'ETF买卖冒烟测试.xlsx', u'上海市价跨市场')


def runcase_SH_ReverseRepo():
    runcase_common.runCases(path, u'普通业务自动化用例冒烟测试.xlsx', u'逆回购_上海')


def runcase_SH_IPO():
    runcase_ipo.runCases(path, u'普通业务自动化用例冒烟测试.xlsx', u'新股申购_上海')


def runcase_SH_AllotmentPayment():
    runcase_allPayment.runCases(path, u'普通业务自动化用例冒烟测试.xlsx', u'配股缴款_上海')

# 科创板冒烟_买卖
def runcase_KCB_MM():
    os.system('sh /home/yhl2/workspace/xtp_test/Autocase_Result/KCB_MM/test_my.sh')

# 科创板冒烟_新股申购
def runcase_KCB_IPO():
    os.system('sh /home/yhl2/workspace/xtp_test/Autocase_Result/KCB_IPO/test.sh')

# 科创板异常恢复_配股缴款
def runcase_KCB_AllotmentPayment():
    os.system('sh /home/yhl2/workspace/xtp_test/Autocase_Result/KCB_AllotmentPayment/test.sh')

def runcase_SH_KZZMM():
    runcase_common.runCases(path, u'kzzmy_ychf.xlsx', u'上海限价')

def runcase_SZ_KZZMM():
    runcase_common.runCases(path, u'kzzmy_ychf.xlsx', u'深圳限价')

def runcase_allcommon():
    runcase_SZ_GPMM()
    time.sleep(2)
    runcase_SZ_KZZMM()
    time.sleep(2)
    runcase_SZ_ETFMMD()
    time.sleep(2)
    runcase_SZ_ETFMMK()
    time.sleep(2)
    runcase_SZ_IPO()
    time.sleep(2)
    runcase_SZ_AllotmentPayment()
    time.sleep(2)
    runcase_SH_GPMM()
    time.sleep(2)
    runcase_SH_ETFMMD()
    time.sleep(2)
    runcase_SH_ETFMMK()
    time.sleep(2)
    runcase_SH_IPO()
    time.sleep(2)
    runcase_SH_AllotmentPayment()
    time.sleep(2)
    runcase_SH_ReverseRepo()
    time.sleep(2)
    runcase_SZ_ReverseRepo()
    time.sleep(2)
    runcase_KCB_MM()
    time.sleep(2)
    runcase_KCB_IPO()
    time.sleep(2)
    runcase_KCB_AllotmentPayment()
    time.sleep(4)
    os.system('sh /home/yhl2/workspace/xtp_test/Autocase_Result/RESTART/test.sh')

if __name__ == '__main__':
    #Transferdata()
    time.sleep(3)
    runcase_allcommon()
