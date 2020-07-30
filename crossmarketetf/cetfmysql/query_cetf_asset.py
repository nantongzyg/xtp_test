#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from mysql.mysql_config import connectMysql


def query_cetf_asset(stockcode,market, security_type,security_status,
                     trade_status, fundid):
    """
    查询跨市场etf持仓
    :param stockcode: 证券代码
    :param market: 市场
    :param security_type: 证券类型
    :param security_status: 证券状态
    :param trade_status: 交易状态
    :param fundid: 资金账号
    :return:
    """
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    if stockcode == '999999':
        sql = ('SELECT a.stock_code,c.creation_redemption_unit from ' +
               'xtp_stk_asset_' + date + ' a,xtp_exch_sec_' + date +
               ' b,xtp_etf_baseinfo_' + date +
               ' c WHERE a.stock_code=b.instrument_id ' +
               'AND a.stock_code=c.ticker AND b.exch_id=' +
              market + ' AND b.security_type=' + security_type +
               ' and b.security_status=' + security_status +
              ' and b.trade_status=' +trade_status +
               ' AND a.fund_acc=\'' + fundid + '\'')
    else:
        sql = ('SELECT a.stock_code,c.creation_redemption_unit from ' +
               'xtp_stk_asset_' + date + ' a,xtp_exch_sec_' + date +
               ' b,xtp_etf_baseinfo_' + date +
              ' c WHERE a.stock_code=b.instrument_id ' +
              'AND a.stock_code=c.ticker AND b.exch_id=' +
              market + ' AND b.security_type=' + security_type +
               ' and b.security_status=' + security_status +
               ' and a.stock_code = ' + stockcode + ' and b.trade_status=' +
              trade_status + ' AND a.fund_acc=\'' + fundid + '\'')
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchall()
    cur.close()
    conn.close()
    return rs

if __name__ == '__main__':
    print query_cetf_asset('580120','1','14', '2', '0','109180003408')

