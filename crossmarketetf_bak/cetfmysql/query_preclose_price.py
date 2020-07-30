#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from mysql.mysql_config import *

date = time.strftime('%Y%m%d', time.localtime(time.time()))

def query_preclose_price(stkcode):
    """
    获取股票昨收价
    :param stkcode:股票代码
    :return: Decimal('9.4400')
    """
    sql = ('SELECT a.preclose_px/10000 from xtp_exch_sec_'
          + date + ' a WHERE a.instrument_id =' +
          stkcode + ' AND a.security_type != 255 and a.trade_status!=255')
    preclose_price = 0
    try:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchone()
        preclose_price = rs[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return preclose_price

def query_compnents_preclose_price(etfcode):
    """
    获取etf所有成分股昨收价
    :param etfcode: etf二级市场代码
    :return: {code1:price1, code2:price2, code3:price3, ...}
    """
    sql = ('SELECT'
                ' c.instrument_id,'
                ' c.preclose_px/10000'
           ' FROM'
               ' xtp_etf_baseinfo_' + date + ' a'
           ' JOIN xtp_etf_components_' + date + ' b on'
               ' a.etf_code1 = b.etf_code1'
           ' JOIN xtp_exch_sec_' + date + ' c on'
               ' b.underlying_instrument_id = c.instrument_id'
           ' WHERE a.ticker = ' + etfcode +
           ' AND b.exch_id = c.exch_id'
           ' AND c.security_type != 255 and c.trade_status!=255')
    components_precloseprices = {}
    try:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(sql)
        components_precloseprice = cur.fetchall()
        for rs in components_precloseprice:
            components_precloseprices[rs[0]] = float(rs[1])
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return components_precloseprices

if __name__ == '__main__':
    print repr(query_preclose_price('600000'))
