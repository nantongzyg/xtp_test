#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
from opt_mysql_config import *


currentDate = time.strftime('%Y%m%d', time.localtime(time.time()))

def queryTgtPreclose(ticker):
    """查询期权标的昨收价"""
    sql = '''
            SELECT
                a.preclose_px
            FROM xtp_exch_sec_%s a
            join xtp_opt_cntrt_info_%s b
            on a.instrument_id = b.tgt_stk_code
            WHERE b.cntrt_id = "%s"''' % (currentDate, currentDate, ticker)

    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchone()
    cur.close()
    conn.close()
    return rs[0]/10000.0
