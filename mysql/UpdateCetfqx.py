#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
from mysql_config import *
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from QueryFundidDB import *

secu_acc = QueryFundidSecuAccDB()
client_id = QueryCustIdDB()
secu_acc_sz = secu_acc['secu_acc_sz']
secu_acc_sh = secu_acc['secu_acc_sh']

def updateAllFundRightHasP():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_fund_info_'+ date + ' set fund_rights  = \'AWJPMF\',xtp_fund_rights = \'AWJPMF\'    WHERE   client_id = ' + str(client_id)
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()
def updateAllFundRightHasNoP():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_fund_info_'+ date + ' set fund_rights  = \'AWJMF\',xtp_fund_rights = \'AWJMF\'    WHERE   client_id = ' + str(client_id)
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateFundRightHasP():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_fund_info_'+ date + ' set fund_rights  = \'AWPJMF\',xtp_fund_rights = \'AWJMF\'    WHERE   client_id = ' + str(client_id)
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateXtpFundRightHasP():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_fund_info_'+ date + ' set fund_rights  = \'AWJMF\',xtp_fund_rights = \'AWJPMF\'    WHERE   client_id = ' + str(client_id)
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

if __name__ == '__main__':


    updateXtpFundRightHasP()
