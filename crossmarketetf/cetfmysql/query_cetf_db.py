#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append('/home/yhl2/workspace/xtp_test')
from mysql.mysql_config import connectMysql


class query_cetf_db(object):
    """连接数据库并查询跨市场ETF数据的类"""


    def __init__(self):
        """获取当天日期"""
        self.date = time.strftime('%Y%m%d', time.localtime(time.time()))

    def __select_db_fetch_one(self,s):
        """连接数据库，执行语句，返回第一条结果"""
        conn = connectMysql()
        cur = conn.cursor()
        rs = []
        try:
            cur.execute(s)
            rs = cur.fetchone()
        except Exception,e:
            print u'执行sql语句失败'
            print e
        finally:
            cur.close()
            conn.close()
        return rs[0] if rs else 0

    def __select_db_fetch_all(self,s):
        """连接数据库，执行语句，返回所有结果"""
        conn = connectMysql()
        cur = conn.cursor()
        rs = []
        try:
            cur.execute(s)
            rs = cur.fetchall()
        except Exception,e:
            print u'执行sql语句失败'
            print e
        finally:
            cur.close()
            conn.close()
        return rs if rs else 0

    def query_creation_redem_unit(self,ticker):
        """查询etf最小申赎单位"""
        sql = ('SELECT creation_redemption_unit from xtp_etf_baseinfo_' +
               self.date + ' t1 where t1.ticker=' + ticker + '')

        return self.__select_db_fetch_one(sql)

    def query_cetf_basketcount(self,ticker):
        """查询跨市场etf成分股数量"""
        sql = ('SELECT count(*) from xtp_etf_components_' + self.date +
              ' a join xtp_etf_baseinfo_' + self.date +
              ' b on a.etf_code1 = b.etf_code1 where b.ticker=' + ticker + '')

        return self.__select_db_fetch_one(sql)

    def query_estimate_cash_component(self,ticker):
        """查询预估现金差额"""
        sql = ('SELECT estimate_cash_component / 10000.0' +
              ' from xtp_etf_baseinfo_' + self.date +
              ' where etf_code0 = ' + ticker)

        return self.__select_db_fetch_one(sql)

    def query_cetf_asset(self,stockcode, market, security_type, security_status,
                         trade_status, fundid):
        """查询跨市场etf持仓
        参数：证券代码、市场、证券状态、交易状态、资金账号"""
        if stockcode == '999999':
            sql = ('SELECT a.stock_code,c.creation_redemption_unit' +
                ' from xtp_stk_asset_' + self.date + ' a,xtp_exch_sec_' +
                   self.date + ' b,xtp_etf_baseinfo_' + self.date +
                  ' c WHERE a.stock_code=b.instrument_id' +
                  ' AND a.stock_code=c.ticker AND b.exch_id=' + market +
                   ' AND b.security_type=' + security_type +
                   ' and b.security_status=' + security_status +
                  ' and b.trade_status=' + trade_status +
                   ' AND a.fund_acc=\'' + fundid + '\'')
        else:
            sql = ('SELECT a.stock_code,c.creation_redemption_unit' +
                   ' from xtp_stk_asset_' +self.date + ' a,xtp_exch_sec_' +
                   self.date + ' b,xtp_etf_baseinfo_' + self.date +
                  ' c WHERE a.stock_code=b.instrument_id' +
                  ' AND a.stock_code=c.ticker AND b.exch_id=' + market +
                  ' AND b.security_type=' + security_type +
                  ' and b.security_status=' + security_status +
                  ' and a.stock_code = ' + stockcode +
                  ' and b.trade_status=' + trade_status +
                  ' AND a.fund_acc=\'' + fundid + '\'')

        return self.__select_db_fetch_all(sql)

    def query_cetf_components_info(self,ticker, market_id):
        """
        根据二级市场代码获取所有成分股的信息
        :param ticker: etf二级市场代码
        :param market_id: etf市场，1是上海，2是深圳
        :return:
        """
        market_id = str(market_id)
        sql = ('SELECT underlying_instrument_id, substitute_flag,' +
               ' component_share, premium_ratio, preclose_px/10000,' +
               ' creation_cash_substitute, estimate_cash_component,' +
               ' redemption_cash_substitute, underlying_instrument_source' +
               ' from xtp_etf_components_' + self.date + ' a, xtp_etf_baseinfo_'
               + self.date +
               ' b, xtp_exch_sec_' + self.date + ' c' +
               ' where a.etf_code1 = b.etf_code1' +
               ' and a.underlying_instrument_id = c.instrument_id' +
               ' and b.ticker = "' + ticker + '"' +
               ' and b.exch_id = "' + market_id + '"' +
               ' and c.security_type in (0, 1, 2)')

        return self.__select_db_fetch_all(sql)

    def query_cetf_components_code(self,ticker):
        """根据一级市场代码查询出ETF所有成分股代码
        ticker：etf一级市场代码"""
        sql = ('SELECT'
               ' underlying_instrument_id'
               ' from'
               ' xtp_etf_components_' + self.date + ' c'
                ' join'
                ' xtp_exch_sec_' + self.date + ' e'
                ' on c.underlying_instrument_id = e.instrument_id'
                ' where'
                ' c.etf_code1 = ' + ticker +
               ' and e.security_type in (0, 1, 2)'
               ' and e.security_status = 2')
        conn = connectMysql()
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
            rs = cur.fetchall()
            code_rs = []
            if rs is not ():
                for code in rs:
                    code_rs.append(code[0])
        return code_rs

    def query_cetf_code1code2(self,ticker):
        """获取etf '一级市场申购赎回代码' 和 '资金划转代码'"""
        sql = 'SELECT etf_code1, etf_code2' \
              ' from xtp_etf_baseinfo_' + self.date + \
              ' where etf_code0 = ' + ticker
        conn = connectMysql()
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
            rs = cur.fetchall()
            code_rs = {}
            if rs is not ():
                code_rs['etf_code1'] = rs[0][0]
                code_rs['etf_code2'] = rs[0][1]
        return code_rs

    def query_cetf_components(self,ticker, underlying_instrument_id):
        """根据etf代码查询单支成分股数量
        参数ticker：二级市场代码
        underlying_instrument_id：成分股代码"""
        sql = 'SELECT a.component_share ' \
              'from xtp_etf_components_' + self.date + \
              ' a, xtp_etf_baseinfo_' + self.date + \
              ' b where a.etf_code1 = b.etf_code1 ' \
              ' and b.ticker = "' + ticker + \
              '" and a.underlying_instrument_id = "' \
              + underlying_instrument_id + '"'

        return self.__select_db_fetch_one(sql)[0]

    def query_cetf_substitute(self,ticker, underlying_instrument_id):
        """查询etf单支成分股数量及现金替代标志
        参数ticker：etf二级市场代码
        参数underlying_instrument_id：成分股代码
        """
        sql = 'SELECT a.component_share, a.substitute_flag ' \
              'from xtp_etf_components_' + self.date + \
              ' a, xtp_etf_baseinfo_' + self.date + \
              ' b where a.etf_code1 = b.etf_code1 ' \
              ' and b.ticker = "' + ticker + \
              '" and a.underlying_instrument_id = "' \
              + underlying_instrument_id + '"'

        return self.__select_db_fetch_one(sql)

    def query_cetf_component_share(self,ticker):
        """查询etf的成分股代码及成分股对应数量(etf最小申购赎回时对应的该成分股数量)
        参数ticker：ETF二级市场代码  返回字典：key=成分股，value=成分股数量
        """
        sql = 'SELECT ' \
              ' a.underlying_instrument_id, ' \
              ' a.component_share ' \
              'from xtp_etf_components_' + self.date + \
              ' a, xtp_etf_baseinfo_' + self.date + \
              ' b where a.etf_code1 = b.etf_code1 ' \
              ' and b.ticker = ' + ticker
        rs = self.__select_db_fetch_all(sql)
        component_shares = dict(rs)
        return component_shares

    def query_creation_redemption_subcash(self,etf_code1):
        """查询同市场成分股必须现金替代时，申赎或赎回需要的总金额"""
        sql = ('SELECT ' +
          ' case when sum(creation_cash_substitute) is null then 0' +
          '   else sum(creation_cash_substitute) end as sum_creation_cash,' +
          ' case when sum(redemption_cash_substitute) is null then 0'
          '   else sum(redemption_cash_substitute) end as sum_redemption_cash' +
          ' from xtp_etf_components_' + self.date +
          ' where etf_code1 = ' + etf_code1 +
          ' and substitute_flag = 2')
        rs = self.__select_db_fetch_all(sql)
        code_rs = {}
        if rs:
            code_rs['creation_cash_substitute'] = rs[0][0]
            code_rs['redemption_cash_substitute'] = rs[0][1]
        return code_rs

    def query_crossmakert_sub_cash(self,etf_code1):
        """
        查询跨市场etf申赎或赎回时，跨市场成分股（退补现金替代 + 必须现金替代）需要的总金额
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
            ' from xtp_etf_components_' + self.date +
            ' where etf_code1 = ' + etf_code1 +
            ' and substitute_flag = 3')
        sql2 = ('SELECT ' +
            ' case when sum(creation_cash_substitute) is null then 0' +
            '   else sum(creation_cash_substitute) end as sum_creation_cash,' +
            ' case when sum(redemption_cash_substitute) is null then 0' +
            '   else sum(redemption_cash_substitute) end as sum_redemption_cash' +
            ' from xtp_etf_components_' + self.date +
            ' where etf_code1 = ' + etf_code1 +
            ' and substitute_flag = 4')
        # 退补现金替代部分
        rs1 = self.__select_db_fetch_all(sql1)
        code_rs1 = [0, 0]
        if rs1:
            code_rs1[0] = rs1[0][0]
            code_rs1[1] = rs1[0][1]
        # 必须现金替代部分
        rs2 = self.__select_db_fetch_all(sql2)
        code_rs2 = [0, 0]
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

    def query_preclose_price(self,stkcode):
        """
        获取股票昨收价
        :param stkcode:股票代码
        :return: Decimal('9.4400')
        """
        sql = ('SELECT a.preclose_px/10000 from xtp_exch_sec_'
               + self.date + ' a WHERE a.instrument_id =' +
               stkcode + ' AND a.security_type != 255 and a.trade_status!=255')
        preclose_price = 0
        rs = self.__select_db_fetch_one(sql)
        if rs:
            preclose_price = rs[0]

        return preclose_price

    def query_compnents_preclose_price(self,etfcode):
        """
        获取etf所有成分股昨收价
        :param etfcode: etf二级市场代码
        :return: {code1:price1, code2:price2, code3:price3, ...}
        """
        sql = ('SELECT'
            ' c.instrument_id,'
            ' c.preclose_px/10000'
            ' FROM'
            ' xtp_etf_baseinfo_'
            + self.date + ' a'
            ' JOIN xtp_etf_components_' + self.date + ' b on'
            ' a.etf_code1 = b.etf_code1'
            ' JOIN xtp_exch_sec_' + self.date + ' c on'
            ' b.underlying_instrument_id = c.instrument_id'
            ' WHERE a.ticker = ' + etfcode +
            ' AND b.exch_id = c.exch_id'
            ' AND c.security_type != 255 and c.trade_status!=255')
        components_precloseprices = {}
        result = self.__select_db_fetch_all(sql)
        if result:
            for rs in tuple(result):
                components_precloseprices[rs[0]] = float(rs[1])
        return components_precloseprices

    def query_premium_ratio(self,etf_code1):
        """
        查询etf可现金替代成分股及其溢价比例
        :param etf_code1: etf一级市场代码
        :return:((code1,decimal(0.100),成分股数),(code2,decimal(0.100),成分股数)...)
        """
        sql = ('SELECT underlying_instrument_id, premium_ratio / 100000, ' +
                  'component_share from xtp_etf_components_' + self.date +
                  ' where substitute_flag = 1' +
                  ' and etf_code1 = ' + str(etf_code1))
        rs = self.__select_db_fetch_all(sql)

        return rs

    def query_cetf_nav(self,ticker):
        """
        查询Etf单位净值
        :param ticker: etf二级市场代码
        :return:
        """
        sql = ('SELECT nav from xtp_etf_baseinfo_' + self.date +
               ' b where b.ticker=' + ticker + '')
        rs = self.__select_db_fetch_one(sql)

        return rs




query_cetf = query_cetf_db()


if __name__ == '__main__':
    print query_cetf.query_creation_redem_unit('510300')
    # print query_cetf.query_cetf_basketcount('510300')
    # print query_cetf.query_estimate_cash_component('510300')
    # print query_cetf.query_cetf_component_share('510300')
    #print query_cetf.query_cetf_nav('510300')

