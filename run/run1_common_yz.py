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
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ETFMM_K')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/FJZJJMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/IPO')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/ReverseRepo')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/AllotmentPayment')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/XjShHBJJMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/SjShHBJJMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/KZZMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/MEDIUM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/GEM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/GEM_REGISTER')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/FXJSMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/TSZLMM')

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
    runcase_common.runCases(path,  u'普通业务自动化用例_验资.xlsx',u'深圳限价')
    runcase_common.runCases(path, u'普通业务自动化用例_验资.xlsx', u'深圳市价')

def runcase_SZ_ETFMMD():
    runcase_common.runCases(path, u'ETF买卖_验资.xlsx', u'深圳限价单市场')
    runcase_common.runCases(path, u'ETF买卖_验资.xlsx', u'深圳市价单市场')

def runcase_SZ_ETFMMK():
    runcase_common.runCases(path, u'ETF买卖_验资.xlsx', u'深圳限价跨市场')
    runcase_common.runCases(path, u'ETF买卖_验资.xlsx', u'深圳市价跨市场')

def runcase_SZ_FJZJJMM():
    runcase_common.runCases(path, u'普通业务自动化用例_验资.xlsx', u'分级子基金深圳限价')
    runcase_common.runCases(path, u'普通业务自动化用例_验资.xlsx', u'分级子基金深圳市价')

def runcase_SZ_ReverseRepo():
    runcase_common.runCases(path, u'普通业务自动化用例_验资.xlsx', u'逆回购_深圳')

def runcase_SZ_IPO():
    runcase_ipo.runCases(path, u'普通业务自动化用例_验资.xlsx', u'新股申购_深圳')

def runcase_SZ_AllotmentPayment():
    runcase_allPayment.runCases(path, u'普通业务自动化用例_验资.xlsx', u'配股缴款_深圳')

def runcase_SZ_KZZMM():
    runcase_common.runCases(path, u'kzz_验资.xlsx', u'深圳限价')

#创业板
def runcase_SZ_GEM():
    runcase_common.runCases(path, u'gem.xlsx',u'深圳限价_验资')
    runcase_common.runCases(path, u'gem.xlsx', u'深圳市价_验资')
	
#创业板注册制
def runcase_SZ_GEM_REGISTER():
    runcase_common.runCases(path, u'gem.xlsx',u'深圳限价_验资')
    runcase_common.runCases(path, u'gem.xlsx', u'深圳市价_验资')
	
#风险警示
def runcase_SZ_FXJSMM():
    runcase_common.runCases(path, u'fxjsmm.xlsx',u'深圳限价_验资')
	
#退市整理
def runcase_SZ_TSZLMM():
    runcase_common.runCases(path, u'tszlmm.xlsx',u'深圳限价_验资')

#中小板
def runcase_SZ_MEDIUM():
    runcase_common.runCases(path, u'mediumm.xlsx',u'深圳限价_验资')
    runcase_common.runCases(path, u'mediumm.xlsx', u'深圳市价_验资')
#退市整理
def runcase_SH_TSZLMM():
    runcase_common.runCases(path, u'tszlmm.xlsx',u'上海限价_验资')

#风险警示
def runcase_SH_FXJSMM():
    runcase_common.runCases(path, u'fxjsmm.xlsx', u'上海限价_验资')

def runcase_SH_GPMM():
    runcase_common.runCases(path,  u'普通业务自动化用例_验资.xlsx',u'上海限价')
    runcase_common.runCases(path, u'普通业务自动化用例_验资.xlsx', u'上海市价')


def runcase_SH_ETFMMD():
    runcase_common.runCases(path, u'ETF买卖_验资.xlsx', u'上海限价单市场')
    runcase_common.runCases(path, u'ETF买卖_验资.xlsx', u'上海市价单市场')


def runcase_SH_ETFMMK():
    runcase_common.runCases(path, u'ETF买卖_验资.xlsx', u'上海限价跨市场')
    runcase_common.runCases(path, u'ETF买卖_验资.xlsx', u'上海市价跨市场')


def runcase_SH_ReverseRepo():
    runcase_common.runCases(path, u'普通业务自动化用例_验资.xlsx', u'逆回购_上海')


def runcase_SH_IPO():
    runcase_ipo.runCases(path, u'普通业务自动化用例_验资.xlsx', u'新股申购_上海')


def runcase_SH_AllotmentPayment():
    runcase_allPayment.runCases(path, u'普通业务自动化用例_验资.xlsx', u'配股缴款_上海')

def runcase_SH_HBJJ():
    runcase_common.runCases(path, u'普通业务自动化用例_验资.xlsx', u'交易型货币基金买卖上海限价')
    runcase_common.runCases(path, u'普通业务自动化用例_验资.xlsx', u'交易型货币基金买卖上海市价')

def runcase_SH_KZZMM():
    runcase_common.runCases(path, u'kzz_验资.xlsx', u'上海限价')

def runcase_commoncase():
    #runcase_SZ_GPMM()
    #runcase_SZ_ETFMMD()
    #runcase_SZ_ETFMMK()
    #runcase_SZ_IPO()
    #runcase_SZ_AllotmentPayment()
    #runcase_SZ_ReverseRepo()
    #runcase_SZ_GEM()
    runcase_SZ_GEM_REGISTER()
    #runcase_SZ_FXJSMM()
    #runcase_SZ_TSZLMM()
    #runcase_SZ_MEDIUM()
   # ---------市场分割线----------
    #runcase_SH_GPMM()
    #runcase_SH_ETFMMD()
    #runcase_SH_ETFMMK()
    #runcase_SH_HBJJ()
    #runcase_SH_IPO()
    #runcase_SH_AllotmentPayment()
    #runcase_SH_ReverseRepo()
    #runcase_SH_TSZLMM()
    #runcase_SH_FXJSMM()

#风险警示
#def runcase_SH_FXJSMM():


if __name__ == '__main__':
    #Transferdata()
    runcase_commoncase()
