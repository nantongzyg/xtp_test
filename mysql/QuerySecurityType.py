#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
from mysql_config import *
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import *
date = time.strftime('%Y%m%d', time.localtime(time.time()))

def QuerySecuid(wt_reqs):
    INSTRUMENT_ID=wt_reqs
    abl='select security_type from xtp_exch_sec_' + date + ' WHERE instrument_id = '+INSTRUMENT_ID 
    #str='select security_type from xtp_exch_sec_' + date + ' WHERE instrument_id = 510010' 
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(abl)
    rs = cur.fetchall()
    secuid = rs[0][0]
    cur.close()
    conn.close()
    return secuid
