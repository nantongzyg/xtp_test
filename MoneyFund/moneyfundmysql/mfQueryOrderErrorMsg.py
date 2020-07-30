#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *

def queryOrderErrorMsg(error_code):
    str = 'select error_msg from order_error_info where error_code = %d' % (error_code)
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs[0]
