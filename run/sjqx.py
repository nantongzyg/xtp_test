#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append('/home/yhl2/workspace/xtp_test/mysql')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/SJQX')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
import runcase_common
import CaseService

def runcase_SJ_QX():
    runcase_common.runCases(path, u'sj_qx.xlsx', u'SJQX')


if __name__ == '__main__':
    path = '/home/yhl2/workspace/xtp_test/utils'
    runcase_SJ_QX()
