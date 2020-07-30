#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import pymssql
import sys
import datetime
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import CONST_TRADE_PORT

today = datetime.date.today()
today = today.strftime('%Y%m%d')
# today = '20171211'

# 数据库相关表
in_exch_db = 'xtp_exch_sec_auto'
out_exch_db = 'xtp_exch_sec_' + today

in_fund_asset_db = 'xtp_fund_asset_auto'
out_fund_asset_db = 'xtp_fund_asset_' + today

in_stk_db = 'xtp_stk_asset_auto'
out_stk_db = 'xtp_stk_asset_' + today

fund_creation = 'xtp_fund_creation_' + today

fund_info = 'xtp_fund_info_' + today

secu_info = 'xtp_secu_info_' + today

xtp_user = 'xtp_oms_user'

in_etf_baseinfo = 'xtp_etf_baseinfo_auto'
out_etf_baseinfo = 'xtp_etf_baseinfo_' + today

in_etf_components = 'xtp_etf_components_auto'
out_etf_components = 'xtp_etf_components_' + today

in_issue_params = 'xtp_issue_params_auto'
out_issue_params = 'xtp_issue_params_' + today

in_rights_issue_params = 'xtp_rights_issue_params_auto'
out_rights_issue_params = 'xtp_rights_issue_params_' + today

in_cur_risk = 'xtp_cur_risk_auto'
out_cur_risk = 'xtp_cur_risk'

in_fund_creation = 'xtp_fund_creation_auto'
out_fund_creation = 'xtp_fund_creation_' + today

in_structured_fund_params = 'xtp_structured_fund_params_auto'
out_structured_fund_params = 'xtp_structured_fund_params_' + today

cur_fee_rate = 'xtp_cur_fee_rate'

#连接数据库配置
def connectMysql():
    # conn=MySQLdb.connect(host='10.33.33.5', user='xtp1',
    #                      passwd='123456', db='xtp1to18', port=3306)
    #conn = MySQLdb.connect(host='10.25.24.194', user='mc-test',
    #                       passwd='mc-test', db='mc-test', port=3306)
    conn = MySQLdb.connect(host='10.29.193.60', user='root',
                           passwd='123456', db='xtp2', port=3306)
    #conn = MySQLdb.connect(host='10.29.182.38', user='root',
    #                        passwd='123456', db='xtp5', port=3306)
    return conn

"""def connectMssql():
    if str(CONST_TRADE_PORT)[-2] == '0':
        ssenum = str(CONST_TRADE_PORT)[-1:]
    else:
        ssenum = str(CONST_TRADE_PORT)[-2:]
    db_ashare = 'sse' + ssenum
    if db_ashare == 'sse':
        return False
    conn = pymssql.connect(host='10.26.134.195', user='root', password='123456', database=db_ashare, port=1435)
    return conn
"""
def connectMssql():
    if str(CONST_TRADE_PORT)[-2] == '0':
        ssenum = str(CONST_TRADE_PORT)[-1:]
    else:
        ssenum = str(CONST_TRADE_PORT)[-2:]
    db_ashare = 'sse' + ssenum
    if db_ashare == 'sse':
        return False
    conn = pymssql.connect(host='10.29.193.64', user='sa', password='123456', database=db_ashare, port=1433)
    #conn = pymssql.connect(host='10.26.134.195 ', user='root', password='123456', database=db_ashare, port=1435)
    return conn
