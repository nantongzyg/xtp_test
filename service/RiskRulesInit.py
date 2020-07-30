#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
sys.path.append('/home/yhl2/workspace/xtp_test/mysql')
import database_manager
sys.path.append('/home/yhl2/workspace/xtp_test/xtp/api')
import config

# 插入风控数据，user_id和server_id动态获取
def RiskRulesInit(risk_file):
    query_info = {
        'table_name': 'xtp_user',
        'fieldname_list': ['id', 'trade_server_id'],
        'query_condition': {'user_name': config.CONST_TRADE_USER},
        'fetch_type': 2
    }
    rs = database_manager.QueryTable(query_info['table_name'],
                                     query_info['fieldname_list'],
                                     query_info['query_condition'],
                                     query_info['fetch_type'])

    rule_info = {
        'table_name': 'xtp_cur_risk',  # 风控表名
        'fieldname_list': ['user_id', 'rule_id', 'value', 'server_id'], # 风控插入字段
        'delete_condition': {'server_id': rs['trade_server_id']},
    }
    database_manager.DeleteTable(rule_info['table_name'],
                                 rule_info['delete_condition'])

    with open(risk_file, 'r') as f:
        for line in f:
            risk = line.strip('\n')
            risk_list = risk.split('|')
            res_risk = risk_list
            for index, item in enumerate(risk_list):
                if item == 'user_id':
                    res_risk[index] = rs['id']
                elif item == 'server_id':
                    res_risk[index] = rs['trade_server_id']
                else:
                    pass
            database_manager.InsertTable(rule_info['table_name'],
                                         rule_info['fieldname_list'],
                                         res_risk)
