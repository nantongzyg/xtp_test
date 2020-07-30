#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import MySQLdb
import random
import traceback
sys.path.append("/home/yhl2/workspace/xtp_test/service")
import ServiceConfig
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql")
from mfQueryStkCjhbQtyDB import *

ashare_tuple_db = None


#判断程序返回的成交回报记录数和数据库是否一致
def QueryStkCjhbQty(cjhb_count,sqbh,sqbh_cd,case_goal,wt_reqs,Api,*xtp_id_init):
    global ashare_tuple_db
    cjbh_flag = False
    if case_goal['期望状态'] in ('全成','部成'):
        cjhb_count_db = QueryStkCjhbQtyDB(sqbh)
        if cjhb_count_db == cjhb_count:
            cjbh_flag = True
    elif case_goal['期望状态'] == '未成交':
        ashare_tuple_db = QueryStkNoMatchDB(sqbh)
        if ashare_tuple_db == (1,1,0,0):
            cjbh_flag = True
    elif case_goal['期望状态'] == '初始':
        ashare_tuple_db = QueryStkInitDB(xtp_id_init)
        if ashare_tuple_db == (1, 0, 0, 0):
            cjbh_flag = True
    elif case_goal['期望状态'] == '部撤':
        ashare_tuple_db = QueryStkPartCanceledDB(sqbh,sqbh_cd)
        if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL']:
            if ashare_tuple_db == (1,1,1,0):
                cjbh_flag = True
        else:
            if ashare_tuple_db == (2, 2, 1, 0):
                cjbh_flag = True
    elif case_goal['期望状态'] == '已撤':
        ashare_tuple_db = QueryStkAllCanceledDB(sqbh,sqbh_cd)
        #价格条件为'五档转撤'时，撤单返回一条数据，其余类型返回两条
        if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL']:
            if ashare_tuple_db == (1,1,0,0):
                cjbh_flag = True
        else:
            if ashare_tuple_db == (2, 2, 0, 0):
                cjbh_flag = True
    return cjbh_flag