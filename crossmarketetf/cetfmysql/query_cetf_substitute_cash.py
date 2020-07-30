#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from mysql.mysql_config import connectMysql

date = time.strftime('%Y%m%d', time.localtime(time.time()))


def query_creation_redemption_subcash(etf_code1):
    """查询同市场成分股必须现金替代时，申赎或赎回需要的总金额"""
    sql = ('SELECT ' +
          ' case when sum(creation_cash_substitute) is null then 0' +
          '   else sum(creation_cash_substitute) end as sum_creation_cash,' +
          ' case when sum(redemption_cash_substitute) is null then 0'
          '   else sum(redemption_cash_substitute) end as sum_redemption_cash' +
          ' from xtp_etf_components_' + date +
          ' where etf_code1 = ' + etf_code1 +
          ' and substitute_flag = 2')
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        code_rs = {}
        if rs is not ():
            code_rs['creation_cash_substitute'] = rs[0][0]
            code_rs['redemption_cash_substitute'] = rs[0][1]
    return code_rs

def query_crossmakert_sub_cash(etf_code1):
    """查询跨市场etf申赎或赎回时，跨市场成分股（退补现金替代 + 必须现金替代）需要的总金额
    """
    sql1 = ('SELECT ' +
          'case when sum(creation_cash_substitute * (1 + premium_ratio/100000))'
          + 'is null then 0' +
          '   else sum(creation_cash_substitute * (1 + premium_ratio/100000)) '
          + 'end as sum_creation_cash, ' +
          'case when sum(redemption_cash_substitute * (1 - premium_ratio/100000))'
          + ' is null then 0 ' +
          '  else sum(redemption_cash_substitute * (1 - premium_ratio/100000)) '
          + 'end as sum_redemption_cash' +
          ' from xtp_etf_components_' + date +
          ' where etf_code1 = ' + etf_code1 +
          ' and substitute_flag = 3')
    sql2 = ('SELECT ' +
          ' case when sum(creation_cash_substitute) is null then 0' +
          '   else sum(creation_cash_substitute) end as sum_creation_cash,' +
          ' case when sum(redemption_cash_substitute) is null then 0' +
          '   else sum(redemption_cash_substitute) end as sum_redemption_cash' +
          ' from xtp_etf_components_' + date +
          ' where etf_code1 = ' + etf_code1 +
          ' and substitute_flag = 4')
    conn = connectMysql()
    with conn:
        cur = conn.cursor()
        # 退补现金替代部分
        cur.execute(sql1)
        rs1 = cur.fetchall()
        code_rs1 = [0, 0]
        if rs1:
            code_rs1[0] = rs1[0][0]
            code_rs1[1] = rs1[0][1]
        # 必须现金替代部分
        cur.execute(sql2)
        rs2 = cur.fetchall()
        code_rs2 = [0,0]
        if rs2:
            code_rs2[0] = rs2[0][0]
            code_rs2[1] = rs2[0][1]
        # 退补现金替代部分 + 必须现金替代部分
        rs = [code_rs1[i] + code_rs2[i] for i in range(2)]
        code_rs = {}
        if sum(rs) != 0:
            code_rs['creation_cash_substitute'] = rs[0]
            code_rs['redemption_cash_substitute'] = rs[1]
    return code_rs

if __name__ == '__main__':
    print query_creation_redemption_subcash('550161')
    print query_crossmakert_sub_cash('550161')
