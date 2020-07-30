#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import os
import time
sys.path.append('/home/yhl2/workspace/xtp_test/option/mysql')
import Opt_SqlData_Transfer
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
import runcase_common
from env_restart import *

def Transferdata():
    sqldata = Opt_SqlData_Transfer.Opt_SqlData_Transfer()
    # 普通期权交易
    sqldata.transfer_exercise_date_tomorrow()

def runcase_Option():
    path = '/home/yhl2/workspace/xtp_test/utils'
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'权利方限价_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'权利方市价_沪市')
    runcase_common.runCasesOption(path,  u'个股期权自动化用例.xlsx', u'义务方限价（认购合约）_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'义务方市价（认购合约）_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'义务方限价（认沽合约）_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'义务方市价（认沽合约）_沪市')
def runcase_Option_yz():
    path = '/home/yhl2/workspace/xtp_test/utils'
    runcase_common.runCasesOption(path, u'个股期权自动化用例_验资.xlsx', u'权利方限价_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例_验资.xlsx', u'权利方市价_沪市')
    runcase_common.runCasesOption(path,  u'个股期权自动化用例_验资.xlsx', u'义务方限价（认购合约）_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例_验资.xlsx', u'义务方市价（认购合约）_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例_验资.xlsx', u'义务方限价（认沽合约）_沪市')
    runcase_common.runCasesOption(path, u'个股期权自动化用例_验资.xlsx', u'义务方市价（认沽合约）_沪市')
def runcase_Option_xq():
    path = '/home/yhl2/workspace/xtp_test/utils'
    sqldata = Opt_SqlData_Transfer.Opt_SqlData_Transfer()
    # 行权
    sqldata.transfer_exercise_date_today()
    oms_restart()
    runcase_common.runCasesOption(path, u'个股期权自动化用例.xlsx', u'行权')

if __name__ == '__main__':
    Transferdata()
    #runcase_Option()
    runcase_Option_yz()


