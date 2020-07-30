#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os
import time
import unittest
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/GPMM')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/XjShRightSide')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/SjShRightSide')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/XjShObligationCall')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/SjShObligationCall')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/XjShObligationPut')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/SjShObligationPut')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/Exercise')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
import CaseService
import CaseServiceRisk
import CaseServiceOption

# 深圳现价case批量执行
def runCases( path, filename, sheet_name):
    '''
    :param cases: py名称集合
    :param filename: 存放case参数的文件名
    :return: None
    '''
    suite_cases = []
    excel_file = os.path.join(path, filename)
    case_service = CaseService.CaseService(excel_file,sheet_name)
    d = [(k, case_service.testcase_seq_dict[k]) for k in sorted(case_service.testcase_seq_dict.keys())]
    # 按顺序加载case
    for (k,case) in d:
        m = __import__(case['pyname'])
        cls = getattr(m, case['pyname'])
        print cls
        suite_case = unittest.TestLoader().loadTestsFromTestCase(cls)
        # suite_cases = []
        suite_cases.append(suite_case)
    suite = unittest.TestSuite(suite_cases)
    unittest.TextTestRunner(verbosity=2).run(suite)
        # time.sleep(10)

# 期权case批量执行
def runCasesOption(path, filename, sheet_name):
    suite_cases = []
    excel_file = os.path.join(path, filename)
    case_service = CaseServiceOption.CaseService(excel_file, sheet_name)
    d = [(k, case_service.testcase_seq_dict[k]) for k in sorted(case_service.testcase_seq_dict.keys())]
    # 按顺序加载case
    for (k, case) in d:
        print case['pyname']
        m = __import__(case['pyname'])
        cls = getattr(m, case['pyname'])
        print cls
        suite_case = unittest.TestLoader().loadTestsFromTestCase(cls)
        # suite_cases = []
        suite_cases.append(suite_case)
    suite = unittest.TestSuite(suite_cases)
    unittest.TextTestRunner(verbosity=2).run(suite)

def runCasesRisk(path, filename, sheet_name):
    '''
    :param cases: py名称集合
    :param filename: 存放case参数的文件名
    :return: None
    '''
    suite_cases = []
    excel_file = os.path.join(path, filename)
    case_service = CaseServiceRisk.CaseService(excel_file,sheet_name)
    d = [(k, case_service.testcase_seq_dict[k]) for k in sorted(case_service.testcase_seq_dict.keys())]
    # 按顺序加载case
    for (k,case) in d:
        m = __import__(case['pyname'])
        cls = getattr(m, case['pyname'])
        suite_case = unittest.TestLoader().loadTestsFromTestCase(cls)
        # suite_cases = []
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

def run_case(casepath_yw, filename, sheetname):
    casepath1 = '/home/yhl2/workspace/xtp_test/Autocase_Result/'+casepath_yw
    sys.path.append(casepath1)
    cases = getCases(casepath1)
    path = '/home/yhl2/workspace/xtp_test/utils'
    runCases(cases, path, filename, sheetname)


if __name__ == '__main__':
    path = '/home/yhl2/workspace/xtp_test/utils'
    # runCasesOption(path, u'个股期权自动化用例.xlsx', u'权利方限价_沪市')
    # runCasesOption(path, u'个股期权自动化用例.xlsx', u'权利方市价_沪市')
    # runCasesOption(path,  u'个股期权自动化用例.xlsx', u'义务方限价（认购合约）_沪市')
    # runCasesOption(path, u'个股期权自动化用例.xlsx', u'义务方市价（认购合约）_沪市')
    # runCasesOption(path, u'个股期权自动化用例.xlsx', u'义务方限价（认沽合约）_沪市')
    # runCasesOption(path, u'个股期权自动化用例.xlsx', u'义务方市价（认沽合约）_沪市')


