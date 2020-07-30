#!/usr/bin/python
# -*- encoding: utf-8 -*-

from opt_mysql_config import connectMysql

def TruncateTable(tablename):
    sql = 'TRUNCATE TABLE %s' % tablename
    db = connectMysql()
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        db.rollback()
        db.close()
        return False

def InsertTable(tablename, fieldname_list, fieldvalue_list):
    if len(fieldname_list) == 0:
        return False
    if len(fieldvalue_list) == 0:
        return False
    sql = "insert into %s(" % tablename
    count = 0
    for name in fieldname_list:
        sql += name
        count += 1
        if count == len(fieldname_list):
          sql += ')'
        else:
          sql += ','
    sql += ' VALUES('
    count = 0
    for value in fieldvalue_list:
        if type(value) == str:
          sql += "'"
          sql += value
          sql += "'"
        else:
          sql += str(value)
        count += 1
        if count == len(fieldvalue_list):
          sql += ')'
        else:
          sql += ','
    db = connectMysql()
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        db.rollback()
        db.close()
        return False

def UpdateTable(tablename, update_action, update_condition):
    if type(update_action) != str:
        return False
    if type(update_condition) != dict:
        return False
    sql = "update %s set %s " % (tablename, update_action)
    if len(update_condition) > 0:
       for (k,v) in update_condition.items():
           sql += " where %s = %s " % (k, v) 
    db = connectMysql()
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        db.rollback()
        db.close()
        return False

def DeleteTable(tablename, delete_condition):
    if type(delete_condition) != dict:
        return False
    sql = "delete from %s" % (tablename)
    if len(delete_condition) > 0:
        sql += " where 1 = 1"
        for (k,v) in delete_condition.items():
           sql += " and %s = %s " % (k, v)
    print sql
    db = connectMysql()
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        db.rollback()
        db.close()
        return False

def QueryTable(tablename, fieldname_list, query_condition,fetch_type):
    '''

    :param tablename: 表名
    :param fieldname_list: 查询字段列表，[field, field2,...]
    :param query_condition: 查询条件， {'k1': 'v1', 'k2': 'v2', ...}
    :param fetch_type: 1-查询所有结果，2-查询一条结果
    :return: fetch_type-1:[{},{}], fetch_type-2:{}
    '''
    if len(fieldname_list) == 0:
        return False
    if fieldname_list == '*': # 暂时不支持select *
        return False
    sql = 'select '
    count = 0
    for name in fieldname_list:
        sql += name
        count += 1
        if count == len(fieldname_list):
            sql += ''
        else:
            sql += ','
    sql += ' from %s' % tablename
    sql += ' where 1=1'
    if len(query_condition) > 0:
       for (k,v) in query_condition.items():
           if isinstance(v, str):
               sql += " and %s = %s " % (k, "'" + v + "'")
           else:
               sql += " and %s = %s " % (k, v)
    db = connectMysql()
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        if fetch_type == 1:
            rs_ret = []
            result = cursor.fetchall()
            if result != ():
                for rs in result:
                    for index, name in enumerate(fieldname_list):
                        rs_dict = {}
                        rs_dict[name] = rs[index]
                        rs_ret.append(rs_dict)
        elif fetch_type == 2:
            rs_ret = {}
            result = cursor.fetchone()
            if result != ():
                for index, name in enumerate(fieldname_list):
                    rs_ret[name] = result[index]
        else:
            rs_ret = None
        return rs_ret
    except:
        return False
    finally:
        db.close()
