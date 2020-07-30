#!/usr/bin/python
# -*- encoding: utf-8 -*-

import xlrd
from templet import *
import collections
import os
import logging


def list_todict(l1, l2):
    ###两个list打包成一个dict
    return dict(zip(l1, l2))

def pyname_seq(D1):
    # 对字典的value值进行编码，处理成想要的格式。
    pyname_seq_dict = collections.OrderedDict()
    if D1['对象'].encode('utf-8') != '-':
        pyname_seq_dict['pyname'] = D1['pyname'].encode('utf-8')
        pyname_seq_dict['seq'] = int(D1['seq'])
    return pyname_seq_dict

class CaseService():
    def __init__(self,excel_file):
        #self.excel_file = u'股票买卖自动化case参数模板.xlsx'
        excel_rs = self.read_excel(excel_file)
        self.testcase_seq_dict = excel_rs
        self.log_file=excel_file+'.log'
        logging.basicConfig(filename=self.log_file, filemode="w",
                            format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",
                            level=logging.INFO)
        self.logger = logging.getLogger("log_demo")

    def read_excel(self, excel_file):
        ###用于读取excel的文件，
        data = xlrd.open_workbook(excel_file, encoding_override='utf-8')
        # 获取一个工作表
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        title_list = table.row_values(0)
        title_list = map(lambda x: x.encode('utf-8'), title_list)
        # 构造用户一个测试例文件名(pyname)-测试例名参数表
        testcase_seq_dict = {}
        # 循环行列表数据
        for i in range(1, nrows):
            para_list = table.row_values(i)
            para_dict = list_todict(title_list, para_list)
            if para_dict['对象'] != '-':
                pyname_seq_dict = pyname_seq(para_dict)
                testcase_seq_dict[pyname_seq_dict['seq']] = pyname_seq_dict
        return testcase_seq_dict



