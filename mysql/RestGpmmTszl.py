#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
from mysql_config import *
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import *
sys.path.append("/home/yhl2/workspace/xtp_test/utils")
from env_restart import *
def run_tszl():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))

    str='update xtp_exch_sec_'+ date + ' set security_status=10  where security_type = 0 and security_status=2'
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    conn.commit()
    rs = cur.fetchall()
    cur.close()
    conn.close()
    clear_data_and_restart_all()

def run_gpmm():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))

    str='update xtp_exch_sec_'+ date + ' set security_status=2  where security_type = 0 and security_status=10'
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    conn.commit()
    rs = cur.fetchall()
    cur.close()
    conn.close()
    clear_data_and_restart_all()


if __name__ == '__main__':
   
   #run_tszl() 
   run_gpmm()
   
   
