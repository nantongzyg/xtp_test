#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
from mysql_config import *
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import *

def InsertTick1DB(tick_list):

    try:
        conn = connectMysql()
        cur = conn.cursor()
        for tick in tick_list:
            sql_str = "insert into tick1(ticker,pricetick) values('" + str(tick['ticker']) + "','"+ str(tick['price_tick']) +"')"
            cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def InsertTick2DB(tick_list):
    try:
        conn = connectMysql()
        cur = conn.cursor()
        for tick in tick_list:
            ticker = tick['ticker'].strip()
            sql_str = "insert into tick2(ticker,pricetick) values('" + ticker + "','"+ str(tick['price_tick']) +"')"
            cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()