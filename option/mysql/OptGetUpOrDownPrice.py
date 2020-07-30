#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
from opt_mysql_config import *

# ------------------------------------------------------------------------------------------------------------------
# 定义函数：根据证券代码获取涨停价
# ------------------------------------------------------------------------------------------------------------------

today = time.strftime('%Y%m%d', time.localtime(time.time()))

def getUpPrice(stkcode):
    str = '''SELECT
                 a.limitup_px,
                 a.security_type
            FROM %s a
            WHERE a.instrument_id = '%s'
            AND a.security_type != 255
            AND a.trade_status!=255''' % (
        'xtp_opt_exch_sec_' + today, stkcode
    )
    try:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(str)
        rs = cur.fetchall()
        cur.close()
        conn.close()
        #如果查询集合为空，则返回100000
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    if len(rs) == 0:
        return 100000
    else:
        return rs[0][0] / 10000.0



# ------------------------------------------------------------------------------------------------------------------
# 定义函数：根据证券代码获取跌停价
# ------------------------------------------------------------------------------------------------------------------
def getDownPrice(stkcode):
    str = '''SELECT
                 a.limitdown_px,
                 a.security_type
             FROM %s a
             WHERE a.instrument_id = '%s'
             AND a.security_type != 255
             AND a.trade_status!=255''' % (
        'xtp_opt_exch_sec_' + today, stkcode
    )
    try:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(str)
        rs = cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    # 如果查询集合为空，则返回0
    if len(rs) == 0:
        return 0
    else:
        return rs[0][0] / 10000.0

def getcodes():
    str = 'SELECT instrument_id from xtp_exch_sec_' + today + ' a ' \
           'WHERE a.security_type = 0 and a.security_status = 2 and a.trade_status = 0' \
           ' order by instrument_id limit 100'
    # rs1=[]
    try:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(str)
        rs = cur.fetchall()
        # for i in rs:
        #     rs1.append(i[0])
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    # 如果查询集合为空，则返回0
    return rs

# ------------------------------------------------------------------------------------------------------------------
# 定义函数：根据证券类型获取（价格）保留小s数位
# ------------------------------------------------------------------------------------------------------------------
def getDecimalPlaces(security_type):
    i=2
    if security_type in(0,1,2):
        i=2
    elif security_type in(14,15):
        i=3

    return i

