#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
from opt_mysql_config import *


date = time.strftime('%Y%m%d', time.localtime(time.time()))


def QueryStkpriceDB(stkcode, market, security_type,
                    security_status, trade_status, call_or_put):
    '''
    :param stkcode: 当stkcode＝’999999‘时，会随机返回符合市场和证券类型要求证券代码
    :param market: '1' 为上Ａ，‘２’为深Ａ
    :param security_type: 30为期权
    :param security_status: 证券状态
    :param trade_status: 交易状态
    :return:
    '''

    stkprice = {
        '证券代码': None,
        '昨收盘价': None,
        '涨停价': None,
        '跌停价': None,
        '随机中间价': None
    }
    # 保留精度
    j=4

    if call_or_put == '*':
        call_or_put1 = 'C'
        call_or_put2 = 'P'
    else:
        call_or_put1 = call_or_put
        call_or_put2 = call_or_put

    # *表示所有期权
    if security_type == '*':
        if stkcode != '999999':
            sql = """select
                        instrument_id,
                        preclose_px,
                        limitup_px,
                        limitdown_px
                     from
                         %s a, %s b
                    where a.instrument_id = b.cntrt_id
                    and (b.call_or_put = '%s' or b.call_or_put = '%s')
                    and a.exch_id = %s
                    and a.trade_status = %s
                    and a.security_status = %s
                    and a.instrument_id = '%s'""" % (
                'xtp_opt_exch_sec_' + date, 'xtp_opt_cntrt_info_' + date, call_or_put1,
                call_or_put2, market, trade_status, security_status, stkcode
            )
        else:
            sql = """select
                        instrument_id,
                        preclose_px,
                        limitup_px,
                        limitdown_px
                     from
                        %s a, %s b
                    where a.instrument_id = b.cntrt_id
                     and (b.call_or_put = '%s' or b.call_or_put = '%s')
                     and a.exch_id = %s
                     and a.trade_status = %s
                     and a.security_status = %s
                     order by rand()""" % (
                'xtp_opt_exch_sec_' + date, 'xtp_opt_cntrt_info_' + date, call_or_put1,
                call_or_put2, market, trade_status, security_status
            )
    else:
        if stkcode != '999999':
            sql = """select
                        instrument_id,
                        preclose_px,
                        limitup_px,
                        limitdown_px
                     from
                         %s a, %s b
                    where a.instrument_id = b.cntrt_id
                     and (b.call_or_put = '%s' or b.call_or_put = '%s')
                     and a.exch_id = %s
                     and a.trade_status = %s
                     and a.security_status = %s
                     and a.security_type = %s
                     and a.instrument_id = '%s'""" % (
                'xtp_opt_exch_sec_' + date, 'xtp_opt_cntrt_info_' + date, call_or_put1,
                call_or_put2, market, trade_status, security_status, security_type, stkcode
            )
        else:
            sql = """select
                        instrument_id,
                        preclose_px,
                        limitup_px,
                        limitdown_px
                     from
                         %s a, %s b
                    where a.instrument_id = b.cntrt_id
                     and (b.call_or_put = '%s' or b.call_or_put = '%s')
                     and a.exch_id = %s
                     and a.trade_status = %s
                     and a.security_status = %s
                     and a.security_type = %s
                     order by rand()""" % (
                'xtp_opt_exch_sec_' + date, 'xtp_opt_cntrt_info_' + date, call_or_put1,
                call_or_put2, market, trade_status, security_status, security_type
            )

    try:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(sql)
        queryPrice = cur.fetchone()
        stkprice['证券代码'] = queryPrice[0]

        stkprice['昨收盘价']=round(float(queryPrice[1]) / 10000, j)

        stkprice['涨停价'] = round(float(queryPrice[2]) / 10000, j)

        stkprice['跌停价'] = round(float(queryPrice[3]) / 10000, j)

        #---随机中间价--
        random_price= random.randint(queryPrice[3], queryPrice[2])
        stkprice['随机中间价'] = round(float(random_price) / 10000, j)

        cur.close()
        conn.close()

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return stkprice
