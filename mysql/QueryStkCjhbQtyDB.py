#!/usr/bin/python
# -*- encoding: utf-8 -*-
from mysql_config import *

#数据库查询到的回报记录数
cjhb_count_db = 0
ashare_tuple_db = None

# 查询全成和部成的成交回报数
def QueryStkCjhbQtyDB(sqbh):
    global cjhb_count_db
    if sqbh != '':
        str_sql = "SELECT count(*) from ashare_cjhb WHERE sqbh = '" + sqbh + "'"
        conn = connectMssql()
        cur = conn.cursor()
        cur.execute(str_sql)
        rs = cur.fetchone()
        cur.close()
        conn.close()
        cjhb_count_db = rs[0]
    return cjhb_count_db


# 查询未成交情况
def QueryStkNoMatchDB(sqbh):
    global ashare_tuple_db
    if sqbh != '':
        str_sql = ("SELECT sum(CASE WHEN t1.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth, "
                     " sum(CASE WHEN t2.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth2, "
                     " sum(CASE WHEN t3.sqbh IS NOT NULL THEN 1 ELSE 0 END) AS reff_cjhb, "
                     " sum(CASE WHEN t4.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth_cancel "
                "from ashare_ordwth t1 "
             "LEFT JOIN ashare_ordwth2 t2 "
                 "on t1.reff = t2.reff "
             "LEFT JOIN ashare_cjhb t3 "
                 "ON t1.reff = t3.sqbh "
             "LEFT JOIN ashare_ordwth_cancel t4 "
                 "on t1.reff = t4.reff "
             " where t1.reff = '" + sqbh + "'")
        conn = connectMssql()
        cur = conn.cursor()
        cur.execute(str_sql)
        rs = cur.fetchone()
        cur.close()
        conn.close()
        ashare_tuple_db = rs
        return ashare_tuple_db

# 查询全撤情况
def QueryStkAllCanceledDB(sqbh,sqbh_cd):
    global ashare_tuple_db
    if sqbh != '':
        str_sql = ("SELECT sum(CASE WHEN t1.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth, "
                     " sum(CASE WHEN t2.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth2, "
                     " sum(CASE WHEN t3.sqbh IS NOT NULL THEN 1 ELSE 0 END) AS reff_cjhb, "
                     " sum(CASE WHEN t4.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth_cancel "
                "from ashare_ordwth t1 "
             "LEFT JOIN ashare_ordwth2 t2 "
                 "on t1.reff = t2.reff "
             "LEFT JOIN ashare_cjhb t3 "
                 "ON t1.reff = t3.sqbh "
             "LEFT JOIN ashare_ordwth_cancel t4 "
                 "on t1.reff = t4.reff "
             " where t1.reff in ('" + sqbh + "','" + sqbh_cd + "')")
        conn = connectMssql()
        cur = conn.cursor()
        cur.execute(str_sql)
        rs = cur.fetchone()
        cur.close()
        conn.close()
        ashare_tuple_db = rs
        return ashare_tuple_db

# 查询部撤情况
def QueryStkPartCanceledDB(sqbh,sqbh_cd):
    global ashare_tuple_db
    if sqbh != '':
        str_sql = ("SELECT sum(CASE WHEN t1.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth, "
                     " sum(CASE WHEN t2.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth2, "
                     " sum(CASE WHEN t3.sqbh IS NOT NULL THEN 1 ELSE 0 END) AS reff_cjhb, "
                     " sum(CASE WHEN t4.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth_cancel "
                "from ashare_ordwth t1 "
             "LEFT JOIN ashare_ordwth2 t2 "
                 "on t1.reff = t2.reff "
             "LEFT JOIN ashare_cjhb t3 "
                 "ON t1.reff = t3.sqbh "
             "LEFT JOIN ashare_ordwth_cancel t4 "
                 "on t1.reff = t4.reff "
             " where t1.reff in ('" + sqbh + "','" + sqbh_cd + "')")
        conn = connectMssql()
        cur = conn.cursor()
        cur.execute(str_sql)
        rs = cur.fetchone()
        cur.close()
        conn.close()
        ashare_tuple_db = rs
        return ashare_tuple_db

# 查询初始情况
def QueryStkInitDB(xtp_id_init):
    global ashare_tuple_db
    if xtp_id_init != '':
        str_sql = ("SELECT sum(CASE WHEN t1.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth, "
                     " sum(CASE WHEN t2.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth2, "
                     " sum(CASE WHEN t3.sqbh IS NOT NULL THEN 1 ELSE 0 END) AS reff_cjhb, "
                     " sum(CASE WHEN t4.reff IS NOT NULL THEN 1 ELSE 0 END) AS reff_ordwth_cancel "
                "from ashare_ordwth t1 "
             "LEFT JOIN ashare_ordwth2 t2 "
                 "on t1.reff = t2.reff "
             "LEFT JOIN ashare_cjhb t3 "
                 "ON t1.reff = t3.sqbh "
             "LEFT JOIN ashare_ordwth_cancel t4 "
                 "on t1.reff = t4.reff "
             " where t1.xtp_id_info = " + str(xtp_id_init[0]) + "")
        conn = connectMssql()
        cur = conn.cursor()
        cur.execute(str_sql)
        rs = cur.fetchone()
        cur.close()
        conn.close()
        ashare_tuple_db = rs
        return ashare_tuple_db








