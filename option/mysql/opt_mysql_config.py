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

# 数据库相关表
in_exch_db = 'xtp_opt_exch_sec_auto'
out_exch_db = 'xtp_opt_exch_sec_' + today

in_fund_asset_db = 'xtp_opt_fund_asset_auto'
out_fund_asset_db = 'xtp_opt_fund_asset_' + today

in_stk_db = 'xtp_opt_stk_asset_auto'
out_stk_db = 'xtp_opt_stk_asset_' + today

fund_info = 'xtp_opt_fund_info_' + today

secu_info = 'xtp_opt_secu_info_' + today

xtp_user = 'xtp_user'

in_cur_risk = 'xtp_cur_risk_auto'
out_cur_risk = 'xtp_cur_risk'

opt_cntrt_info = 'xtp_opt_cntrt_info_' + today

cur_fee_rate = 'xtp_cur_fee_rate'

out_rights_issue_params = 'xtp_rights_issue_params_' + today

#连接数据库配置
def connectMysql():
    # conn=MySQLdb.connect(host='10.33.33.5',user='xtp1',passwd='123456',db='xtp1222',port=3306)
    # conn = MySQLdb.connect(host='10.26.134.181', user='mc-test',
    #                        passwd='mc-test', db='option_test', port=3306)
    conn = MySQLdb.connect(host='10.29.193.60', user='root',
                           passwd='123456', db='xtp2', port=3306)
    # conn = MySQLdb.connect(host='10.25.24.46', user='xtp1',
    #                       passwd='123456', db='xtp1', port=3306)
    #conn = MySQLdb.connect(host='10.29.182.38', user='root',
    #                       passwd='123456', db='xtp5', port=3306)
    return conn

def connectMssql():
    db_ashare = 'sse' + str(CONST_TRADE_PORT)[-1:]
    print db_ashare
    if db_ashare == 'sse' + ssenum:
        return False
    conn = pymssql.connect(host='10.29.193.60', user='sa', password='123456', database=db_ashare, port=1433)
    return conn



