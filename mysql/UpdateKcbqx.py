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


def updateSecuRightHasAll():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'@\' ,xtp_secu_rights  =  \'@\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sh + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()
    #clear_data_and_restart_all()

def updateSecuRightHas1ShBefore():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'WJMF1\' ,xtp_secu_rights  =  \'WJMF\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sh + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHas1ShAfter():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'WJMF\' ,xtp_secu_rights  =  \'WJMF1\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sh + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHas1Sh():
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


def updateSecuRightHasNo1Sh():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'JMFW\' ,xtp_secu_rights  =  \'JMFW\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sh + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateFundRightHas1():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_fund_info_'+ date + ' set fund_rights  = \'A1JXMF\',xtp_fund_rights = \'A1JXMF\'    WHERE   client_id = ' + str(client_id)
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateFundRightHasNo1():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_fund_info_'+ date + ' set fund_rights  = \'AJXMF\',xtp_fund_rights = \'AJXMF\'    WHERE   client_id = ' + str(client_id)
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

if __name__ == '__main__':
    updateSecuRightHas1()
    #updateSecuRightHasNo1()
    #updateFundRightHasNo1()
    #updateFundRightHas1()
