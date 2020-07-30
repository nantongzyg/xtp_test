#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import MySQLdb
import time
import random
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import stock_code_black_list


def QueryStructuredFundDB(stkcode, market, security_type,
                          security_status, trade_status, divide_status):
    '''
    分级基金拆分合并查询代码
    :param stkcode: 证券代码，999999表示随机取代码
    :param market: 市场，2-深A， 1-沪A
    :param security_type: 证券类型 ,0表示主板股票
    :param security_status: 证券状态， 2表示正常状态
    :param trade_status: 交易状态， 0表示可正常交易
    :param divide_status: stkprice
    :return:
    '''

    stkprice = {
        '证券代码': None,
    }

    date = time.strftime('%Y%m%d', time.localtime(time.time()))

    if stkcode != '999999':
        sql = '''
                select
                    t1.instrument_id
                from %s t1, %s t2
                where
                  t1.instrument_id = t2.fund_ticker
                and t1.exch_id = %s
                and t1.security_type = %s
                and t1.security_status = %s
                and t1.trade_status = %s
                and t1.instrument_id = %s
                and t2.is_mother_fund = 1
                and t2.divide_status = %s
                ''' % ('xtp_exch_sec_' + date, 'xtp_structured_fund_params_' + date,
                       market, security_type,
                       security_status, trade_status,
                       stkcode, divide_status)
    else:
        sql = '''
                select
                    t1.instrument_id
                from %s t1, %s t2
                where
                  t1.instrument_id = t2.fund_ticker
                and t1.exch_id = %s
                and t1.security_type = %s
                and t1.security_status = %s
                and t1.trade_status = %s
                and t2.is_mother_fund = 1
                and t2.fund_ticker not in %s
                and t2.divide_status = %s
                ''' % ('xtp_exch_sec_' + date, 'xtp_structured_fund_params_' + date,
                       market, security_type,
                       security_status, trade_status,
                       stock_code_black_list, divide_status)

    try:
        conn=connectMysql()
        cur = conn.cursor()
        cur.execute(sql)
        queryPrice = cur.fetchall()
        i=random.randint(0, len(queryPrice)-1)
        stkprice['证券代码'] = queryPrice[i][0]

        cur.close()
        conn.close()

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return stkprice
