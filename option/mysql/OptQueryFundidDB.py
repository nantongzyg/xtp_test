#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from opt_mysql_config import *
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import *

def QueryFundidDB():

    str='select fundid from xtp_user WHERE user_name =\''+CONST_TRADE_USER + '\''
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchall()
    fundid = rs[0][0]
    cur.close()
    conn.close()
    return fundid

def QueryFundidSecuAccDB():

    str= '''
        select
          a.fund_acc,
          max(case b.market when 0 then b.secu_acc end) secu_acc_sz,
          max(case b.market when 1 then b.secu_acc end) secu_acc_sh
        from %s a, %s b, %s c
          where a.fund_acc = c.fundid
        and b.client_id = a.client_id
        and c.user_name = '%s'
        group by a.fund_acc
    ''' % (fund_info, secu_info, xtp_user, CONST_TRADE_USER)
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(str)
    rs = cur.fetchone()
    user_info = {}
    user_info['fund_acc'] = rs[0]
    user_info['secu_acc_sz'] = rs[1]
    user_info['secu_acc_sh'] = rs[2]
    cur.close()
    conn.close()
    return user_info

def QueryFundomsidDB():

    sql = 'select id from xtp_server where ip = "%s" and port = %d'%(CONST_TRADE_IP, CONST_TRADE_PORT)
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchall()
    oms_id = rs[0][0]
    cur.close()
    conn.close()
    if len(rs)==0:
        return None
    else:
        return oms_id
