#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append('/home/yhl2/workspace/xtp_test/mysql')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/CYBGGPGQX')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
import runcase_allPayment
import CaseService

def runcase_CYBGGPGQX():
    runcase_allPayment.runCases(path, u'sj_qx.xlsx', u'CYBGGPGQX')


if __name__ == '__main__':
    path = '/home/yhl2/workspace/xtp_test/utils'
    runcase_CYBGGPGQX()
