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

def updateSecuRightHasJXSz():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'JX\' ,xtp_secu_rights  =  \'JX\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sz + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHasJXMSz():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'JXM\' ,xtp_secu_rights  =  \'JXM\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sz + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHas3JSz():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'3J\' ,xtp_secu_rights  =  \'3J\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sz + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHas3JMSz():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'3JM\' ,xtp_secu_rights  =  \'3JM\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sz + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHasJSz():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'J\' ,xtp_secu_rights  =  \'J\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sz + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHasJMSz():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'JM\' ,xtp_secu_rights  =  \'JM\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sz + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHasXSz():
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

def updateSecuRightHasXSh():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'WJXF1\' ,xtp_secu_rights  =  \'WJXF1\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sh + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()
    #clear_data_and_restart_all()


def updateSecuRightHasNoXSz():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'JMWF \' ,xtp_secu_rights  =  \'JMWF \'  WHERE   client_id ='+ str(client_id)+ ' and secu_acc =  \'' + secu_acc_sz + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSecuRightHasNoXSh():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_secu_info_'+ date + ' set secu_rights  =  \'JWF1\' ,xtp_secu_rights  =  \'JWF1\'  WHERE   client_id ='+ str(client_id) + ' and secu_acc =  \'' + secu_acc_sh + '\''
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateFundRightHasX():
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
def updateFundRightHasNoX():
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

def updateSetInvTy1():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_fund_info_'+ date + ' set invest_type  = 1    WHERE   client_id = '+ str(client_id)
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

def updateSetInvTy0():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        conn = connectMysql()
        cur = conn.cursor()
        sql_str = 'UPDATE xtp_fund_info_'+ date + ' set invest_type  = 0    WHERE   client_id = '+ str(client_id)
        print(sql_str)
        cur.execute(sql_str)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

if __name__ == '__main__':
    updateSecuRightHasJXSz()
    #updateSecuRightHasX()
    #updateSecuRightHasNoX()
    #updateFundRightHasNoX()
    #updateFundRightHasX()
