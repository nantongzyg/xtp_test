#!/usr/bin/python
# -*- encoding: utf-8 -*-

import MySQLdb
import sys
import logging
from mysql_config import *
import collections
import os
sys.path.append('/home/yhl2/workspace/xtp_test/service')
import ServiceConfig
sys.path.append('/home/yhl2/workspace/xtp_test/mysql')
import QueryFundidDB
from database_manager import QueryTable
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import Config


"""用于将mysql中造的测试数据导入当天数据库表"""
class SqlData_Transfer(object):
    def __init__(self):
        self.log_file = 'SqlData_Transfer.log'
        logging.basicConfig(filename=self.log_file, filemode="w",
                            format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",
                            level=logging.DEBUG)
        self.logger = logging.getLogger("log_demo")

    def transfer_stk_asset(self):
        self.delete_stk_asset()
        self.insert_stk_asset()

    def keep_stk_asset(self):
        self.delete_stk_asset()
        self.insert_stk_asset()
        self.keep_guarantee_stk()

    def transfer_debt_details(self, debt_list, xtp_id):
        self.delete_debt_details()
        self.insert_debt_details(debt_list, xtp_id)
        self.delete_debt_details_by_time()

    def delete_debts_data(self):
        self.delete_debt_details()
        self.delete_debt_check() 

    def transfer_opt_stk_asset(self):
        self.delete_opt_stk_asset()
        self.insert_opt_stk_asset()

    def transfer_exch_sec(self):
        self.delete_exch_sec()
        self.insert_exch_sec()

    def transfer_credit_exceptional_stk(self):
        self.delete_credit_exceptional_stk()
        self.insert_credit_exceptional_stk()

    def transfer_credit_cash_stk_asset(self):
        self.delete_credit_cash_stk_asset()
        self.insert_credit_cash_stk_asset()

    def transfer_credit_guarantee_stk(self):
        self.delete_credit_guarantee_stk()
        self.insert_credit_guarantee_stk()

    def transfer_credit_target_stk(self):
        self.delete_credit_target_stk()
        self.insert_credit_target_stk()

    def transfer_credit_margin_rate_off(self):
        self.delete_credit_margin_rate_off()
        self.insert_credit_margin_rate_off()

    def transfer_opt_exch_sec(self):
        self.delete_opt_exch_sec()
        self.insert_opt_exch_sec()

    def transfer_fund_asset(self, py_name):
        self.delete_fund_asset()
        self.insert_fund_asset(py_name)

    def transfer_credit_cash_fund_asset(self, py_name):
        self.update_credit_cash_fund_asset(py_name)

    def transfer_credit_debts(self, py_name):
        self.delete_credit_debts()
        self.insert_credit_debts(py_name)

    def transfer_credit_asset(self, py_name):
        self.delete_credit_asset(py_name)
        self.insert_credit_asset(py_name)

    def transfer_credit_cust_contract(self, py_name):
        self.delete_credit_cust_contract()
        self.insert_credit_cust_contract(py_name)

    def insert_exch_sec(self):
        """将xtp_exch_sec_auto表数据导入到xtp_exch_sec_%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        try:
            sql = '''insert into %s
                       select * from %s''' % (out_exch_db, in_exch_db)
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("insert_exch_sec success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_exch_sec failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_credit_exceptional_stk(self):
        """将xtp_credit_exceptional_stk_auto表数据导入到xtp_credit_exceptional_stk_%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        try:
            sql = '''insert into %s
                       select * from %s''' % (out_credit_exceptional_stk_db, in_credit_exceptional_stk_db)
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("insert_credit_exceptional_stk success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_credit_exceptional_stk failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_credit_cash_stk_asset(self):
        """将xtp_credit_cash_stk_asset_auto表数据导入到xtp_credit_cash_stk_asset_%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        try:
            sql = '''insert into %s
                       select * from %s''' % (out_credit_cash_stk_asset, in_credit_cash_stk_asset)
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("insert_credit_cash_stk_asset success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_credit_cash_stk_asset failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_credit_guarantee_stk(self):
        """将xtp_credit_guarantee_stk_auto表数据导入到xtp_credit_guarantee_stk_%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        try:
            sql = '''insert into %s
                       select * from %s''' % (out_credit_guarantee_stk, in_credit_guarantee_stk)
            print sql
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("insert_credit_guarantee_stk success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_credit_guarantee_stk failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_credit_target_stk(self):
        """将xtp_credit_target_stk_auto表数据导入到xtp_credit_target_stk_%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        try:
            sql = '''insert into %s
                       select * from %s''' % (out_credit_target_stk, in_credit_target_stk)
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("insert_credit_target_stk success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_credit_target_stk failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_credit_margin_rate_off(self):
        """将xtp_credit_margin_rate_off_auto表数据导入到xtp_credit_margin_rate_off_%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        # 查询资金账号
        fund_acc = QueryFundidDB.QueryFundidDB()
        try:
            sql = '''insert into %s
                       select 
                         %s,
                         rz_rate_off,
                         rz_rate_low,
                         rq_rate_off,
                         rq_rate_low,
                         node_id
                       from %s ''' % (out_credit_margin_rate_off, fund_acc, in_credit_margin_rate_off)
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("insert_credit_margin_rate_off success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_credit_margin_rate_off failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_opt_exch_sec(self):
        """将xtp_opt_exch_sec_auto表数据导入到xtp_opt_exch_sec_%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        try:
            sql = '''insert into %s
                       select * from %s''' % (out_opt_exch_db, in_opt_exch_db)
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("insert_opt_exch_sec success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_opt_exch_sec failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_etf_baseinfo(self):
        """将xtp_etf_baseinfo_auto表数据导入到xtp_etf_baseinfo%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        try:
            sql = '''insert into %s
                       select * from %s''' % (out_etf_baseinfo, in_etf_baseinfo)
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("insert_etf_baseinfo success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_etf_baseinfo failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_etf_components(self):
        """将xtp_etf_components_auto表数据导入到xtp_etf_components%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        try:
            sql = '''insert into %s
                       select * from %s''' % (out_etf_components, in_etf_components)
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("in_etf_components success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("in_etf_components failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_issue_params(self):
        """将xtp_issue_params_auto表数据导入到xtp_issue_params%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        try:
            sql = '''insert into %s
                               select * from %s''' % (
                out_issue_params, in_issue_params)
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("in_issue_params success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("in_issue_params failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_rights_issue_params(self):
        """将xtp_rights_issue_params_auto表数据导入到xtp_rights_issue_params%s (today)"""
        # 连接数据库
        conn = connectMysql()
        self.logger.info("sql able to connect!")
        cur = conn.cursor()
        try:
            sql = '''insert into %s
                               select * from %s''' % (
                out_rights_issue_params, in_rights_issue_params)
            cur.execute(sql)
            conn.commit()
            self.logger.info(sql)
            self.logger.info("in_rights_issue_params success!")
        except:
            # Error_Msg="Mysql Error %d: %s" % (e.args[0], e.args[1])
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("in_rights_issue_params failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_credit_cust_contract(self, py_name):
        """将xtp_credit_cust_contract_auto表数据导入到xtp_credit_cust_contract_%s(today)"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号
        fund_acc = QueryFundidDB.QueryFundidDB()
        client_id = QueryTable('xtp_user', ['custid'], {'user_name': Config.trade.user}, 2)['custid']
        try:
            sql = '''insert into %s
                       select 
                         %d,
                         %s,
                         branch_id,
                         cur_type,
                         fi_debts_bal,
                         sl_debts_bal,
                         all_debts_bal,
                         fi_mar_rate,
                         sl_mar_rate,
                         fi_intr_rate,
                         sl_intr_rate,
                         intr_type,
                         contract_rights,
                         cash_grp_no,
                         sp_cash_grp_no,
                         crd_fare_str,
                         sp_crd_fare_str,
                         crd_level,
                         get_intr_way,
                         node_id
                       from %s
                       where py_name = '%s'
            ''' % (out_credit_cust_contract, client_id, fund_acc, in_credit_cust_contract, py_name)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("insert_credit_cust_contract success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_credit_cust_contract failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_fund_asset(self, py_name):
        """将xtp_fund_asset_auto表数据导入到xtp_fund_asset_%s(today)"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号
        fund_acc = QueryFundidDB.QueryFundidDB()
        try:
            sql = '''insert into %s
                       select
                        %s,
                        cur_type,
                        fund_avl_bal,
                        fund_frz_bal,
                        fund_bal,
                        fund_buy_sale,
                        fund_unc_buy,
                        fund_unc_sale,
                        fund_trsf,
                        node_id
                  from %s where py_name="%s"''' % (out_fund_asset_db, fund_acc, in_fund_asset_db, py_name)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("insert_fund_asset" + str(py_name) + "success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_fund_asset" + str(py_name) + "failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def update_credit_cash_fund_asset(self, py_name):
        """将xtp_credit_cash_fund_asset_auto表数据更新到xtp_credit_cash_fund_asset_%s(today)"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询头寸编号
        cash_grp_no = QueryTable('xtp_credit_cash_fund_asset_' + today,
            ['cash_grp_no'], {'cash_grp_name': 'XTPVIP_100'}, 2)['cash_grp_no']
        try:
            sql = '''update 
                         %s a
                     inner join 
                         %s b
                     set
                         a.fund_avl_bal = b.fund_avl_bal
                     where 
                         a.cash_grp_name = b.cash_grp_name
                     and b.py_name = '%s'
                  ''' % (out_credit_cash_fund_asset_db, in_credit_cash_fund_asset_db, py_name)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("update_credit_cash_fund_asset" + str(py_name) + "success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("update_credit_cash_fund_asset" + str(py_name) + "failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_credit_debts(self, py_name):
        """将xtp_credit_debts_auto表数据导入到xtp_credit_debts_%s(today)"""
        # 连接数据库
        today = datetime.date.today()
        today = today.strftime('%Y%m%d')
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号
        fund_acc = QueryFundidDB.QueryFundidDB()
        # 查询client_id
        client_id = QueryTable('xtp_user', ['custid'], {'user_name': Config.trade.user}, 2)['custid']
        # 查询头寸编号
        cash_grp_no = QueryTable('xtp_credit_cash_fund_asset_' + today,
            ['cash_grp_no'], {'cash_grp_name': 'XTPVIP_100'}, 2)['cash_grp_no']
        try:
            sql = '''insert into %s
                       select
                        compact_id
                        ,order_date
                        ,order_time
                        ,station
                        ,trade_way
                        ,operator
                        ,order_no
                        ,order_id
                        ,%s
                        ,branch_id
                        ,%s
                        ,cur_type
                        ,credit_direct
                        ,market
                        ,secu_acc
                        ,stk_code
                        ,stock_type
                        ,trd_id
                        ,order_price
                        ,order_qty
                        ,tnvr_qty
                        ,tnvr_amt
                        ,trade_fee
                        ,end_date
                        ,old_end_date
                        ,intr_rate
                        ,punish_rate
                        ,delay_int
                        ,intr_begin_date
                        ,punish_begin_rate
                        ,margin_rate
                        ,%s
                        ,csh_grp_type
                        ,credit_fare_str
                        ,intr_type
                        ,contract_amt
                        ,contract_qty
                        ,contract_trd_fee
                        ,credit_repay
                        ,stk_repay
                        ,intr_pro
                        ,punish_intr_pro
                        ,contract_intr
                        ,intr_repay
                        ,life_status
                        ,close_date
                        ,due_rights
                        ,due_right_qty
                        ,punish_debts
                        ,debts_type
                        ,debts_value
                        ,right_adjust_qty
                        ,node_id
                  from %s where py_name="%s"''' % (out_credit_debts_db, fund_acc, client_id, cash_grp_no, in_credit_debts_db, py_name)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("insert_credit_debts" + str(py_name) + "success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_credit_debts" + str(py_name) + "failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_credit_asset(self, py_name):
        """将xtp_credit_asset_auto表数据导入到xtp_credit_asset_%s(today)"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号
        fund_acc = QueryFundidDB.QueryFundidDB()
        client_id = QueryTable('xtp_user', ['custid'], {'user_name': Config.trade.user}, 2)['custid']
        try:
            sql = '''insert into %s
                       select
                            %d,
                            %s,
                            branch_id,
                            cur_type,
                            fund_avl_bal,
                            debt_bal,
                            mar_avl,
                            fund_des,
                            asset_des,
                            fi_avl,
                            fi_used,
                            fi_contract_amt,
                            sl_avl,
                            sl_used,
                            sl_mkt,
                            sub_stk_mkt,
                            all_stk_mkt,
                            mdbp_avl,
                            rzbd_avl,
                            mqhq_avl,
                            xjhk_avl,
                            expect_intr,
                            other_fee,
                            correct_amt,
                            debts_type,
                            debts_value,
                            node_id
                  from %s where py_name="%s"''' % \
                  (out_credit_asset_db, client_id, fund_acc, in_credit_asset_db, py_name)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("insert_credit_asset" + str(py_name) + "success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_credit_asset" + str(py_name) + "failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()            

    def insert_stk_asset(self):
        """将xtp_stk_asset_auto表数据导入到xtp_stk_asset_%s(today)"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号和股东账号
        user_info = QueryFundidDB.QueryFundidSecuAccDB()
        self.logger.info("sql able to connect!")
        try:
            sql = '''insert into %s
                      select
                        %s,
                        market,
                        case market when 1
                          then '%s'
                          else '%s'
                        end as secu_acc,
                        stock_code,
                        stk_avl_qty,
                        stk_frz_qty,
                        stk_bal,
                        stk_buy_sale,
                        stk_buy_unfrz,
                        stk_sale_frz,
                        lst_buy_cst,
                        lst_prf_cst,
                        buy_cst,
                        profit_cst,
                        stk_remain,
                        stk_corp_rem,
                        cre_stk_bal,
                        node_id
                      from %s''' % (out_stk_db,
                                    user_info['fund_acc'],
                                    user_info['secu_acc_sh'],
                                    user_info['secu_acc_sz'],
                                    in_stk_db)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("insert_stk_asset success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_stk_asset failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_debt_details(self, debt_list, xtp_id):
        """将oms日志中的卖券还款的还款信息插入debt_details表"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            for debt in debt_list:
                if debt['xtp_id'] == str(xtp_id):
                    sql = '''insert into %s
                        values(%s, %s, %s, '%s', %s, %d)''' % \
                        (out_debt_details, debt['time'], debt['xtp_id'], debt['debt_id'], debt['index'], debt['amount'], debt['order'])
                    self.logger.info(sql)
                    cur.execute(sql)
            conn.commit()
            self.logger.info("insert_debt_details success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_debt_details failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()


    def insert_opt_stk_asset(self):
        """将xtp_opt_stk_asset_auto表数据导入到xtp_opt_stk_asset_%s(today)"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号和股东账号
        user_info = QueryFundidDB.QueryFundidOptSecuAccDB()
        self.logger.info("sql able to connect!")
        try:
            sql = '''insert into %s
                      select
                        %s,
                        market,
                        '%s' as secu_acc,
                        cntrt_code,
                        cntrt_name,
                        opt_avl_qty,
                        opt_frz_qty,
                        opt_bal,
                        pos_side,
                        cntrt_type,
                        tgt_stk_code,
                        tgt_stk_type,
                        buy_cost,
                        margin,
                        buy_amt_used,
                        opt_premium,
                        opt_cvd_asset,
                        sum_cls_profit,
                        combed_qty,
                        opt_posi_rlt
                      from %s''' % (out_opt_stk_db,
                                    user_info['fund_acc'],
                                    user_info['secu_acc'],
                                    in_opt_stk_db)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("insert_opt_stk_asset success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_opt_stk_asset failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_fund_creation(self):
        """将xtp_fund_creation_auto表数据导入到xtp_fund_creation_%s(today)"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = '''insert into %s select
                        *
                     from
                        %s''' % (out_fund_creation, in_fund_creation)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("insert_fund_creation success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_fund_creation failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_structured_fund_params(self):
        """将xtp_structured_fund_params_auto表数据导入到xtp_structured_fund_params_%s(today)"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = '''insert into %s select
                        *
                     from
                        %s''' % (out_structured_fund_params, in_structured_fund_params)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("insert_structured_fund_params success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_structured_fund_params failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def update_cur_fee_rate(self, fee_type, py_name):
        """
        修改xtp_cur_fee_rate表的费用配置

        :param fee_type: 1-etf申赎费用, 2-分级基金申赎
        :param py_name: case脚本名称
        :return:
        """
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询用户id
        user_id = QueryTable(xtp_user, ['id'],
                             {'user_name': Config.trade.user}, 2)
        self.logger.info("sql able to connect!")
        try:
            if fee_type == 1:
                fee_rate_id = [4001, 4002, 4003]
                for id in fee_rate_id:
                    sql = '''
                            update %s set
                              value = %s
                            where
                              user_id = %s
                            and fee_rate_id = %s''' % (
                        cur_fee_rate,
                        ServiceConfig.fee_etf_creation_redemption[py_name][id],
                        user_id['id'], id
                    )
                    cur.execute(sql)
            elif fee_type == 2:
                fee_rate_id = [3001, 3002, 3003]
                for id in fee_rate_id:
                    sql = '''
                            update %s set
                              value = %s
                            where
                              user_id = %s
                            and fee_rate_id = %s''' % (
                        cur_fee_rate,
                        ServiceConfig.fee_structured_fund_creation_redemption[py_name][id],
                        user_id['id'], id
                    )
                    cur.execute(sql)
            else:
                self.logger.error("错误的fee_type传值，1-etf申赎费用, 2-分级基金申赎")
            self.logger.info(sql)
            conn.commit()
            self.logger.info("update_cur_fee_rate success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("update_cur_fee_rate failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_credit_cust_contract(self):
        """将表xtp_credit_asset_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        fund_acc = QueryFundidDB.QueryFundidDB()
        client_id = QueryTable('xtp_user', ['custid'], {'user_name': Config.trade.user}, 2)['custid']
        self.logger.info("sql able to connect!")
        try:
            sql = "delete from %s" \
                  " where fund_acc = %s and client_id = %d" % (
                out_credit_cust_contract, fund_acc, client_id
            )

            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_credit_cust_contract))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_credit_cust_contract))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_fund_asset(self):
        """将表xtp_credit_asset_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        fund_acc = QueryFundidDB.QueryFundidDB()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete from %s" \
                  " where fund_acc = %s" % (
                out_fund_asset_db, fund_acc
            )

            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_fund_asset_db))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_fund_asset_db))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_credit_debts(self):
        """将表xtp_credit_debts_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        fund_acc = QueryFundidDB.QueryFundidDB()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete from %s" \
                  " where fund_acc = %s" % (
                out_credit_debts_db, fund_acc
            )

            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_credit_debts_db))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_credit_debts_db))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_credit_asset(self, py_name):
        """将表xtp_credit_asset_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        fund_acc = QueryFundidDB.QueryFundidDB()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete from %s" \
                  " where fund_acc = %s" % (
                out_credit_asset_db, fund_acc
            )

            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_credit_asset_db))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_credit_asset_db))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_exch_sec(self):
        """将表xtp_exch_sec_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.exch_id = %s.exch_id" \
                  " and %s.instrument_id = %s.instrument_id" % (
                out_exch_db, out_exch_db, in_exch_db,
                out_exch_db, in_exch_db,
                out_exch_db, in_exch_db)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_exch_db))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_exch_db))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_credit_exceptional_stk(self):
        """将表xtp_credit_exceptional_stk_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete from %s" % (
                out_credit_exceptional_stk_db)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_credit_exceptional_stk_db))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_credit_exceptional_stk_db))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_exch_sec(self):
        """将表xtp_exch_sec_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.exch_id = %s.exch_id" \
                  " and %s.instrument_id = %s.instrument_id" % (
                out_exch_db, out_exch_db, in_exch_db,
                out_exch_db, in_exch_db,
                out_exch_db, in_exch_db)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_exch_db))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_exch_db))
        finally:
            cur.close()
            # 关闭连接
            conn.close()
    def delete_credit_cash_stk_asset(self):
        """将表xtp_credit_cash_stk_asset_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete from %s" % (out_credit_cash_stk_asset)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_credit_cash_stk_asset))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_credit_cash_stk_asset))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_credit_guarantee_stk(self):
        """将表xtp_credit_guarantee_stk_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.market = %s.market" \
                  " and %s.stk_code = %s.stk_code" % (
                out_credit_guarantee_stk, out_credit_guarantee_stk, in_credit_guarantee_stk,
                out_credit_guarantee_stk, in_credit_guarantee_stk,
                out_credit_guarantee_stk, in_credit_guarantee_stk)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_credit_guarantee_stk))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_credit_guarantee_stk))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_credit_target_stk(self):
        """将表xtp_credit_target_stk_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.market = %s.market" \
                  " and %s.stk_code = %s.stk_code" % (
                out_credit_target_stk, out_credit_target_stk, in_credit_target_stk,
                out_credit_target_stk, in_credit_target_stk,
                out_credit_target_stk, in_credit_target_stk)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_credit_target_stk))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_credit_target_stk))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_credit_margin_rate_off(self):
        """将表xtp_credit_margin_rate_off_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号
        fund_acc = QueryFundidDB.QueryFundidDB()
        self.logger.info("sql able to connect!")
        try:
            sql = '''delete from %s where fund_acc = %s''' % (
                out_credit_margin_rate_off, fund_acc)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_credit_margin_rate_off))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_credit_margin_rate_off))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_opt_exch_sec(self):
        """将表xtp_opt_exch_sec_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.exch_id = %s.exch_id" \
                  " and %s.instrument_id = %s.instrument_id" % (
                out_opt_exch_db, out_opt_exch_db, in_opt_exch_db,
                out_opt_exch_db, in_opt_exch_db,
                out_opt_exch_db, in_opt_exch_db)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_opt_exch_db))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_opt_exch_db))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_issue_params(self):
        """将表xtp_issue_params_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where  %s.ticker = %s.ticker" % (
                out_issue_params, out_issue_params, in_issue_params,
                out_issue_params, in_issue_params)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_issue_params))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_issue_params))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_rights_issue_params(self):
        """将表xtp_rights_issue_params_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where  %s.ticker = %s.ticker" % (
                out_rights_issue_params, out_rights_issue_params, in_rights_issue_params,
                out_rights_issue_params, in_rights_issue_params)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_rights_issue_params))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_rights_issue_params))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_etf_baseinfo(self):
        """将表xtp_etf_baseinfo_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.exch_id = %s.exch_id" \
                  " and %s.ticker = %s.ticker" % (
                out_etf_baseinfo, out_etf_baseinfo, in_etf_baseinfo,
                out_etf_baseinfo, in_etf_baseinfo,
                out_etf_baseinfo, in_etf_baseinfo)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_etf_baseinfo))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_etf_baseinfo))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_etf_components(self):
        """将表xtp_etf_components_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.exch_id = %s.exch_id" \
                  " and %s.etf_code1 = %s.etf_code1" \
                  " and %s.underlying_instrument_id = %s.underlying_instrument_id" % (
                out_etf_components, out_etf_components, in_etf_components,
                out_etf_components, in_etf_components,
                out_etf_components, in_etf_components,
                out_etf_components, in_etf_components)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_etf_components))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_etf_components))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_stk_asset(self):
        """将表xtp_stk_asset_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号
        fund_acc = QueryFundidDB.QueryFundidDB()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.fund_acc = %s" \
                  "  and %s.market = %s.market" \
                  "  and %s.stock_code = %s.stock_code" % (
                    out_stk_db, out_stk_db, in_stk_db,
                    out_stk_db, fund_acc,
                    out_stk_db, in_stk_db,
                    out_stk_db, in_stk_db)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_stk_db))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_stk_db))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_debt_details(self):
        """将表debt_details中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete from %s" % (
                    out_debt_details)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_debt_details))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_debt_details))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_debt_check(self):
        """将表debt_check中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete from %s" % (
                    out_debt_check)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_debt_check))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_debt_check))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_debt_details_by_time(self):
        """将表debt_details中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = '''delete
                      from
                            %s
                     where
                            time !=
                        (select
                                last_time
                          from
                       (select max(cast(time as unsigned)) as last_time from %s) as sub) ''' % (
                    out_debt_details, out_debt_details)
            self.logger.info(sql)
            # cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_debt_details))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_debt_details))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_all_stk_asset(self):
        """将表xtp_stk_asset_xxxx中当前用户的持仓删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号
        fund_acc = QueryFundidDB.QueryFundidDB()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.fund_acc = %s" % (
                    out_stk_db, out_stk_db, in_stk_db,
                    out_stk_db, fund_acc)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_stk_db))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_stk_db))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_opt_stk_asset(self):
        """将表xtp_opt_stk_asset_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号
        fund_acc = QueryFundidDB.QueryFundidDB()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.fund_acc = %s" \
                  "  and %s.market = %s.market" \
                  "  and %s.cntrt_code = %s.cntrt_code" % (
                    out_opt_stk_db, out_opt_stk_db, in_opt_stk_db,
                    out_opt_stk_db, fund_acc,
                    out_opt_stk_db, in_opt_stk_db,
                    out_opt_stk_db, in_opt_stk_db)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_opt_stk_db))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_opt_stk_db))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_fund_creation(self):
        """将表xtp_fund_creation_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = 'delete from %s' % (
                out_fund_creation
            )
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_fund_creation))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_fund_creation))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_structured_fund_params(self):
        """将表xtp_structured_fund_params_xxxx中的数据给删除"""
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = 'delete from %s' % (
                out_structured_fund_params
            )
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_structured_fund_params))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_structured_fund_params))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def truncate_sse(self):
        """清空上海接口库"""
        conn = connectMssql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        truncate_tb = ''
        try:
            for tb in ServiceConfig.truncate_tables_sh:
                truncate_tb = tb
                sql = 'TRUNCATE TABLE %s' % tb
                self.logger.info(sql)
                cur.execute(sql)
                conn.commit()
            conn.close()
            self.logger.info("truncate table %s success!" % str(truncate_tb))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("truncate table %s failed!" % str(truncate_tb))
        finally:
            cur.close()
            # 关闭连接
            conn.close()
    # 只保留担保品股票持仓
    def keep_guarantee_stk(self):
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号
        fund_acc = QueryFundidDB.QueryFundidDB()
        self.logger.info("sql able to connect!")
        try:
            sql = '''
                    delete a
                    from %s a
                    where not exists (select 1 from %s b where a.stock_code = b.stk_code)
                    and a.fund_acc = %s
            ''' % (out_stk_db, out_credit_guarantee_stk, fund_acc)
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_cur_risk))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_cur_risk))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def delete_cur_risk(self):
        '''删除xtp_cur_risk数据'''
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            sql = "delete %s from %s, %s" \
                  " where %s.user_name = '%s'" \
                  "  and %s.server_id = %s.trade_server_id" % (
                        out_cur_risk, out_cur_risk, xtp_user,
                        xtp_user, Config.trade.user,
                        out_cur_risk, xtp_user
                      )
            self.logger.info(sql)
            cur.execute(sql)
            conn.commit()
            self.logger.info("delete table %s success!" % str(out_cur_risk))
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("delete table %s failed!" % str(out_cur_risk))
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def insert_cur_risk(self, py_name):
        '''插入xtp_cur_risk数据'''
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        self.logger.info("sql able to connect!")
        try:
            # 查询用户id和trade_server_id
            user_rs = QueryTable(xtp_user, ['id', 'trade_server_id'], {'user_name': Config.trade.user}, 2)
            # 获取需要插入的各个风控值
            rs = self.query_cur_risk_auto(py_name)
            rule_id = [
                0, 1001, 1002, 2001, 2002,
                9001, 9002, 10001, 10002, 14001,
                14002, 14003, 14004, 25001, 25002,
                26001, 26002, 27001, 27002, 27003,
                27004, 38001, 38002, 38003, 38004,
                41001, 41002, 42001, 42002, 42003,
                43001, 43002, 43003, 43004
            ]
            for index, rule_value in enumerate(rs[1:]):
                if str(rule_id[index])[0:2] == '43':
                    user_id = -1
                else:
                    user_id = user_rs['id']

                sql = "insert into %s values(%s, %d, %d, '%s', %d)" % (
                    out_cur_risk, 'null', user_id,
                    rule_id[index], rule_value, user_rs['trade_server_id']
                )
                cur.execute(sql)
                self.logger.info(sql)
            conn.commit()
            self.logger.info("insert_cur_risk success!")
        except:
            conn.rollback()
            self.logger.exception("Exception Logged")
            self.logger.info("insert_cur_risk failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

    def query_cur_risk_auto(self, py_name):
        '''查询xtp_cur_risk_auto数据'''
        # 连接数据库
        conn = connectMysql()
        cur = conn.cursor()
        # 查询资金账号和股东账号
        self.logger.info("sql able to connect!")
        try:
            sql = "select * from %s where %s.py_name = '%s'" % (
                in_cur_risk, in_cur_risk, py_name
            )
            self.logger.info(sql)
            cur.execute(sql)
            rs = cur.fetchone()
            self.logger.info("insert_cur_risk success!")
            return rs
        except:
            self.logger.exception("Exception Logged")
            self.logger.info("insert_cur_risk failed!")
        finally:
            cur.close()
            # 关闭连接
            conn.close()

if __name__ == '__main__':
    sqldata = SqlData_Transfer()
    sqldata.delete_exch_sec()
    sqldata.insert_exch_sec()

    # # #
    # sqldata.delete_fund_creation()
    # sqldata.insert_fund_creation()
    # #
    # sqldata.delete_structured_fund_params()
    # sqldata.insert_structured_fund_params()

    sqldata.delete_stk_asset()
    sqldata.insert_stk_asset()

    # sqldata.delete_etf_baseinfo()
    # sqldata.insert_etf_baseinfo()

    # sqldata.delete_etf_components()
    # sqldata.insert_etf_components()

    # sqldata.delete_issue_params()
    # sqldata.insert_issue_params()

    # sqldata.delete_rights_issue_params()
    # sqldata.insert_rights_issue_params()

    # sqldata.delete_exch_sec()
    # sqldata.delete_stk_asset()
    # sqldata.delete_etf_baseinfo()
    # sqldata.delete_etf_components()
    # sqldata.delete_issue_params()
    # sqldata.delete_rights_issue_params()
    # sqldata.delete_fund_creation()
    # sqldata.delete_structured_fund_params()

    # # 期权
    # sqldata.delete_opt_exch_sec()
    # sqldata.insert_opt_exch_sec()

    # sqldata.delete_opt_stk_asset()
    # sqldata.insert_opt_stk_asset()

    # 两融
    sqldata.transfer_credit_guarantee_stk()

    sqldata.transfer_credit_cust_contract('')

    sqldata.transfer_credit_target_stk()

    sqldata.transfer_credit_cash_stk_asset()

    sqldata.keep_guarantee_stk()

    sqldata.transfer_credit_margin_rate_off()

    sqldata.transfer_credit_exceptional_stk()
