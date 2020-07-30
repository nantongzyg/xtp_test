#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
from opt_mysql_config import *
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import *

def QueryAllotmentStkInfoDB(fundacc,market):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = ("SELECT t1.ticker FROM xtp_rights_issue_params_" + date + " t1"
                    " INNER JOIN xtp_stk_asset_" + date + " t2"
                      " ON t1.ticker = t2.stock_code"
                    " WHERE t2.fund_acc = '" + fundacc + "'"
                        "AND t1.exch_id = " + market + " order by rand()")
        cur.execute(sql_str)
        conn.commit()
        rs = cur.fetchall()
        ticker_list = []
        for i in rs:
            ticker_list.append(i)
        return ticker_list
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def QueryAllotmentStkPrice(stkcode):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = "SELECT issue_price/10000 FROM xtp_rights_issue_params_" + date + " where ticker = " + stkcode
        cur.execute(sql_str)
        conn.commit()
        rs = cur.fetchone()
        return float(rs[0])
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()