#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import MySQLdb
import time
import random
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


# 查询xtp_mrcommon_fjjj，取最新一条
def QueryMrcommFjjj():
    sql = 'select send_flag, appl_id, memo' \
          ' from xtp_mrcomm_fjjj order by recv_time desc limit 1'
    mrcommon_dict = {}
    try:
        conn=connectMysql()
        cur = conn.cursor()
        cur.execute(sql)
        queryPrice = cur.fetchall()
        mrcommon_dict['send_flag'] = queryPrice[0][0]
        mrcommon_dict['appl_id'] = queryPrice[0][1]
        mrcommon_dict['memo'] = queryPrice[0][2]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return mrcommon_dict
