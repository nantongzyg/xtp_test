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

def updateSecuRightHasJSz():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'WJXMF\' ,xtp_secu_rights  =  \'WJXMF\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sz + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHasJSh():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'WJMF1\' ,xtp_secu_rights  =  \'WJMF1\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sh + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()
    #clear_data_and_restart_all()


def updateSecuRightHasNoJSz():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'WXMF \' ,xtp_secu_rights  =  \'WXMF \'  WHERE   client_id ='+ str(client_id)+ ' and secu_acc =  \'' + secu_acc_sz + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHasNoJSh():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'WMF1\' ,xtp_secu_rights  =  \'WMF1\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sh + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateFundRightHasJ():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_fund_info_'+ date + ' set fund_rights  = \'AWJXMF\',xtp_fund_rights = \'AWJXMF\'    WHERE   client_id = ' + str(client_id)
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()
def updateFundRightHasNoJ():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_fund_info_'+ date + ' set fund_rights  = \'AWXMF\',xtp_fund_rights = \'AWXMF\'    WHERE   client_id = ' + str(client_id)
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

if __name__ == '__main__':
    updateSecuRightHasJ()
    #updateSecuRightHasNoJ()
    #updateFundRightHasNoJ()
    #updateFundRightHasJ()
