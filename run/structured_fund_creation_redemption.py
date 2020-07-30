#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os
import unittest
sys.path.append('/home/yhl2/workspace/xtp_test/StructuredFund/creationRedemption')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
import CaseServiceStructuredFundCreation

# 深圳现价case批量执行
def runCases(path, filename, sheet_name):
    '''
    :param filename: 存放case参数的文件名
    :return: None
    '''
    suite_cases = []
    excel_file = os.path.join(path, filename)
    case_service = CaseServiceStructuredFundCreation.CaseService(excel_file, sheet_name)
    d = [(k, case_service.testcase_seq_dict[k]) for k in
         sorted(case_service.testcase_seq_dict.keys())]
    # 按顺序加载case
    for (k,case) in d:
        m = __import__(case['pyname'])
        cls = getattr(m, case['pyname'])
        suite_case = unittest.TestLoader().loadTestsFromTestCase(cls)
        suite_cases.append(suite_case)
    suite = unittest.TestSuite(suite_cases)
    unittest.TextTestRunner(verbosity=2).run(suite)

def getCases(casepath):
    file_list = os.listdir(casepath)
    cases = []
    for file in file_list:
        if file[-2:] == 'py' and file != '__init__.py':
            file_index = file.find('.py')
            case = file[0:file_index]
            cases.append(case)
    return cases

if __name__ == '__main__':
    # py存放路径
    casepath = '/home/yhl2/workspace/xtp_test/StructuredFund/creationRedemption'
    cases = getCases(casepath)
    path = '/home/yhl2/workspace/xtp_test/utils'
    runCases(path, 'structured_fund_creation_redemption.xlsx', u'申赎')
