#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append('/home/yhl2/workspace/xtp_test/mysql')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/TSZLQX')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
import runcase_common
import CaseService

def runcase_TSZLQX():
    runcase_common.runCases(path, u'sj_qx.xlsx', u'TSZLQX')


if __name__ == '__main__':
    path = '/home/yhl2/workspace/xtp_test/utils'
    runcase_TSZLQX()
