#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from mainService import *
from CaseParmInsertMysql import *

class OrderCommon():

    def __init__(self, title, case_goal, stkparm, wt_reqs):
        self.title = title
        self.case_goal = case_goal
        self.stkparm = stkparm
        self.wt_reqs = wt_reqs

    def InsertOrderCommon(self):
        # 如果下单参数获取失败，则用例失败
        if self.stkparm['返回结果'] == False:
            rs = {
                '用例测试结果': self.stkparm['返回结果'],
                '测试错误原因': '获取下单参数失败,' + self.stkparm['错误原因'],
            }
            return rs
        else:
            ParmIni(Api, self.case_goal['期望状态'], self.wt_reqs['price_type'])
            CaseParmInsertMysql(self.case_goal, self.wt_reqs)
            rs = serviceTest(Api, self.case_goal, self.wt_reqs)
            return rs



