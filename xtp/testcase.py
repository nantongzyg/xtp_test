#!/home/vagrant/anaconda2/bin/python
# -*- encoding: utf-8 -*-

# 导入sleep
# 导入Api
# 导入Attribute
# 导入python单元测试模块
import unittest


# 单元测试基类
############################################################################
class XTPTestCase(unittest.TestCase):
    # --------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        super(XTPTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        """在每个用例执行之前会调用"""
        print
        pass

    def tearDown(self):
        """在每个用例执行之后会调用"""
        print
        pass

