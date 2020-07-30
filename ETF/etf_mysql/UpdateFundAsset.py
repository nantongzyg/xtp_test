#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


def UpdateFundAsset(fund_amount,fund_acc):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    str_sql = 'update xtp_fund_asset_' + date + \
              ' set fund_avl_bal = "' + str(fund_amount) + \
              '", fund_bal = "' + str(fund_amount) + \
          '" where fund_acc = "' + str(fund_acc) + '"'
    conn = connectMysql()
    cur = conn.cursor()
    res = cur.execute(str_sql)
    conn.commit()
    cur.close()
    conn.close()