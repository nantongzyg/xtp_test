#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import *

def getSecurityType(stkcode):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str = 'SELECT a.security_type from xtp_exch_sec_' + date + ' a WHERE a.instrument_id =' + stkcode + ' AND a.security_type != 255 and a.trade_status!=255'
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchall()
    cur.close()
    conn.close()
    if len(rs)==0:
       return None
    else:
        return rs[0][0]
