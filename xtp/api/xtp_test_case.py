#!/usr/bin/python
# -*- encoding: utf-8 -*-

# 导入sleep
from time import sleep
# 导入Api
# from xtpapi import Api
from xtpapi import *
from xtp_data_type import *
# 导入Attribute
from attribute import Attribute
#
from utils import *

import unittest


# 单元测试基类
############################################################################
class xtp_test_case(unittest.TestCase):
    # --------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        super(xtp_test_case, self).__init__(*args, **kwargs)

    def setUp(self):
        """在每个用例执行之前会调用"""
        ver = Api.trade.GetApiVersion()
        print '---------api version: ' + ver + '-----------'
        #print

    def tearDown(self):
        """在每个用例执行之后会调用"""
        print '\n'
        pass

