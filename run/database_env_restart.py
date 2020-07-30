#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/27 15:39
# @Author : LJY
# @Brief :
# @File : database_env_restart.py
# @PROJECT_NAME : xtp_test
# @Software: PyCharm
import sys
import getpass

linux_username = getpass.getuser()
#sys.path.append('/home/' + linux_username + '/workspace/xtp_test/run')
#from runcase_common import Transferdata

sys.path.append('/home/' + linux_username + '/workspace/xtp_test/mysql')
from mysql_config import *
import datetime
sys.path.append('/home/' + linux_username + '/workspace/xtp_test/utils')
from env_restart import *

def Init_database():
    today = datetime.date.today()
    today = today.strftime('%Y%m%d')
    # print "run  today",today
    sql = "rename table "
    Flag = False
    all_table_tuple = Get_all_table_name()
    for item in all_table_tuple:
        for item1 in item:
            if len(item1) > 8 and item1[-8:-4] == "2020" and item1[-8:] != today:
                sql = sql + item1 + " to " + item1[:-8] + today + ","
                Flag = True
    sql = sql[:-1] + ";" if Flag else ""
    if sql != "":
        conn = connectMysql()
        cur = conn.cursor()
        try:
            # print "sql",sql
            cur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        finally:
            cur.close()
            # 关闭连接
            conn.close()
        print "列表后缀日期不等于当天日期，数据库初始化日期表完成"
    else:
        print "列表后缀日期等于当天日期，数据库无需初始化日期表!!!!!!!!!"


def Get_all_table_name():
    all_table_name_tuple = {}
    conn = connectMysql()
    cur = conn.cursor()
    try:
        cur.execute('SHOW TABLES')
        all_table_name_tuple = cur.fetchall()
    except:
        conn.rollback()
    finally:
        cur.close()
        # 关闭连接
        conn.close()
        return all_table_name_tuple

def Trade_day_alte():
    today = datetime.date.today().strftime('%Y%m%d')
    trade_table_sql = 'insert into xtp_trade_day(id,trade_day) values(1,%s)' % int(today)
    commond = []
    commond.append('truncate table xtp_trade_day ')
    commond.append(trade_table_sql)
    for sql in commond:
        conn = connectMysql()
        cur = conn.cursor()
        try:
            # print "sql",sql
            cur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        finally:
            cur.close()
            # 关闭连接
            conn.close()



if __name__ == '__main__':
    Init_database()
    Trade_day_alte()
    clear_data_and_restart_all()
    #Transferdata()
    print "数据库、组件初始化重启完成"
