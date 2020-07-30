#!/usr/bin/python
# -*- encoding: utf-8 -*-
import MySQLdb
import time
import random
from log import *
import  sys
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import *


def CaseParmInsertMysql(case_goal,wt_reqs):
     logger.info('测试用例入参和期待结果插入数据库')
